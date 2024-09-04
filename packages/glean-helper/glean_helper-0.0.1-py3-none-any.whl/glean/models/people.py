from typing import Optional, List, Union, Any, Dict
from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl, Field, ConfigDict, field_validator
from zoneinfo import ZoneInfo
from .base import GleanModel
from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4
from uuid_extensions import uuid7
from datetime import datetime

def generate_upload_id() -> str:
    return str(uuid7())

class EmployeeType(str, Enum):
    FULL_TIME = "FULL_TIME"
    CONTRACTOR = "CONTRACTOR"
    NON_EMPLOYEE = "NON_EMPLOYEE"
    FORMER_EMPLOYEE = "FORMER_EMPLOYEE"

class EmployeeStatus(str, Enum):
    CURRENT = "CURRENT"
    FUTURE = "FUTURE"
    FORMER = "EX"

class EmployeeRelationshipType(str, Enum):
    CHIEF_OF_STAFF = "CHIEF_OF_STAFF"
    EXECUTIVE_ASSISTANT = "EXECUTIVE_ASSISTANT"

class TeamMemberRole(str, Enum):
    MEMBER = "MEMBER"
    MANAGER = "MANAGER"
    LEAD = "LEAD"
    CONTACT = "POINT_OF_CONTACT"
    OTHER = "OTHER"

