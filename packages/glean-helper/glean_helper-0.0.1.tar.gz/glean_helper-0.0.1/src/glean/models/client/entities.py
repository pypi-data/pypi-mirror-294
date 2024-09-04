from typing import Optional, List, Union, Any, Dict
from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl, Field, ConfigDict
from ..base import GleanModel
from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4
from uuid_extensions import uuid7
from datetime import datetime
from ..people import EmployeeBase, EmployeeTeamInfo, TeamMemberRole, TeamMember, TeamBase, HyperlinkField, AdditionalField, StructuredLocation, EmployeeType, EmployeeStatus, SocialNetwork, DatasourceProfile
from ...config import get_settings

class EntityType(str, Enum):
    PEOPLE = "PEOPLE"
    TEAMS = "TEAMS"
    CUSTOM_ENTITIES = "CUSTOM_ENTITIES"

class RelationType(str, Enum):
    EQUALS = "EQUALS"
    LT = "LT"
    GT = "GT"

class IncludeField(str, Enum):
    PEOPLE = "PEOPLE"
    TEAMS = "TEAMS"
    PEOPLE_DISTANCE = "PEOPLE_DISTANCE"
    PERMISSIONS = "PERMISSIONS"
    FACETS = "FACETS"
    INVITE_INFO = "INVITE_INFO"
    LAST_EXTENSION_USE = "LAST_EXTENSION_USE"
    MANAGEMENT_DETAILS = "MANAGEMENT_DETAILS"
    UNPROCESSED_TEAMS = "UNPROCESSED_TEAMS"

class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class SortBy(str, Enum):
    ENTITY_NAME = "ENTITY_NAME"
    FIRST_NAME = "FIRST_NAME"
    LAST_NAME = "LAST_NAME"
    ORG_SIZE_COUNT = "ORG_SIZE_COUNT"
    START_DATE = "START_DATE"
    TEAM_SIZE = "TEAM_SIZE"
    RELEVANCE = "RELEVANCE"

class SortOptions(GleanModel):
    orderBy: Optional[SortOrder] = Field(description="The order to sort the results.", examples=["ASC", "DESC"])
    sortBy: Optional[SortBy] = Field(description="The field to sort the results by.", examples=["ENTITY_NAME", "FIRST_NAME", "LAST_NAME", "ORG_SIZE_COUNT", "START_DATE", "TEAM_SIZE", "RELEVANCE"])

class FilterValue(GleanModel):
    relationType: RelationType = Field(description="The type of relation to apply to the filter value.", examples=["EQUALS", "LT", "GT"])
    value: str = Field(description="The value to filter on.", examples=["New York"])

class Filter(GleanModel):
    fieldName: str = Field(description="The name of the field to filter on.", examples=["city"])
    groupName: Optional[str] = Field(description="Indicates the value of a facet, if any, that the given facet is grouped under. This is only used for nested facets, for example, fieldName could be owner and groupName would be Spreadsheet if showing all owners for spreadsheets as a nested facet.")
    values: List[FilterValue] = Field(description="The values to filter on.", examples=[{"relationType": "EQUALS", "value": "New York"}])


class ListEntitiesRequest(GleanModel):
    """
    Represents the required information to fetch from the Glean Client API to list all entities (people).

    https://developers.glean.com/client/operation/listentities/
    """
    cursor: Optional[str] = Field(default=None, description="Pagination record counter. A previously received opaque token representing the position in the overall results at which to start.", examples=["5000"])
    datasource: Optional[str] = Field(default=None, description="The datasource to query for people data. Can be left blank.", examples=["CUSTOM_ENTITIES"])
    entityType: Optional[EntityType] = Field(default=EntityType.PEOPLE, description="The type of entity to list.", examples=["PEOPLE"])
    filter: Optional[List[Filter]] = Field(default_factory=list, description="Filters to apply to the results.", examples=[{"fieldName": "city", "values": [{"relationType": "EQUALS", "value": "New York"}]}])
    includeFields: Optional[List[IncludeField]] = Field(default_factory=list, description="A list of non-default fields to return.", examples=["PEOPLE", "FACETS"])
    pageSize: int = Field(default=get_settings().BATCH_SIZE, description="The number of records to return per page. Must be less than or equal to 10,000.", le=10000, examples=[500])
    query: Optional[str] = Field(default="", description="A query string to search for entities that each entity in the response must conform to. An empty query does not filter any entities.", examples=["John"])
    sort: Optional[List[SortOptions]] = Field(default_factory=list, description="The sort options to apply to the results.", examples=[{"orderBy": "ASC", "sortBy": "START_DATE"}])
    source: Optional[str] = Field(default=None, description="A string denoting the search surface from which the endpoint is called. For logging purposes only. Can be left blank.", examples=["Reporting_Tool"])

    class Config:
        extra = 'ignore'

