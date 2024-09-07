# %%
import inspect
import json
import logging
import os
import re
from datetime import date, datetime
from enum import Enum
from typing import Literal

import tabulate
import typer
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel
from typing_extensions import Annotated

import powercicd.powerbi.powerbi_utils as powerbi_utils
from powercicd.config import get_project_config
from powercicd.powerbi.config import PowerBiComponentConfig
from powercicd.powerbi.powerbi_client import PowerBiWebClient

# first dotenv
load_dotenv()

# then logging
log_level  = os.getenv('LOG_LEVEL' , 'INFO').upper()
logging.basicConfig(level=log_level, format="%(asctime)s %(levelname).1s %(name)-17s %(message)s", datefmt='%H:%M:%S')
log = logging.getLogger("powercicd.cli")
# set log level one step higher because these libraries are too verbose:
# - msal.authority
# - azure.core.pipeline.policies.http_logging_policy
# - azure.identity._internal.interactive
next_log_level = 10 + getattr(logging, log_level)
logging.getLogger("msal.authority"                                   ).setLevel(next_log_level)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy" ).setLevel(next_log_level)
logging.getLogger("azure.identity._internal.interactive"             ).setLevel(next_log_level)


class OutputFormat(Enum):
    table: Literal["table"] = "table"
    json : Literal["json" ] = "json"
    yaml : Literal["yaml" ] = "yaml"


DEFAULT_OUTPUT_FMT = "yaml"


main_cli = typer.Typer()
config_cli = typer.Typer()
main_cli.add_typer(config_cli, name="config")
powerbi_cli = typer.Typer()
main_cli.add_typer(powerbi_cli, name="powerbi")


def get_tmp_dir(project_dir, suffix):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    tmp_dir = f"{project_dir}/temp/{timestamp}-{suffix}"
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


class CliCtx:
    def __init__(self, lookup_path, output_fmt, keep_browser_open, headless, selenium_user_dir):
        self.lookup_path       = lookup_path
        self.output_fmt        = output_fmt
        self.project_config    = get_project_config(self.lookup_path)
        self.keep_browser_open = keep_browser_open
        self.headless          = headless
        self.selenium_user_dir = selenium_user_dir

    def prepare_output(self, data):
        if isinstance(data, list):
            return [self.prepare_output(d) for d in data]
        if isinstance(data, dict):
            return {k: self.prepare_output(v) for k, v in data.items()}
        elif isinstance(data, BaseModel):
            fields = data.model_dump()
            # add all field values which are annotated by @property too
            getters = { f"({k})": getattr(data, k) for k, member in inspect.getmembers(data.__class__) if isinstance(member, property) and not k.startswith("_") }        
            # avoids recursion in the output: keep only simple types
            getters = {k: v for k, v in getters.items() if isinstance(v, (str, int, float, bool, list, dict))}
            all_relevant_fields = {**fields, **getters}
            return {k: self.prepare_output(v) for k, v in all_relevant_fields.items()}
        elif isinstance(data, Enum):
            return data.value
        elif isinstance(data, (datetime, date)):
            return data.isoformat()
        else:
            return data
            
    def get_result_echo(self, result):
        result = self.prepare_output(result)
        if self.output_fmt == "json":
            return json.dumps(result, indent=2)
        elif self.output_fmt == "yaml":
            return yaml.dump(result, default_flow_style=False)
        else:
            return tabulate.tabulate(result, headers="keys", tablefmt="pretty")
        
    def echo_result(self, result):
        result_echo = self.get_result_echo(result)
        typer.echo(result_echo)

    def get_pbi_client(self):
        return PowerBiWebClient(tenant=self.project_config.tenant, keep_browser_open=self.keep_browser_open, headless=self.headless, selenium_user_dir=self.selenium_user_dir)


@main_cli.callback(no_args_is_help=True)
def shared_to_all_commands(
    ctx: typer.Context,
    project_dir : Annotated[str, typer.Option(
        help="The project directory to work on. If not defined, then the current directory is used as lookup start point towards file system root",
        prompt=False
    )] = None,
    output_fmt : Annotated[str, typer.Option(
        help="The output format to use for the command",
        prompt=False,
        envvar="OUTPUT_FMT"
    )] = DEFAULT_OUTPUT_FMT,
    keep_browser_open: Annotated[bool, typer.Option(
        help="Keep the browser open after use of it (for debugging purposes)",
        prompt=False,
        envvar="KEEP_BROWSER_OPEN"
    )] = False,
    headless: Annotated[bool, typer.Option(
        help="Run the browser in headless mode (unless user interaction required -> for authentication)",
        prompt=False,
        envvar="HEADLESS"
    )] = True,
    selenium_user_dir: Annotated[str, typer.Option(
        help="The directory to store the selenium user data. if not explicitely set, then '.selenium' is used",
        prompt=False,
        envvar="SELENIUM_USER_DIR"
    )] = ".selenium",
):
    ctx.obj = CliCtx(lookup_path=project_dir, output_fmt=output_fmt, keep_browser_open=keep_browser_open, headless=headless, selenium_user_dir=selenium_user_dir)
    ctx.ensure_object(CliCtx)