class TeamEmailType(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    ONCALL = "ONCALL"
    OTHER = "OTHER"

class DatasourceProfile(GleanModel):
    """
    Represents a profile on an external datasource.

    This model contains information about a user's profile on an external datasource, 
    including the name of the datasource, the user's handle on that datasource, 
    and the URL to the user's profile.

    Links to: Employee model, Team model
    """

    datasource: str = Field(description="Name of the datasource this profile is for.", examples=["github"])
    handle: str = Field(description="The display name of the datasource as it will appear in the user's/team's profile.", examples=["GitHub"])
    url: Optional[HttpUrl] = Field(default=None, description="URL to the profile on the datasource.", examples=["https://github.com/janedoe"])
    nativeAppUrl: Optional[str] = Field(default=None, description="A deep link URL (if available) to the profile in the native app.", examples=["github://user/janedoe"])
    isUserGenerated: bool = Field(default=False, description="[Internal Use Only] True if the profile was manually added by a user in the Glean UI.", exclude=True)

class TeamMember(GleanModel):
    """
    Represents a member of a team.
    
    This model contains information about a team member, including their email,
    role in the team, and the date they joined the team.

    Links to: Team model
    """

    email: EmailStr = Field(description="Email address of the user in the team.", examples=["jane.doe@example.com"])
    relationship: TeamMemberRole = Field(default=TeamMemberRole.MEMBER, description="Role or relationship of the team member to the team.")
    join_date: Optional[date] = Field(default=None, description="Date when the team member joined the team (YYYY-MM-DD)", examples=["2023-08-01"])

    @field_validator('join_date', mode='before')
    @classmethod
    def parse_join_date(cls, value):
        if isinstance(value, str):
            try:
                # Try parsing as simple YYYY-MM-DD first
                return date.fromisoformat(value)
            except ValueError:
                try:
                    # If that fails, try parsing as a full ISO 8601 datetime
                    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    # Convert to UTC and return only the date part
                    return dt.astimezone(ZoneInfo("UTC")).date()
                except ValueError:
                    raise ValueError("Invalid date format. Use YYYY-MM-DD or a valid ISO 8601 datetime.")
        return value

class TeamEmail(GleanModel):
    """
    Represents an email address for a team.

    This model contains information about an email address for a team, including its
    type (e.g., primary, secondary, on-call) and the email address itself.

    Links to: Team model
    """

    email: EmailStr = Field(description="Email address of the team.", examples=["team-oncall@example.com"])
    type: TeamEmailType = Field(default=TeamEmailType.OTHER, description="Type of email address.", examples=["PRIMARY", "SECONDARY", "ONCALL", "OTHER"])

class TeamBase(GleanModel):
    """
    Represents a base model for a Team within an organization.
    The fields included here are the same across both the Indexing API (pushing team info) and Client API (fetching team info).
    
    This model contains information about a team, including its name, description,
    business unit, department, and list of team members.
    """

    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the team.")
    name: str = Field(description="Name of the team.", examples=["Product Development Team"])
    emails: List[TeamEmail] = Field(default_factory=list, description="List of email addresses for the team.")
    description: Optional[str] = Field(default=None, description="Description of the team.", examples=["Core team responsible for product development and innovation"])
    businessUnit: Optional[str] = Field(default=None, description="Business unit the team belongs to.", examples=["Product"])
    department: Optional[str] = Field(default=None, description="Department or division the team belongs to.", examples=["Engineering"])
    photoUrl: Optional[HttpUrl] = Field(default=None, description="URL to the team's logo or photo.", examples=["https://example.com/team-photo.jpg"])
    externalLink: Optional[HttpUrl] = Field(default=None, description="URL to the team's page or resources.", examples=["https://example.com/teams/product-dev"])
    datasourceProfiles: List[DatasourceProfile] = Field(default_factory=list, description="List of application profiles to display in the team's profile, e.g., GitHub, Slack.")
    
class Team(TeamBase):
    """
    Represents a team within an organization.
    
    This model contains information about a team, including its name, description,
    business unit, department, and list of team members.
    """

    #bannerPhotoUrl: Optional[HttpUrl] = Field(default=None, description="URL to the team's banner image.", examples=["https://example.com/team-banner.jpg"])
    # TODO: For bulk upload, either members OR an externalLink must be populated. If neither, error is {Team has no members and no external link=[<team_id>]}. Add custom validation.
    members: List[TeamMember] = Field(default_factory=list, description="List of the members of the team.")

class StructuredLocation(GleanModel):
    """
    Represents a structured location for an employee.

    This model contains structured information about an employee's work location, such as their work address.

    Links to: Employee model
    """

    address: Optional[str] = Field(default=None, description="Full address of the employee's work location, or the office name.", examples=["123 Tech Street", "San Fran HQ"], alias="desk_location")
    city: Optional[str] = Field(default=None, description="City of the employee's work location.", examples=["San Francisco"])
    state: Optional[str] = Field(default=None, description="State or province of the employee's work location.", examples=["California"])
    country: Optional[str] = Field(default=None, description="Country of the employee's work location.", examples=["United States"])
    region: Optional[str] = Field(default=None, description="Broader region of the employee's work location, e.g., APAC, EMEA, AMER.", examples=["APAC", "EMEA"])
    zipCode: Optional[str] = Field(default=None, description="Postal or ZIP code of the work location.", examples=["94105"], alias="zip_code")
    timezone: Optional[str] = Field(default=None, description="Time zone of the work location.", examples=["America/Los_Angeles"])
    deskLocation: Optional[str] = Field(default=None, description="Specific desk or office location.", examples=["Building A, Floor 3, Desk 42"], alias="desk_location")
    countryCode: Optional[str] = Field(default=None, description="Alpha-2 or Alpha-3 ISO 3166 country code, e.g., US or USA.", examples=["US", "USA"], alias="country_code")

class SocialNetwork(GleanModel):
    """
    Represents a social network profile for an employee.

    This model contains information about a user's profile on a social network, including the name of the social network,
    the user's profile name on that network, and the URL to the user's profile.

    Links to: Employee model
    """

    name: str = Field(description="Name of the social network.", examples=["linkedin"])
    profileName: Optional[str] = Field(default=None, description="Human-readable profile name to appear in the user's Glean profile.", examples=["LinkedIn"])
    profileUrl: HttpUrl = Field(description="URL to the user's profile on the social network.", examples=["https://linkedin.com/in/janedoe"])

class HyperlinkField(GleanModel):
    """
    Represents a hyperlink field for an employee profile.

    This model contains information about a hyperlink field, including the text to display as the hyperlink anchor.
    
    Links to: AdditionalField model
    """

    anchor: str = Field(description="Text to display as the hyperlink anchor.", examples=["Workday"])
    hyperlink: HttpUrl = Field(description="URL to link to.", examples=["https://workday.com/janedoe"])

class AdditionalField(GleanModel):
    """
    Represents an additional field for an employee profile, outside of the standard fields to be indexed.

    This model contains information about an additional field, including the key (name of the field) and the value.
    It is used to provide additional information about an employee, such as languages spoken, certifications, etc.

    Links to: Employee model
    """
    
    key: str = Field(description="Name of the additional field.", examples=["languages", "certifications"])
    value: List[Union[str, HyperlinkField]] = Field(description="Either a list of string values or a list of dictionaries containing an anchor value and hyperlink value (for display in a profile).", examples=[["English", "Japanese"], [{"anchor": "BambooHR", "hyperlink": "https://example.bamboohr.com/profile"}]])

class EmployeeTeamInfo(GleanModel):
    """
    Represents information about an employee's team affiliation.

    This model contains information about an employee's team affiliation, including the team's name, ID, and URL.

    Links to: Employee model
    """
    id: Optional[str] = Field(default=None, description="Unique identifier for the team.", examples=["organization-team-id-315"])
    name: Optional[str] = Field(default=None, description="Name of the team.", examples=["APAC Sales Team"])
    url: Optional[HttpUrl] = Field(default=None, description="URL to the team's page or resources.", examples=["https://example.com/teams/organization-team-id-315"])

class EmployeeRelationship(GleanModel):
    """
    Represents a unidirectional relationship between employees.

    This model contains information about a unidirectional relationship between employees, including the type of relationship,
    and the email of the employee with whom the relationship exists.

    Links to: Employee model
    """
    name: EmployeeRelationshipType = Field(description="Type of unidirectional relationship the employee has with another employee. E.g., This employee is another employee's executive assistant.", examples=["EXECUTIVE_ASSISTANT", "CHIEF_OF_STAFF"])
    email: EmailStr = Field(description="Email of the employee with whom the unidirectional relationship exists.", examples=["ceoemail@example.com"])

class EmployeeBase(GleanModel):
    """
    Represents a base model for an employee within an organization.
    The fields included here are the same across both the Indexing API (pushing employee info) and Client API (fetching employee info).

    This model contains basic information about an employee, including their email, first name, last name, and department.
    """
    email: EmailStr = Field(description="Employee's work email address.", examples=["john.doe@example.com"])
    firstName: str = Field(description="Employee's first name.", examples=["John"], alias="first_name")
    lastName: str = Field(default="", description="Employee's last name.", examples=["Doe"], alias="last_name")
    department: str = Field(description="Department the employee works in.", examples=["Engineering"])
    pronoun: Optional[str] = Field(default=None, description="Employee's preferred pronouns.", examples=["he/him"])
    preferredName: Optional[str] = Field(default=None, description="Employee's preferred name or nickname.", examples=["Johnny"], alias="preferred_name")
    title: Optional[str] = Field(default=None, description="Employee's job title.", examples=["Senior Software Engineer"])
    businessUnit: Optional[str] = Field(default=None, description="Business unit the employee belongs to.", examples=["Product Development"], alias="business_unit")
    startDate: Optional[date] = Field(default=None, description="Date when the employee started working.", examples=["2020-01-01"], alias="start_date")
    endDate: Optional[date] = Field(default=None, description="Date when the employee stopped working, if applicable.", examples=["2025-12-31"], alias="end_date")
    bio: Optional[str] = Field(default=None, description="Short biography or description of the employee.", examples=["Experienced software engineer with a passion for AI"])
    type: EmployeeType = Field(default=EmployeeType.FULL_TIME, description="The type of employee.", examples=["FULL_TIME", "CONTRACTOR", "NON_EMPLOYEE"])
    location: Optional[str] = Field(default=None, description="Location of the employee's work, e.g., city, office.", examples=["San Francisco HQ"], deprecated="This field is deprecated, use structuredLocation instead.")
    photoUrl: Optional[HttpUrl] = Field(default=None, description="URL to the employee's profile photo.", examples=["https://example.com/john-doe-photo.jpg"], alias="photo_url")
    structuredLocation: Optional[StructuredLocation] = Field(default=None, description="Structured representation of the employee's work location.")

    @field_validator('startDate' or 'endDate', mode='before')
    @classmethod
    def parse_join_date(cls, value):
        if isinstance(value, str):
            try:
                # Try parsing as simple YYYY-MM-DD first
                return date.fromisoformat(value)
            except ValueError:
                try:
                    # If that fails, try parsing as a full ISO 8601 datetime
                    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    # Convert to UTC and return only the date part
                    return dt.astimezone(ZoneInfo("UTC")).date()
                except ValueError:
                    raise ValueError("Invalid date format. Use YYYY-MM-DD or a valid ISO 8601 datetime.")
        return value

class Employee(EmployeeBase):
    """
    Represents an employee within an organization.
    
    This model contains comprehensive information about an employee, including
    personal details, job information, contact details, and team affiliations.
    """
    id: Optional[str] = Field(default=None, description="Unique identifier for the employee.", examples=["EMP12345"])
    alsoKnownAs: Optional[List[str]] = Field(default_factory=list, description="List of other names the employee is (or has been) known by.", examples=[["JD", "Johnny", "Steve Smith"]], alias="also_known_as")
    managerEmail: Optional[EmailStr] = Field(default=None, description="Email of the employee's direct manager.", examples=["manager@example.com"], alias="manager_email")
    managerId: Optional[str] = Field(default=None, description="Employee ID of the employee's direct manager. Should map to the id field.", examples=["EMP54321"], alias="manager_id")
    phoneNumber: Optional[str] = Field(default=None, description="Employee's work phone number.", examples=["+1 (555) 123-4567"], alias="phone_number")
    profileUrl: Optional[HttpUrl] = Field(default=None, description="URL to the employee's profile page, if available.", examples=["https://example.com/employees/john-doe"], alias="external_profile_link")
    status: EmployeeStatus = Field(default=EmployeeStatus.CURRENT, description="Current status of the employee.", examples=["CURRENT", "FUTURE", "EX"])
    bannerUrl: Optional[HttpUrl] = Field(default=None, description="URL to the employee's banner image on their profile page.", examples=["https://example.com/john-doe-banner.jpg"], alias="banner_photo_url", exclude=True)
    datasourceProfiles: List[DatasourceProfile] = Field(default_factory=list, description="List of application profiles to display in the user's profile if Glean is not connected to them, e.g., Slack, GitHub.")
    relationships: List[EmployeeRelationship] = Field(default_factory=list, description="List of unidirectional relationships this employee has with other employees. E.g., 'Executive Assistant' to ceoname@example.com")
    additionalFields: List[AdditionalField] = Field(default_factory=list, description="Additional fields with more information about the employee. E.g., languages, certifications, etc.")
    socialNetworks: List[SocialNetwork] = Field(default_factory=list, description="List of social network profiles to display in the user's profile.")
    teams: List[EmployeeTeamInfo] = Field(default_factory=list, description="List of teams the employee belongs to.")

    @classmethod
    def fix_missing_fields(cls, data: dict) -> dict:
        # Create a mapping of aliases to field names
        alias_to_field = {field.alias: field_name for field_name, field in cls.model_fields.items() if field.alias}

        # Handle structuredLocation
        location_fields = {'address', 'city', 'country', 'state', 'region', 'zipCode', 'timezone', 'deskLocation', 'countryCode'}
        if 'structuredLocation' not in data and any(field in data for field in location_fields):
            location_data = {field: data.pop(field) for field in location_fields if field in data}
            if location_data:
                data['structuredLocation'] = location_data

        # Handle social networks
        if 'socialNetworks' not in data:
            social_networks = []
            fields_to_remove = []
            for key, value in data.items():
                if key.endswith('_url') and not any(field.alias == key for field in cls.model_fields.values()):
                    network_name = key[:-4]  # Remove '_url' from the end
                    social_networks.append({
                        "name": network_name,
                        "profileName": network_name.capitalize(),
                        "profileUrl": value
                    })
                    fields_to_remove.append(key)
            
            for key in fields_to_remove:
                data.pop(key)
            
            if social_networks:
                data['socialNetworks'] = social_networks

        # Handle additional fields and aliases
        known_fields = set(cls.model_fields.keys())
        additional_fields = []
        for key, value in list(data.items()):
            if key in alias_to_field:
                # If the key is an alias, update the data with the actual field name
                actual_field_name = alias_to_field[key]
                data[actual_field_name] = value
                data.pop(key)
            elif key not in known_fields:
                additional_fields.append({
                    "key": key,
                    "value": [value] if isinstance(value, (str, dict)) else value
                })
                data.pop(key)
        
        if additional_fields:
            if 'additionalFields' in data:
                data['additionalFields'].extend(additional_fields)
            else:
                data['additionalFields'] = additional_fields

        return data

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "id": "EMP12345",
                "email": "john.doe@example.com",
                "firstName": "John",
                "lastName": "Doe",
                "title": "Senior Software Engineer",
                "department": "Engineering",
                "businessUnit": "Product Development",
                "type": "FULL_TIME",
                "startDate": "2020-01-01",
                "status": "CURRENT"
            }]
        }
    )