class HyperlinkField(GleanModel):
    urlAnchor: str = Field(description="The name of the hyperlink, displayable in the UI.", examples=["Workday"], alias="anchor")
    urlLink: HttpUrl = Field(description="The URL of the hyperlink.", examples=["https://workday.com/janedoe"], alias="hyperlink")

class CustomField(GleanModel):
    displayable: bool = Field(default=True, description="Whether the field is displayable in the UI.", examples=[True, False])
    label: str = Field(description="U user-facing label for this custom field.", examples=["Languages", "Certifications"])
    values: List[Union[str, HyperlinkField, "EmployeeResult"]] = Field(default_factory=list, description="The values for this custom field.", examples=[["English", "Spanish"], [{"name": "John Doe", "obfuscatedId": "CF05DF2950A4606D1A5F371EB017CA01"}], [{"urlAnchor": "Workday", "urlLink": "https://workday.com/janedoe"}]])

class EmployeeTeamInfo(EmployeeTeamInfo):
    externalLink: Optional[HttpUrl] = Field(default=None, description="URL to the team's external page, if available.", examples=["https://example.com/teams/engineering"])
    joinDate: Optional[datetime] = Field(default=None, description="The date the employee joined the team.", examples=["2021-01-01T00:00:00Z"], frozen=True)
    relationship: TeamMemberRole = Field(default=TeamMemberRole.MEMBER, description="Role or relationship of the team member to the team.", examples=["MEMBER", "MANAGER", "LEAD", "POINT_OF_CONTACT", "OTHER"])

class Employee(EmployeeBase):
    # TODO: Map these to client fields, these are currently copy/paste from the indexing api.
    aliasEmails: Optional[List[EmailStr]] = Field(default_factory=list, description="Additional email addresses / email identities associated with this user (if any).", examples=[["EMP12345@ext.example.com", "jdoe@subsidiary.com"]])
    # TODO: badges
    bannerUrl: Optional[str] = Field(default=None, description="URL to the employee's banner image on their profile page.", examples=["https://example.com/john-doe-banner.jpg"], alias="banner_photo_url")
    # TODO: busyEvents
    customFields: List[CustomField] = Field(default_factory=list, description="Custom fields for the employee.", examples=[{"displayable": True, "label": "Languages", "values": ["English", "Spanish"]}])
    datasourceProfile: List[DatasourceProfile] = Field(default_factory=list, description="List of application profiles to display in the user's profile if Glean is not connected to them, e.g., Slack, GitHub.")
    departmentCount: Optional[int] = Field(default=None, description="The number of people in this employee's department", examples=[467])
    directReportsCount: Optional[int] = Field(default=None, description="The number of people who report directly to this employee", examples=[5, 0])
    # email: Inherited from EmployeeBase
    # endDate: Inherited from EmployeeBase
    externalProfileLink: Optional[HttpUrl] = Field(default=None, description="URL to the employee's profile page, if available.", examples=["https://example.com/employees/john-doe"], alias="external_profile_link")
    # firstName: Inherited from EmployeeBase
    # TODO: inviteInfo

    isOrgRoot: Optional[bool] = Field(default=None, description="Whether this person is a 'root' node in their organization's hierarchy.", examples=[True, False])
    isSignedUp: Optional[bool] = Field(default=None, description="Whether the user has signed into Glean at least once.", examples=[True, False])
    lastExtensionUse: Optional[datetime] = Field(default=None, description="The last time the user interacted with the Glean browser extension (in ISO 8601 format)", examples=["2021-01-01T00:00:00Z"])
    # lastName: Inherited from EmployeeBase
    # location (deprecated): Inherited from EmployeeBase
    loggingId: Optional[str] = Field(default=None, description="Unique identifier for the employee for scrubbed logging purposes.", examples=["D2EF443F2760FDBAC4A8490ABFD45570"])
    managementChain: Optional[List["EmployeeResult"]] = Field(default_factory=list, description="The chain of reporting in the company as far up as it goes. The last entry is this person's direct manager.")
    manager: Optional["EmployeeResult"] = Field(default=None, description="The employee's direct manager.")
    orgSizeCount: Optional[int] = Field(default=None, description="The total recursive size of the people reporting to this person, or 1", examples=[467, 1])
    # TODO: peopleDistance
    # TODO: permissions
    phone: Optional[str] = Field(default=None, description="Employee's work phone number.", examples=["+1 (555) 123-4567"], alias="phone_number")
    # photoUrl: Inherited from EmployeeBase
    # preferredName: Inherited from EmployeeBase
    # TODO: profileBoolSettings
    # pronoun: Inherited from EmployeeBase
    # TODO: querySuggestions
    reports: Optional[List["EmployeeResult"]] = Field(default_factory=list, description="The people who report directly to this person.")
    socialNetwork: List[SocialNetwork] = Field(default_factory=list, description="List of social network profiles to display in the user's profile.")
    # startDate: Inherited from EmployeeBase
    startDatePercentile: Optional[float] = Field(default=None, description="Percentage of the company that started strictly after this person, 0-100.", examples=[88.16097])
    # structuredLocation: Inherited from EmployeeBase
    teams: List[EmployeeTeamInfo] = Field(default_factory=list, description="List of teams the employee belongs to.")
    timezone: Optional[str] = Field(default=None, description="The timezone of the employee.", examples=["America/Los_Angeles"])
    timezoneOffset: Optional[int] = Field(default=None, description="The timezone offset of the employee in seconds from UTC.", examples=[36000])
    # title: Inherited from EmployeeBase
    # type: Inherited from EmployeeBase
    uneditedPhotoUrl: Optional[HttpUrl] = Field(default=None, description="The original photo URL of the person's avatar before any edits they made are applied.", examples=["https://example.com/john-doe-photo.jpg"], alias="unedited_photo_url")
    
    class Config:
        extra = 'ignore'

