from pydantic import BaseModel, EmailStr, HttpUrl, Field, ConfigDict
from typing import Optional, List, Union
from enum import Enum
from datetime import datetime
from .base import GleanModel
from .people import Employee as IndexAPIEmployee, AdditionalField, EmployeeTeamInfo, TeamMemberRole
from .client.entities import ListEntitiesResponse, EmployeeResult, Employee as ClientAPIEmployee

class EmployeeMetadata(GleanModel):
    gleanUserId: Optional[str] = Field(default=None, description="Glean's unique identifier for the employee.", examples=["CF05DF2950A4606D1A5F371EB017CA01"], frozen=True)
    gleanLoggingId: Optional[str] = Field(default=None, description="Glean's unique logging identifier for the employee.", examples=["D2EF443F2760FDBAC4A8490ABFD45570"], frozen=True)
    isSignedUp: Optional[bool] = Field(default=None, description="Whether the employee has logged into Glean at least once.", examples=[True, False], frozen=True)

class EmployeeTeamInfo(GleanModel):
    id: Optional[str] = Field(default=None, description="Unique identifier for the team.", examples=["organization-team-id-315"])
    name: Optional[str] = Field(default=None, description="Name of the team.", examples=["APAC Sales Team"])
    externalUrl: Optional[HttpUrl] = Field(default=None, description="URL to the team's page or resources.", examples=["https://example.com/teams/organization-team-id-315"], alias="external_url")
    joinDate: Optional[datetime] = Field(default=None, description="The date the employee joined the team.", examples=["2021-01-01T00:00:00Z"])
    relationship: TeamMemberRole = Field(default=TeamMemberRole.MEMBER, description="Role or relationship of the team member to the team.", examples=["MEMBER", "MANAGER", "LEAD", "POINT_OF_CONTACT", "OTHER"])

class Employee(IndexAPIEmployee):
    """
    Represents an employee's information as fetched from Glean.
    Inherits from the Employee model in the people module; used to serialize employee data for upload to Glean.

    This model is used to serialize an employee's data in a format more inline with the Indexing API than what is returned from the Client API.
    """
    displayName: Optional[str] = Field(default=None, description="The employee's full name.", examples=["John Doe"], alias="name")
    emailAliases: Optional[List[EmailStr]] = Field(default_factory=list, description="A list of alternative email addresses associated with the employee.", examples=[["EMP12345@ext.example.com", "jdoe@subsidiary.com"]], frozen=True)
    bannerPhotoUrl: Optional[str] = Field(default=None, description="URL to the employee's banner image on their profile page.", examples=["https://example.com/john-doe-banner.jpg"], alias="banner_photo_url")
    metadata: Optional[EmployeeMetadata] = Field(default=None, description="Additional metadata about the employee, such as ", examples=[{"lastExtensionUse": "2021-01-01T00:00:00Z", "signUpTime": "2021-01-01T00:00:00Z", "inviteTime": "2021-01-01T00:00:00Z", "gleanLoggingId": "D2EF443F2760FDBAC4A8490ABFD45570"}], frozen=True)
    teams: Optional[List[EmployeeTeamInfo]] = Field(default=None, description="A list of teams the employee is a member of.", examples=[{"id": "organization-team-id-315", "name": "APAC Sales Team", "externalUrl": "https://example.com/teams/organization-team-id-315", "joinDate": "2021-01-01T00:00:00Z", "relationship": "MEMBER"}])

    @classmethod
    def from_client_api(cls, data: Union[dict, EmployeeResult]) -> 'Employee':
        """
        Employee data directly fetched from the Glean Client API into an Employee object that is easier to parse.
        """
        # Check all possible data types and map all fields included inherited ones:
        if isinstance(data, dict):
            client_api_data = EmployeeResult.model_validate(data)  # Will raise pydantic.ValidationError if data is invalid

        elif isinstance(data, EmployeeResult):
            client_api_data = data

        else:
            raise ValueError(f"Invalid data type: {type(data)}")

        # Process additional fields
        additionalFields = []
        if client_api_data.metadata.customFields:
            for field in client_api_data.metadata.customFields:
                additionalFields.append(
                    AdditionalField(
                        key = field.label,
                        value = field.values
                    )
                )

        # Process teams
        teams = []
        if client_api_data.metadata.teams:
            for team in client_api_data.metadata.teams:
                teams.append(
                    EmployeeTeamInfo(
                        id = team.id,
                        name = team.name,
                        joinDate = team.joinDate,
                        externalUrl= team.externalLink,
                        relationship = team.relationship
                    )
                )

        # Map client API response fields to Employee model fields. None if the field is not present.
        employee = cls(
            emailAliases = client_api_data.metadata.aliasEmails,
            bannerPhotoUrl = client_api_data.metadata.bannerUrl,
            bio = client_api_data.metadata.bio,
            businessUnit = client_api_data.metadata.businessUnit,
            additionalFields = additionalFields,
            displayName = client_api_data.name,
            datasourceProfiles = client_api_data.metadata.datasourceProfile,
            department = client_api_data.metadata.department,
            email = client_api_data.metadata.email,
            endDate = client_api_data.metadata.endDate,
            profileUrl = client_api_data.metadata.externalProfileLink,
            firstName = client_api_data.metadata.firstName,
            lastName = client_api_data.metadata.lastName,
            location = client_api_data.metadata.location,
            phoneNumber = client_api_data.metadata.phone,
            photoUrl = client_api_data.metadata.photoUrl,
            preferredName = client_api_data.metadata.preferredName,
            pronouns = client_api_data.metadata.pronoun,
            socialNetworks = client_api_data.metadata.socialNetwork,
            startDate = client_api_data.metadata.startDate,
            structuredLocation = client_api_data.metadata.structuredLocation,
            teams = teams,
            metadata = EmployeeMetadata(
                gleanUserId = client_api_data.obfuscatedId,
                gleanLoggingId = client_api_data.metadata.loggingId,
                isSignedUp = client_api_data.metadata.isSignedUp
            ),
            title = client_api_data.metadata.title,
            type = client_api_data.metadata.type
        )

        if not employee.structuredLocation.timezone and client_api_data.metadata.timezone:
            employee.structuredLocation.timezone = client_api_data.metadata.timezone

        return employee
    
