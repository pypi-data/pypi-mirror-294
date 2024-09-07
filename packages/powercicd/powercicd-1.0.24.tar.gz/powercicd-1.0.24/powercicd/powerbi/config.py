import logging
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from powercicd.config_utils import VisibilityAction
from powercicd.shared.config import ComponentConfig

_log = logging.getLogger(__name__)

Report = dict
Group = dict
Dataset = dict
Datasource = dict
WeekDays = Literal["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
NotifyOption = Literal["MailOnFailure", "NoNotification"]


class DatasetRefreshSchedule(BaseModel):
    enabled         : Annotated[bool           , Field(description="Whether the refresh schedule is enabled")]
    localTimeZoneId : Annotated[str            , Field(description="The local time zone ID", examples=["UTC", "Romance Standard Time"])]
    days            : Annotated[List[WeekDays] , Field(description="The days of the week when the refresh should occur")]
    times           : Annotated[List[str]      , Field(description="The times of the day when the refresh should occur", examples=["00:00", "12:00"])]
    NotifyOption    : Annotated[NotifyOption   , Field(description="The notification option")]


class PowerBiComponentConfig(ComponentConfig):
    type                    : Annotated[Literal["powerbi"]               , Field(description="The type of the component")] = "powerbi"
    group_name              : Annotated[str                              , Field(description="The name of the powerbi group/workspace")]
    report_name             : Annotated[str                              , Field(description="The name of the report")]
    refresh_schedule        : Annotated[Optional[DatasetRefreshSchedule] , Field(default=None, description="The schedule for the dataset refresh")]
    dataset_parameters      : Annotated[dict[str, Any]                   , Field(default_factory=lambda: {}, description="The parameters for the dataset refresh")]
    version_parameter_name  : Annotated[str                              , Field(default="DATASET VERSION", description="The name of the version parameter defined in the PBIX file that needs to be set during the build process")]
    powerapps_id_by_name    : Annotated[dict[str, str]                   , Field(default={}, description="The PowerApps ID by powerapps name")]
    page_visibility_actions : Annotated[list[dict[VisibilityAction, str]], Field(default_factory=lambda: [], description="list of '{action: pattern}' dict to change visibility of pages. The action of the first matching pattern will be applied. example: [{'show': 'Sales*'}, {'hide': 'Marketing*'}]. Matching syntax is fnmatch.fnmatch")]

