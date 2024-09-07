import logging
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import Field, PrivateAttr
from typing_extensions import Annotated

log = logging.getLogger(__name__)


class ProjectVersion(BaseModel):
    major               : Annotated[int, Field(description="The major version of the project")]
    minor               : Annotated[int, Field(description="The minor version of the project")]
    build_ground        : Annotated[int, Field(description="The ground number to subtract from the total amount of commits to calculate the build number")]
    _resulting_version  : Annotated[str, PrivateAttr()] = None
    
    @property
    def resulting_version(self):
        return self._resulting_version

    @resulting_version.setter
    def resulting_version(self, value):
        self._resulting_version = value


class ComponentConfig(BaseModel):
    # discriminator used by pydantic to determine the type of the component at deserialization
    type                : Annotated[Literal[None]   , Field(description="The type of the component")] = None
    name                : Annotated[str             , Field(description="The name of the component", pattern=r"^[a-zA-Z0-9_\-\.]+$")]
    depends_on          : Annotated[List[str]       , Field(default_factory=list, description="The components this component depends on")]
    # noinspection PyUnresolvedReferences
    _parent_project     : Annotated["ProjectConfig" , PrivateAttr()] = None
    _relative_dir       : Annotated[str             , PrivateAttr()] = None

    @property
    def parent_project(self):
        return self._parent_project
    
    @parent_project.setter
    def parent_project(self, value):
        self._parent_project = value
    
    @property
    def relative_dir(self):
        return self._relative_dir
    
    @relative_dir.setter
    def relative_dir(self, value):
        self._relative_dir = value
        
    @property
    def component_root(self):
        # noinspection PyProtectedMember
        return f"{self._parent_project._project_dir}/{self._relative_dir}"
