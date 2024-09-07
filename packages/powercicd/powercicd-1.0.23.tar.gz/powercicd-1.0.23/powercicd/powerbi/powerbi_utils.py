import json
import os
import re
import fnmatch
import shutil
from typing import Callable, Literal
import zipfile
from jsonpath_ng.ext import parse
import logging

from powercicd.config_utils import VisibilityAction, get_first_matching_key_pattern
from powercicd.shared.logging_utils import log_call

log = logging.getLogger("powercicd.powerbi")

_save_layout_transformation_step_increment = 0

def save_layout_transformation_step(layout, filepath):
    global _save_layout_transformation_step_increment
    _save_layout_transformation_step_increment += 1
    
    folder = os.path.normpath(os.path.abspath(os.path.dirname(filepath)))
    file   = os.path.basename(filepath)
    file_with_increment = f"{_save_layout_transformation_step_increment:02}_{file}"
    filepath_with_increment = f"{folder}/{file_with_increment}"
    
    log.debug(f"Writing result to '{filepath_with_increment}'...")
    os.makedirs(os.path.dirname(filepath_with_increment), exist_ok=True)
    with open(filepath_with_increment, 'w', encoding='utf-8') as f:
        json.dump(layout, f, indent=2, ensure_ascii=False)


def constant_fn_factory(constant):
    def constant_fn(x):
        return constant

    constant_fn.__name__ = f"constant_fn_{constant}"
    return constant_fn


def replace_field_value(
    layout,
    rel_jsonpath_to_key_field: str,
    rel_jsonpath_to_value_field: str,
    key_regex_pattern: str,
    substitution_fn: str | Callable[[dict], str]
):
    # convert to callable non callable sub_fn
    if not callable(substitution_fn):
        substitution_fn = constant_fn_factory(substitution_fn)

    parser_visual_containers_expr = f"$.sections[*].visualContainers[*]"
    parser_visual_containers      = parse(parser_visual_containers_expr)
    parser_key_field              = parse(rel_jsonpath_to_key_field)
    parser_value_field            = parse(rel_jsonpath_to_value_field)

    count = 0
    for visual_container_match in parser_visual_containers.find(layout):
        visual_container_path = visual_container_match.full_path
        visual_container      = visual_container_match.value

        # filter visual container with no matching key
        key_matches = parser_key_field.find(visual_container)
        key_match   = key_matches[0] if len(key_matches) > 0 else None
        if key_match is None:
            continue
        key_path        = key_match.full_path
        key_str         = key_match.value
        key_regex_match = re.match(key_regex_pattern, key_str)
        if key_regex_match is None:
            continue
        key_groups = key_regex_match.groupdict()

        # processing value path
        # - here we are not sure that visual container owns the full path to the visual. If it does not, then we only log an information
        value_matches = parser_value_field.find(visual_container)
        value_match   = value_matches[0] if len(value_matches) > 0 else None
        if value_match is None:
            log.warning(f"- Substitution skipped at path: {visual_container_path}, key: {key_path}/{key_str} (groups: {key_groups}): No value at relative jsonpath found: {rel_jsonpath_to_value_field}")
            continue

        value_path    = value_match.full_path
        value_old_str = value_match.value

        value_new_str = substitution_fn(key_groups)
        value_path.update(visual_container, value_new_str)

        # substitute only once
        for vm in value_matches[1:]:
            value_path.update(visual_container, "")

        log.debug(f"- Successful substitution at path: {visual_container_path}, key: {key_path}/{key_str} (groups: {key_groups}), value path: {value_path} / old value: {value_old_str}, new value: {value_new_str}")
        count += 1

    if count > 0:
        log.debug(f"Replaced {count} values")
    else:
        log.warning(f"Nothing performed for substitution request: key path {rel_jsonpath_to_key_field} / regex {key_regex_pattern} and value path {rel_jsonpath_to_value_field}")


def stringify_json(layout, jsonpath_expr, tmp_folder):
    log.debug(f"jsonify_string_jsons: {jsonpath_expr}")    
    parser = parse(jsonpath_expr)
    for match in parser.find(layout):
        full_path = match.full_path
        value     = match.value
        new_value = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
        full_path.update(layout, new_value)
    save_layout_transformation_step(layout, f"{tmp_folder}/{jsonpath_expr.replace('*', 'star')}.json")
    return layout