@config_cli.command(short_help="configure vscode for the project")
def setup_vscode(
    ctx: typer.Context
):
    curr_dir = os.getcwd()
        
    # Create the .vscode folder if it does not exist
    vscode_folder = f"{curr_dir}/.vscode"
    if not os.path.exists(vscode_folder):
        log.info(f"Creating vscode folder '{vscode_folder}'")
        os.makedirs(vscode_folder, exist_ok=True)
    else:
        log.info(f"vscode folder '{vscode_folder}' already exists")
        
    # Create the settings.json file if it does not exist
    settings_json_file = f"{vscode_folder}/settings.json"
    if not os.path.exists(settings_json_file):
        log.info(f"Creating vscode settings.json file '{settings_json_file}'")
        with open(settings_json_file, "w") as f:
            f.write("{\n}")
    else:
        log.info(f"vscode settings.json file '{settings_json_file}' already exists")
            
    # Read the settings file
    log.info(f"Updating vscode settings.json file '{settings_json_file}'")
    with open(settings_json_file, "r") as f:
        settings = json.load(f)
    
    # Add yaml schemas if not already present
    if "yaml.schemas" not in settings:
        settings["yaml.schemas"] = {}
    yaml_schemas = settings["yaml.schemas"]
    yaml_schemas.update({
        "doc/generated/component_config.jsonschema.json": "power-component.yaml",
        "doc/generated/project_config.jsonschema.json": "power-project.yaml"    
    })    

    # Write the settings file back
    log.info(f"Writing vscode settings.json file '{settings_json_file}'")
    with open(settings_json_file, "w") as f:
        json.dump(settings, f, indent=2)
    log.info("Done!")


@main_cli.command("list", short_help="List all components")
def list_(
    ctx: typer.Context
):
    cli_ctx: CliCtx = ctx.obj
    cli_ctx.echo_result(cli_ctx.project_config.component_raw_configs)


# ------------------------------


@powerbi_cli.command("list", short_help="List all powerbi components")
def list_(
    ctx: typer.Context
):
    cli_ctx: CliCtx = ctx.obj
    cli_ctx.echo_result(cli_ctx.project_config.get_component_raw_configs_by_type("powerbi"))


@powerbi_cli.command(short_help="Login to PowerBI")
def login(
    ctx: typer.Context
):
    cli_ctx: CliCtx = ctx.obj
    pbi = cli_ctx.get_pbi_client()
    pbi.login_for_selenium()
    pbi.close_browser()


@powerbi_cli.command(short_help="Deploy PowerBI components")
def deploy(
    ctx: typer.Context,
    stage : Annotated[str, typer.Option(
        show_default=False,
        help="The cloud stage to use. this env designation will be used as suffix to find the project and component configuration files"
    )],
    components: Annotated[list[str], typer.Argument(
        help="The component to deploy"
    )] = None,
    deploy_report: Annotated[bool, typer.Option(
        prompt=False, help="Deploy the report",
    )] = True,
    deploy_app: Annotated[bool, typer.Option(
        prompt=False, help="Deploy the app",
    )] = True
):
    if not deploy_report and not deploy_app:
        log.error("Nothing to deploy: neither report nor app is selected. Exiting...")
        return

    cli_ctx: CliCtx = ctx.obj
    project_config = cli_ctx.project_config
    tmp_folder = get_tmp_dir(project_config.project_dir, "deploy")

    if components is None:
        component_configs = project_config.get_component_configs_by_type("powerbi", stage=stage)
        components = [c.name for c in component_configs]
        msg = f"Do you want to deploy all powerbi components ({', '.join(components)})? (y/n)"
        if not typer.confirm(msg):
            return
    else:
        component_configs = [project_config.get_component_config(component_name, stage=stage) for component_name in components]

    pbi = cli_ctx.get_pbi_client()

    # first the app login, because it is definitively the most expensive with the browser, and
    # it ensures that the correct browser is active for the api login, where the user has already logged in
    if deploy_app:
        pbi.login_for_selenium()
    pbi.login_for_powerbi_api()

    if deploy_report:
        component_config: PowerBiComponentConfig
        for component_config in component_configs:
            group = pbi.get_group_by_name(component_config.group_name)
            upload_report_name = f"{component_config.report_name} {project_config.version.resulting_version}"

            src_code_folder = f"{component_config.component_root}/src"
            pbix_filepath = f"{tmp_folder}/{upload_report_name}.pbix"

            dataset_parameters = component_config.dataset_parameters.copy()
            dataset_parameters[component_config.version_parameter_name] = project_config.version.resulting_version

            # convert src code to pbix
            powerbi_utils.convert_src_code_to_pbix(
                src_code_folder         = src_code_folder,
                pbix_filepath           = pbix_filepath,
                tmp_folder              = tmp_folder,
                powerapps_id_by_name    = component_config.powerapps_id_by_name,
                page_visibility_actions = component_config.page_visibility_actions,
                version                 = project_config.version.resulting_version,
            )

            # deploy report
            log.info(f"Deploying report '{upload_report_name}' to group '{group['name']}'")
            pbi.deploy_report(
                group_id           = group["id"],
                upload_report_name = upload_report_name,
                final_report_name  = component_config.report_name,
                pbix_file_path     = pbix_filepath,
                dataset_parameters = dataset_parameters,
                refresh_schedule   = component_config.refresh_schedule,
                cleanup_regex      = rf"^{re.escape(component_config.report_name)}\W*\d+\.\d+\.\d+.*"
            )

    if deploy_app:
        group_names = sorted(set(component_config.group_name for component_config in component_configs))
        for group_name in group_names:
            group = pbi.get_group_by_name(group_name)
            log_dir = f"{tmp_folder}/deploy_app/logs"
            os.makedirs(log_dir, exist_ok=True)
            if log.isEnabledFor(logging.DEBUG):
                log.debug(f"Deploying app for group '{group_name}' (log_dir={log_dir})")
            else:
                log.info(f"Deploying app for group '{group_name}'")
            pbi.deploy_app(group["id"], log_dir=log_dir)
        log.info("All apps deployed")

    pbi.close_browser()
    log.info("Deployment finished")