class EmployeeResult(GleanModel):
    name: str = Field(..., description="The display name of the employee.", examples=["John Doe"])
    obfuscatedId: str = Field(..., description="The obfuscated ID of the employee. This is used within Glean for logging purposes.", examples=["CF05DF2950A4606D1A5F371EB017CA01"])
    metadata: Employee
    # TODO: relatedDocuments

class TeamStatus(str, Enum):
    PROCESSED = "PROCESSED"
    QUEUED_FOR_CREATION = "QUEUED_FOR_CREATION"
    QUEUED_FOR_DELETION = "QUEUED_FOR_DELETION"

class TeamMember(TeamMember):
    person: EmployeeResult = Field(description="The details of the employee who is a member of the team.")
    customRelationshipStr: Optional[str] = Field(default=None, description="Display name for the employee relationship to the team if relationship is set to OTHER.", examples=["EXECUTIVE_SPONSOR"])

class Team(TeamBase):
    # id: Inherited from TeamBase
    # name: Inherited from TeamBase
    bannerUrl: Optional[HttpUrl] = Field(default=None, description="URL to the team's banner image.", examples=["https://example.com/team-banner.jpg"])
    # businessUnit: Inherited from TeamBase
    canBeDeleted: bool = Field(default=True, description="Whether the team can be deleted from within the UI. Teams synced from CSV or Indexing API cannot. Defaults to True.", examples=[True, False])
    createdFrom: Optional[str] = Field(default=None, description="For teams created from a document, this is set to the document title. Otherwise, None.")
    datasource: Optional[str] = Field(default=None, description="The data source of the team.", examples=["gdrive"])
    # datasourceProfiles: Inherited from TeamBase
    # description: Inherited from TeamBase
    # emails: Inherited from TeamBase
    # externalLink: Inherited from TeamBase
    lastUpdatedAt: Optional[datetime] = Field(default=None, description="The last time the team was updated (in ISO 8601 format).", examples=["2021-01-01T00:00:00Z"])
    loggingId: Optional[str] = Field(default=None, description="Unique identifier for the team for scrubbed logging purposes.", examples=["D2EF443F2760FDBAC4A8490ABFD45570"])
    memberCount: Optional[int] = Field(default=None, description="The number of members in the team and all sub-teams", examples=[5, 0])
    members: List[TeamMember] = Field(default_factory=list, description="Whether this team is fully processed or there are still unprocessed operations that will affect it.", examples=[item.value for item in TeamStatus])
    # TODO: permissions (team permissions)
    # TODO: relatedObjects
    status: TeamStatus = Field(default=TeamStatus.PROCESSED, description="The status of the team.", examples=["PROCESSED", "QUEUED_FOR_CREATION", "QUEUED_FOR_DELETION"])

class ListEntitiesResponse(GleanModel):
    cursor: Optional[str] = Field(default=None, description="Pagination record counter. A previously received opaque token representing the position in the overall results at which to start.", examples=["5000"])
    # TODO: customEntityResults 
    customFacetNames: Optional[List[str]] = Field(default=None, description="A list of Employee attributes that are custom set by deployment.")
    # TODO: facetResults
    hasMoreResults: bool = Field(default=False, description="Indicates whether there are more results available (used along with the cursor field for pagination).", examples=[True])
    results: Optional[List[EmployeeResult]] = Field(default=None, description="The list of employee objects that match the query.", examples=[{"name": "John Doe", "obfuscatedId": "CF05DF2950A4606D1A5F371EB017CA01", "metadata": {}}])
    sortOptions: Optional[List[SortBy]] = Field(default_factory=list, description="The sort options that are supported for this response. Default is an empty list.", examples=[{"orderBy": "ASC", "sortBy": "START_DATE"}])
    teamResults: Optional[List[Team]] = Field(default_factory=list, description="The list of team objects that match the query.", examples=[{"id": "CF05DF2950A4606D1A5F371EB017CA01", "name": "Engineering", "members": []}])
    totalCount: int = Field(description="The total number of results. Used in conjunction with the cursor and hasMoreResults fields for pagination.", examples=[7500])