def jsonify_string(layout, jsonpath_expr, tmp_folder):
    log.debug(f"jsonify_string: {jsonpath_expr}")    
    parser = parse(jsonpath_expr)
    for match in parser.find(layout):
        full_path = match.full_path
        value     = match.value
        new_value = json.loads(value)
        full_path.update(layout, new_value)
    save_layout_transformation_step(layout, f"{tmp_folder}/{jsonpath_expr.replace('*', 'star')}.json")
    return layout
    

def convert_original_to_src_layout(
    layout_file_path: str, 
    layout_code_path: str,
    tmp_folder: str
):
    log.debug(f"Reading layout file '{layout_file_path}' and decoding string JSONs...")
    with open(layout_file_path, 'r', encoding='utf-16 le') as f:
        layout = json.load(f)
    save_layout_transformation_step(layout, f"{tmp_folder}/10_layout_after_read.json")
    
    layout = jsonify_string(layout, "$[config]", tmp_folder)
    layout = jsonify_string(layout, "$.sections[*][config,filters]", tmp_folder)
    layout = jsonify_string(layout, "$.sections[*].visualContainers[*][config,filters,query,dataTransforms]", tmp_folder) 

    # apply version substitution
    log.debug(f"Applying version substitution...")
    replace_field_value(
        layout,
        "$.config.singleVisual.vcObjects.general[0].properties.altText.expr.Literal.Value",
        "$.config.singleVisual.objects.general[0].properties.paragraphs[*].textRuns[*].value",
        r"^.*\[\[\[report_version\]\]\].*$",
        "REPORT_VERSION_REMOVED_BY_BUILD_SCRIPT"
    )
    # apply powerapps app id substitution
    log.debug(f"Applying powerapps app id substitution...")
    replace_field_value(
        layout,
        "$.config.singleVisual.vcObjects.general[0].properties.altText.expr.Literal.Value",
        "$.config.singleVisual.objects.general[0].properties.appId.expr.Literal.Value",
        r"^.*\[\[\[powerapps\:(?P<app_name>.*)\]\]\].*$",
        "POWERAPPS_APP_ID_REMOVED_BY_BUILD_SCRIPT",
    )
            
    # write to code file
    os.makedirs(os.path.dirname(layout_code_path), exist_ok=True)
    with open(layout_code_path, 'w', encoding='utf-8') as f:
        json.dump(layout, f, indent=2, ensure_ascii=False)

    # delete original file
    os.remove(layout_file_path)


def convert_src_code_to_original_layout(
    code_file                       : str,
    layout_file                     : str,
    tmp_folder                      : str,
    powerapps_id_by_name            : dict,
    page_visibility_actions : list[dict[VisibilityAction, str]],
    report_version                  : str,
):
    log.debug(f"Processing layout code file: '{code_file}'")
    with open(code_file, 'r', encoding='utf-8') as f:
        layout = json.load(f)

    # apply version substitution
    log.debug(f"Applying version substitution...")
    replace_field_value(
        layout,
        "$.config.singleVisual.vcObjects.general[0].properties.altText.expr.Literal.Value",
        "$.config.singleVisual.objects.general[0].properties.paragraphs[0].textRuns[0].value",
        r"^.*\[\[\[report_version\]\]\].*$",
        report_version
    )
    save_layout_transformation_step(layout, f"{tmp_folder}/after_version_substitutions.json")

    # apply powerapps app id substitution
    log.debug(f"Applying powerapps app id substitution...")

    def powerapps_id_by_name_fn(key_regex_match):
        """This inner function is used to substitute the powerapps app name with the corresponding app id"""
        app_name = key_regex_match["app_name"]
        if app_name not in powerapps_id_by_name:
            msg = f"PowerApps app '{app_name}' not found in the project configuration but it is referenced in the layout. Please add it to the component configuration in block 'powerapps_id_by_name'"
            log.error(msg)
            raise ValueError(msg)
        app_id = powerapps_id_by_name[app_name]
        return f"'/providers/Microsoft.PowerApps/apps/{app_id}'"
    
    replace_field_value(
        layout,
        "$.config.singleVisual.vcObjects.general[0].properties.altText.expr.Literal.Value",
        "$.config.singleVisual.objects.general[0].properties.appId.expr.Literal.Value",
        r"^.*\[\[\[powerapps\:(?P<app_name>.*)\]\]\].*$",
        powerapps_id_by_name_fn
    )
    save_layout_transformation_step(layout, f"{tmp_folder}/after_powerapps_guid_substitutions.json")

    # set visibility of sections if needed
    log.debug(f"Setting visibility of sections...")
    for section_match in parse("$.sections[*]").find(layout):
        section_value   = section_match.value
        section_name    = section_match.value["displayName"]
        old_visibility  = section_value.get("config", {}).get("visibility", 0)  # remark: 0 is visible, 1 is hidden!!!!!!!
        action, pattern = get_first_matching_key_pattern(page_visibility_actions, section_name) or ("keep", None)
        new_visibility  = 1 if action == "hide" else 0 if action == "show" else old_visibility
        log.debug(f"Set section visibility: {action}: '{section_name}' (matching pattern '{pattern}')")
        section_value["config"]["visibility"] = new_visibility
    save_layout_transformation_step(layout, f"{tmp_folder}/after_visibility_changes.json")

    layout = stringify_json(layout, "$[config]", tmp_folder)
    layout = stringify_json(layout, "$.sections[*][config,filters]", tmp_folder)
    layout = stringify_json(layout, "$.sections[*].visualContainers[*][config,filters,query,dataTransforms]", tmp_folder)

    # write to layout file
    os.makedirs(os.path.dirname(layout_file), exist_ok=True)    
    with open(layout_file, 'w', encoding='utf-16 le') as f:
        json.dump(layout, f, indent=None, ensure_ascii=False, separators=(',', ':'))

    # delete code file
    os.remove(code_file)