@powerbi_cli.command(short_help="Retrieve PowerBI components from the cloud")
def retrieve(
    ctx: typer.Context,
    stage : Annotated[str, typer.Option(
        show_default=False,
        help="The cloud stage to use. this env designation will be used as suffix to find the project and component configuration files"
    )],
    components: Annotated[list[str], typer.Argument(
        help="The component(s) to retrieve"
    )] = None,
):
    cli_ctx: CliCtx = ctx.obj
    project_config = cli_ctx.project_config
    tmp_folder = get_tmp_dir(project_config.project_dir, "retrieve")

    if components is None:
        component_configs = project_config.get_component_configs_by_type("powerbi", stage=stage)
        components = [c.name for c in component_configs]
        msg = f"Do you want to retrieve all powerbi components ({', '.join(components)})? (y/n)"
        if not typer.confirm(msg):
            return
    else:
        component_configs = [project_config.get_component_config(component_name, stage=stage) for component_name in components]

    pbi = cli_ctx.get_pbi_client()
    pbi.login_for_powerbi_api()

    component_config: PowerBiComponentConfig
    for component_config in component_configs:
        pbi.retrieve_report(
            component_config.group_name,
            component_config.report_name, 
            f"{component_config.component_root}/src", 
            tmp_folder
        )


@powerbi_cli.command("import", short_help="Import PowerBI components from pbix file to src code")
def import_from_pbix(
    ctx: typer.Context,
    pbix_file: Annotated[str, typer.Option(...,
        help="The pbix file to import from"
    )],
    component: Annotated[str, typer.Argument(...,
        help="The component to import to"
    )],
):
    cli_ctx: CliCtx = ctx.obj
    project_config   = cli_ctx.project_config
    component_raw_config = project_config.component_raw_configs_by_name[component]
    component_dir        = f"{project_config.project_dir}/{component_raw_config['relative_dir']}"
    src_code_folder      = f"{component_dir}/src"
    tmp_folder           = get_tmp_dir(project_config.project_dir, "import_from_pbix")
    powerbi_utils.convert_pbix_to_src_code(pbix_file, src_code_folder, tmp_folder)


@powerbi_cli.command("export", short_help="Export PowerBI components from src code to pbix file")
def export_to_pbix(
    ctx: typer.Context,
    stage : Annotated[str, typer.Option(
        show_default=False,
        help="The cloud stage to use. this env designation will be used as suffix to find the project and component configuration files"
    )],
    pbix_file: Annotated[str, typer.Option(...,
        help="The pbix file to export to"
    )],
    component: Annotated[str, typer.Argument(...,
        help="The component to import to"
    )],
):    
    cli_ctx: CliCtx  = ctx.obj
    project_config   = cli_ctx.project_config
    component_config = project_config.get_component_config(component, stage=stage)
    src_code_folder  = f"{component_config.component_root}/src"
    tmp_folder       = get_tmp_dir(project_config.project_dir, "export_to_pbix")

    powerbi_utils.convert_src_code_to_pbix(
        src_code_folder         = src_code_folder,
        pbix_filepath           = pbix_file,
        tmp_folder              = tmp_folder,
        powerapps_id_by_name    = component_config.powerapps_id_by_name,
        page_visibility_actions = component_config.page_visibility_actions,
        version                 = project_config.version.resulting_version
    )


if __name__ == '__main__':
    try:
        main_cli()
    except typer.BadParameter as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
