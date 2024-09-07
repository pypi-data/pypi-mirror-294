import copy
import glob
import logging
import os
from typing import Union, Annotated, List, Any

import yaml
from pydantic import Tag, BaseModel, Discriminator, Field, PrivateAttr

from powercicd.json_utils import apply_switches
from powercicd.powerapps.config import PowerAppsComponentConfig
from powercicd.powerbi.config import PowerBiComponentConfig
from powercicd.powerbi.file_utils import find_parent_dir_where_exists_file
from powercicd.shared.config import ProjectVersion, ComponentConfig
from powercicd.sharepoint.config import SharepointComponentConfig

log = logging.getLogger("powercicd.config")

AnyComponent = Union[
    Annotated[PowerBiComponentConfig   , Tag('powerbi'   )],
    Annotated[PowerAppsComponentConfig , Tag('powerapps' )],
    Annotated[SharepointComponentConfig, Tag('sharepoint')],
]


PROJECT_CONFIG_FILENAME   : str = "power-project.yaml"
COMPONENT_CONFIG_FILENAME : str = "power-component.yaml"


def get_discriminator_value(values: dict):
    """ Custom discriminator function to handle both single and list components dynamically """
    if isinstance(values, list):
        return "listComponent"
    else:
        return values["type"]


class RawComponentDeserializer(BaseModel):
    component: Annotated[
        Union[
            AnyComponent,
            Annotated[List[AnyComponent], Tag('listComponent')]
        ],
        Discriminator(get_discriminator_value)
    ]

    @classmethod
    def deserialize_raw_component(cls, component_raw_config: Any, stage: str) -> AnyComponent:
        component_config_json = apply_switches(component_raw_config, {"stage": stage})
        containing_config_json = {"component": component_config_json}
        validated_component = cls.model_validate(containing_config_json).component
        return validated_component


class ProjectConfig(BaseModel):
    tenant: Annotated[str, Field(description="The tenant of the project. Either the tenant ID or the tenant name (i.e. abc.onmicrosoft.com). Environment variables are supported in the format '{ENV_VAR_NAME}'")]
    version: Annotated[ProjectVersion, Field(description="The version of the project")]
    stages: Annotated[List[str], Field(description="The stages of the project")]
    _project_dir: Annotated[str, PrivateAttr()] = None
    _component_raw_configs: Annotated[List[ComponentConfig], PrivateAttr(default_factory=list)]
    _component_raw_configs_by_name: Annotated[dict[str, ComponentConfig], PrivateAttr()] = None

    @property
    def project_dir(self):
        return self._project_dir

    @project_dir.setter
    def project_dir(self, value):
        self._project_dir = value

    @property
    def component_raw_configs(self):
        return self._component_raw_configs

    @component_raw_configs.setter
    def component_raw_configs(self, value):
        self._component_raw_configs = value

    @property
    def component_raw_configs_by_name(self):
        if self._component_raw_configs_by_name is None:
            self._component_raw_configs_by_name = {c["name"]: c for c in self._component_raw_configs}
        return self._component_raw_configs_by_name

    def get_component_raw_configs_by_type(self, typ: str):
        return [c for c in self._component_raw_configs if c["type"] == typ]

    def get_component_config(self, name: str, stage: str):
        if stage not in self.stages:
            raise ValueError(f"Stage '{stage}' not found in the project configuration. Available stages: {self.stages}")

        raw_component = self.component_raw_configs_by_name.get(name, None)
        if raw_component is None:
            raise ValueError(
                f"Component '{name}' not found in the project configuration. Available components: {list(self.component_raw_configs_by_name.keys())}")

        raw_component = copy.deepcopy(raw_component)
        relative_dir = raw_component.pop("relative_dir")
        component = RawComponentDeserializer.deserialize_raw_component(raw_component, stage=stage)
        component.parent_project = self
        component.relative_dir = relative_dir
        return component

    def get_component_configs_by_type(self, typ: str, stage: str):
        return [self.get_component_config(c["name"], stage) for c in self.get_component_raw_configs_by_type(typ)]