@log_call(log)
def convert_pbix_to_src_code(
    pbix_file       : str,
    src_code_folder : str,
    tmp_folder      : str
):
    pbix_content_dir = f"{tmp_folder}/pbix_content"
    log.debug(f"Unzipping '{pbix_file}' to '{pbix_content_dir}'")
    os.makedirs(pbix_content_dir, exist_ok=True)
    with zipfile.ZipFile(pbix_file, 'r') as zip_ref:
        zip_ref.extractall(pbix_content_dir)

    # transform "original layout" to "src layout"
    original_file = f"{pbix_content_dir}/Report/Layout"
    code_file     = f"{pbix_content_dir}/Report/Layout.json"
    log.debug(f"Converting '{original_file}' to '{code_file}'")
    convert_original_to_src_layout(original_file, code_file, tmp_folder)
    
    log.debug(f"Copying content of '{pbix_content_dir}/' to '{src_code_folder}/'")
    if os.path.exists(src_code_folder):
        shutil.rmtree(src_code_folder)
    shutil.copytree(pbix_content_dir, src_code_folder)
    log.debug(f"Copying done.")


@log_call(log)
def convert_src_code_to_pbix(
    src_code_folder         : str,
    pbix_filepath           : str,
    tmp_folder              : str,
    powerapps_id_by_name    : dict,
    page_visibility_actions : list[dict[VisibilityAction, str]],
    version                 : str
):
    pbix_content_dir = f"{tmp_folder}/pbix_content"
    log.debug(f"Copying content of '{src_code_folder}/' to '{pbix_content_dir}/'")
    if os.path.exists(pbix_content_dir):
        shutil.rmtree(pbix_content_dir)
    shutil.copytree(src_code_folder, pbix_content_dir)
    log.debug(f"Copying done.")

    # transform "src layout" to "original layout"
    code_file     = f"{pbix_content_dir}/Report/Layout.json"
    original_file = f"{pbix_content_dir}/Report/Layout"
    log.debug(f"Converting '{code_file}' to '{original_file}'")
    convert_src_code_to_original_layout(
        code_file, 
        original_file, 
        tmp_folder, 
        powerapps_id_by_name, 
        page_visibility_actions,
        version
    )

    log.debug(f"Zipping '{pbix_content_dir}' to '{pbix_filepath}'")
    os.makedirs(os.path.dirname(pbix_filepath), exist_ok=True)
    with zipfile.ZipFile(pbix_filepath, 'w', zipfile.ZIP_STORED) as zip_ref:
        for root, dirs, files in os.walk(pbix_content_dir):
            for file in files:
                abs_path = f"{root}/{file}"
                rel_path = os.path.relpath(abs_path, pbix_content_dir)
                if rel_path == "SecurityBindings":
                    log.debug(f"...Skipping '{rel_path}'")
                    continue
                zip_ref.write(abs_path, rel_path)
    log.debug(f"Zipping done.")