class IndexEmployee(GleanModel):
    """
    Represents an employee to be indexed in Glean.

    This model is used to validate and serialize an employee's data in the format expected by the Glean Indexing API.
    """
    employee: Employee = Field(description="Employee data to be indexed in Glean.")
    version: Optional[int] = Field(default=0, description="Version number of the employee profile. If absent or 0, then no version checks are done when pushing data.", examples=[0, 1, 2])

class IndexEmployees(GleanModel):
    """
    Represents a bulk index request for employees in Glean.

    This model is used to validate and serialize a bulk index request for employees in the format expected by the Glean Indexing API.
    """
    uploadId: str = Field(default_factory=generate_upload_id, description="Unique identifier for the bulk index request. Automatically uses UUID7 if nothing is specified.", examples=["066b060d-1bdb-765e-8000-621a4d95146f"], alias="upload_id")
    isFirstPage: bool = Field(default=False, description="True if this is the first page of the bulk index request. Defaults to False.")
    isLastPage: bool = Field(default=False, description="True if this is the last page of the bulk index request. Defaults to False.")
    forceRestartUpload: bool = Field(default=False, description="Flag to discard previous upload attempts and start from scratch. Must be specified with isFirstPage=true. Defaults to False.")
    employees: List[Employee] = Field(description="List of employee data to be indexed in Glean.")
    disableStaleDataDeletionCheck: bool = Field(default=False, description="True if older employee data needs to be force deleted after the upload completes. Defaults to older data being deleted only if the percentage of data being deleted is less than 20%. This must only be set when isLastPage = true.")