def get_current_version(project_dir: str, project_config: ProjectConfig):
    major_version = project_config.version.major
    minor_version = project_config.version.minor
    build_ground = project_config.version.build_ground

    # Case 1: project folder is outside git work tree
    cmd = f"git -C {project_dir} rev-parse --is-inside-work-tree"
    log.debug(f"Executing command: {cmd}")
    response = os.popen(cmd).read()
    log.debug(f"Response: '{response}'")
    if response.strip() != "true":
        log.info(
            f"Project folder is outside git work tree, then keep version '{major_version}.{minor_version}.{build_ground}' unchanged")
        return f"{major_version}.{minor_version}.{build_ground}"

    # Case 2: project folder is inside git work tree but no commits at all (not even HEAD)
    cmd = f"git -C {project_dir} rev-list --all"
    log.debug(f"Executing command: {cmd}")
    response = os.popen(cmd).read()
    log.debug(f"Response: '{response}'")
    if response.strip() == "":
        log.info(
            f"No commits found in '{project_dir}', then keep version '{major_version}.{minor_version}.{build_ground}' unchanged")
        return f"{major_version}.{minor_version}.{build_ground}"

    # Case 3: project folder is inside git work tree and there are commits
    cmd = f"git -C {project_dir} rev-list HEAD --count"
    log.debug(f"Executing command: {cmd}")
    response = os.popen(cmd).read()
    log.debug(f"Response: '{response}'")
    count_commits = int(response.strip())
    build_number = count_commits - build_ground

    cmd = f"git -C {project_dir} status --porcelain"
    log.debug(f"Executing command: {cmd}")
    response = os.popen(cmd).read()
    log.debug(f"Response: '{response}'")
    modified_flag = "M" if response.strip() != "" else ""
    version = f"{major_version}.{minor_version}.{build_number}{modified_flag}"
    log.info(f"Computed version: {version}")
    return version


def get_project_config(lookup_path: str | None = None) -> ProjectConfig:
    if lookup_path is None:
        lookup_path = os.getcwd()

    # Determine project root and project_config.json
    project_dir = find_parent_dir_where_exists_file(lookup_path, PROJECT_CONFIG_FILENAME)
    log.info(f"Project root: {project_dir}")

    # Load project_config.json
    with open(os.path.join(project_dir, PROJECT_CONFIG_FILENAME), 'r', encoding='utf-8') as f:
        project_json_config = yaml.safe_load(f)

    project_config = ProjectConfig(**project_json_config)
    # support environment variables in tenant
    project_config.tenant = project_config.tenant.format(**os.environ)
    
    # Enrich project_config
    project_config._project_dir = project_dir
    project_config.version.resulting_version = get_current_version(project_dir, project_config)

    # load component configs
    project_config._component_raw_configs = []
    component_config_files = [f for f in glob.glob(f"{project_dir}/*/{COMPONENT_CONFIG_FILENAME}")]

    if len(component_config_files) == 0:
        raise FileNotFoundError(f"No '{COMPONENT_CONFIG_FILENAME}' files found in '{project_dir}'")

    raw_components = []
    for component_config_file in component_config_files:
        relative_dir = os.path.basename(os.path.dirname(component_config_file))

        log.info(f"Reading raw component config(s) from '{component_config_file}'")
        with open(component_config_file, 'r', encoding='utf-8') as f:
            raw_configs = list(yaml.safe_load_all(f))
        if not isinstance(raw_configs, list):
            raw_configs = list(raw_configs)

        # enrich with relative_dir
        for raw_config in raw_configs:
            raw_config["relative_dir"] = relative_dir

        raw_components.extend(raw_configs)

    project_config.component_raw_configs = raw_components

    return project_config
