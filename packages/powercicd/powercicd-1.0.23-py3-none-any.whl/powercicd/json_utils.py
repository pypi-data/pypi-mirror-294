import copy
import logging
from typing import Any
from jsonpath_ng.ext import parse

log = logging.getLogger(__name__)


def apply_substitution(json_tree, value_path, replacement):
    log.debug(f"Applying substitution '{value_path}' -> '{replacement}':")
    parser = parse(value_path)        
    count = 0
    for match in parser.find(json_tree):
        count += 1
        full_path = match.full_path
        value = match.value
        log.debug(f"- Replacing at '{full_path}' old value '{value}' with '{replacement}'")
        value.update(json_tree, replacement)
    if count == 0:
        log.debug(f"- Substitution '{value_path}' -> '{replacement}' did not match any value.")


DISPATCH_VARIABLE_PREFIX = "~>"


def apply_switches(json_tree: Any, switch_variables: dict):
    return _apply_switches_recursive(json_tree, switch_variables)


def _apply_switches_recursive(json_tree: Any, switch_variables: dict, debug_path=None):
    f"""
    Recursively apply switches to a JSON tree. The switches are defined by a key starting with {DISPATCH_VARIABLE_PREFIX}.
    """
    if debug_path is None:
        debug_path = []
    if isinstance(json_tree, dict):
        conventional_keys = {key for key in json_tree if not key.startswith(DISPATCH_VARIABLE_PREFIX)}
        result = {
            key: _apply_switches_recursive(json_tree[key], switch_variables, debug_path + [key])
            for key
            in conventional_keys
        }

        switch_variable_names_with_prefix = {k for k in json_tree if k not in conventional_keys}
        if len(switch_variable_names_with_prefix) > 1:
            raise ValueError(f"Only one substitution key starting with '{DISPATCH_VARIABLE_PREFIX}' is allowed at path '{debug_path}'. Found: {switch_variable_names_with_prefix}")
        elif len(switch_variable_names_with_prefix) == 0:
            pass
        else:
            switch_variable_name_with_prefix = switch_variable_names_with_prefix.pop()
            switch_variable_name             = switch_variable_name_with_prefix[len(DISPATCH_VARIABLE_PREFIX):]
            switch_cases                     = json_tree[switch_variable_name_with_prefix]
            
            if not isinstance(switch_cases, dict):
                raise ValueError(f"Expected a dictionary value for '{DISPATCH_VARIABLE_PREFIX}' at path '{debug_path}'")
            
            if switch_variable_name not in switch_variables:
                log.info(f"Switch at path '{debug_path}' ignored because '{switch_variable_name}' is not defined as switch variables. Are defined: {list(switch_variables.keys())}")
            else:
                switch_variable_value = switch_variables[switch_variable_name]
                if switch_variable_value not in switch_cases:
                    log.info(f"Switch at path '{debug_path}' ignored because '{switch_variable_name}={switch_variables[switch_variable_name]}' is not defined in switch cases. Are defined: {list(switch_cases.keys())}")
                else:                
                    switch_value = switch_cases[switch_variable_value]
                    result = {
                        **result,
                        **_apply_switches_recursive(switch_value, switch_variables, debug_path + [switch_variable_name_with_prefix])
                    }            
        return result
    elif isinstance(json_tree, list):
        return [
            _apply_switches_recursive(value, switch_variables, debug_path + [index])
            for index, value 
            in enumerate(json_tree)
        ]
    else:
        return json_tree

    
class JsonschemaEnhancerForSubstitutionSupport:
    """
    Enhances a JSON schema to support substitution of values at each node with switch capability.
    """
    def __init__(self, json_schema: Any, option_object_marker: str, fallback_key: str | None, common_key: str | None):
        self.json_schema = json_schema
        self.option_object_marker = option_object_marker
        self.fallback_key = fallback_key
        self.common_key = common_key
        self.result_defs = {}

    def enhance(self):
        result = self.enhance_recursive(self.json_schema, [])
        result["$defs"] = {
            **result.get("$defs", {}),
            **self.result_defs
        } 
        return result
            
    def enhance_recursive(self, node, path):
        if isinstance(node, dict):
            transformed_subtree = {
                key: self.enhance_recursive(value, path + [key])
                for key, value 
                in node.items()
            }
            node_jsonschema_type = transformed_subtree.get("type", None)
            if node_jsonschema_type != "object":
                return transformed_subtree
            
            # compute non-overridable properties                
            all_properties             = set(transformed_subtree.get("properties", {}))
            non_overridable_properties = { key for key in all_properties if "const" in transformed_subtree["properties"][key] }
            overridable_properties     = all_properties - non_overridable_properties
            required_properties        = set(transformed_subtree.get("required", []))            
            base_subtree               = copy.deepcopy(transformed_subtree)
            base_subtree["required"]   = list(non_overridable_properties)
            over_subtree               = copy.deepcopy(transformed_subtree)
            over_subtree["required"]   = []
            over_subtree["properties"] = { key: over_subtree["properties"][key] for key in overridable_properties }            
            over_subtree_id            = "OVERRIDES_" + ".".join([str(p) for p in path])
            if "title" in over_subtree:
                over_subtree["title"] = f"OVERRIDES for {over_subtree['title']}"
            self.result_defs[over_subtree_id] = over_subtree
            if "properties" not in base_subtree:
                base_subtree["properties"] = {}
            base_subtree["properties"][self.option_object_marker] = {
                "type": "object",
                "description": f"Switch depending on '{self.option_object_marker}'",
                "properties": {
                    ".*": {
                        "$ref": f"#/$defs/{over_subtree_id}"
                    }
                }
            }
            return base_subtree
        elif isinstance(node, list):
            return [
                self.enhance_recursive(value, path + [index])
                for index, value in enumerate(node)
            ]
        else:
            return node

    def build_partial_substitution_schema(self, partial_obj_ref_id, ):
        return {
            "type": "object",
            "properties": {
                self.option_object_marker: {
                    "type": "object",
                    "description": f"Substitution depending on the value of '{self.option_object_marker}'",
                    "properties": {
                        self.fallback_key: {
                            "$ref": f"#/$defs/{partial_obj_ref_id}"
                        },
                        self.common_key: {
                            "$ref": f"#/$defs/{partial_obj_ref_id}"
                        },
                        # any marker/dispatcher key is allowed
                        ".*": {
                            "$ref": f"#/$defs/{partial_obj_ref_id}"
                        }                        
                    }
                }
            },
            "required": [self.option_object_marker]
        }