class DeleteEmployee(GleanModel):
    """
    Represents an employee to be deleted from Glean.

    This model is used to validate and serialize an employee's data in the format expected by the Glean Indexing API for deletion.
    """
    employeeEmail: EmailStr = Field(description="Email address of the employee to be deleted from Glean.", examples=["sam.sample@example.com"])
    version: int = Field(default=0, description="Version number of the employee profile. If absent or 0, then no version checks are done when deleting data.", examples=[0, 1, 2])

class IndexTeam(GleanModel):
    """
    Represents a team to be indexed in Glean.

    This model is used to validate and serialize a team's data in the format expected by the Glean Indexing API.
    """
    team: Team = Field(description="Team data to be indexed in Glean.")
    version: Optional[int] = Field(default=0, description="Version number of the team profile. If absent or 0, then no version checks are done when pushing data.", examples=[0, 1, 2])

class IndexTeams(GleanModel):
    """
    Represents a bulk index request for teams in Glean.

    This model is used to validate and serialize a bulk index request for teams in the format expected by the Glean Indexing API.
    """
    uploadId: str = Field(default_factory=generate_upload_id, description="Unique identifier for the bulk index request. Automatically uses UUID7 if nothing is specified.", examples=["066b060d-1bdb-765e-8000-621a4d95146f"], alias="upload_id")
    isFirstPage: bool = Field(default=False, description="True if this is the first page of the bulk index request. Defaults to False.")
    isLastPage: bool = Field(default=False, description="True if this is the last page of the bulk index request. Defaults to False.")
    forceRestartUpload: bool = Field(default=False, description="Flag to discard previous upload attempts and start from scratch. Must be specified with isFirstPage=true. Defaults to False.")
    teams: List[Team] = Field(description="List of team data to be indexed in Glean.")

class DeleteTeam(GleanModel):
    """
    Represents a team to be deleted from Glean.

    This model is used to validate and serialize a team's data in the format expected by the Glean Indexing API for deletion.
    """
    id: str = Field(description="Unique identifier for the team to be deleted from Glean.", examples=["team-id-123"])

if __name__ == "__main__":

    import json

    with open('tests/single_user_flatdata.json', 'r') as f:
        data = json.load(f)

    data = Employee.fix_missing_fields(data)

    # TEST: Creating an Employee model instance from JSON data
    employee = Employee(**data)

    from pprint import pprint
    print(employee)

    import sys
    sys.exit(0)
    
    # TEST: Dumping the Employee model with and without alias names
    employee = Employee(id="EMP123", email="john.doe@example.com", first_name="John", last_name="Doe", department="Engineering", title="Senior Developer")

    print("Original field names:")
    print(employee.model_dump())

    print("\nCSV column names (with all fields):")
    print(employee.model_dump(by_alias=True))

    print("\nCSV column names (excluding non-aliased fields):")
    print(employee.model_dump(by_alias=True, exclude_non_aliased=True))
