from enum import Enum
from typing import Optional, Dict, Union
import requests
from .base import BaseAPI, APIResult
from ..models.client.entities import ListEntitiesRequest, ListEntitiesResponse, EntityType, IncludeField, SortOptions, SortOrder, SortBy
from ..models.helper import Employee
from ..config import get_settings, check_api_key
import json

class APIVersion(Enum):
    V1 = "v1"
    V2 = "v2"

class ClientAPI(BaseAPI):
    def __init__(self, backend_domain: Optional[str] = None):
        super().__init__(domain=backend_domain)
        self.api_name = "rest"
        self.settings = get_settings()

    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {get_settings().GLEAN_CLIENT_API_KEY.get_secret_value()}'
        }

    @check_api_key('client')
    def get_employees(self, batch_size: Optional[int] = None, include_management: bool = False, include_permissions: bool = False, include_invite_detail: bool = False, include_extension_detail: bool = False) -> APIResult:
        """
        Fetches all employees from the Glean Client API.
        TODO: Add support for filtering and sorting. E.g. Only return employees in Location X, or in Department Y.
        """
        settings = get_settings()
        endpoint = f"{self.api_name}/api/{APIVersion.V1.value}/listentities"

        # Allow overriding the batch size. If not specified, use the value from settings.
        if not batch_size:
            batch_size = settings.BATCH_SIZE

        # Create initial request object
        request = ListEntitiesRequest(
            cursor=None,
            entityType=EntityType.PEOPLE,
            filter=[],
            includeFields=[IncludeField.PEOPLE],
            pageSize=batch_size,
            query="",
            sort=[SortOptions(orderBy=SortOrder.DESC, sortBy=SortBy.ENTITY_NAME)],
            source="Glean Helper Tool"
        )

        # Process include flags
        if include_management:
            request.includeFields.append(IncludeField.MANAGEMENT_DETAILS)
        if include_permissions:
            request.includeFields.append(IncludeField.PERMISSIONS)
        if include_invite_detail:
            request.includeFields.append(IncludeField.INVITE_INFO)
        if include_extension_detail:
            request.includeFields.append(IncludeField.LAST_EXTENSION_USE)

        # Make initial request
        print(f"Beginning fetch of employee records from Glean...")
        response = self._make_request("POST", endpoint, headers=self.get_headers(), data=request.model_dump_json())

        if not response.success:
            response.message = "Failed to fetch employees from the Glean API."
            return response

        # Write api_response to a file:
        # with open('api_response.json', 'w') as f:
        #     f.write(response.api_response)

        # Write jsonified api_response to a file:
        # with open('api_response_jsonified.json', 'w') as f:
        #     json.dump(json.loads(response.api_response), f, indent=4)
        
        # Process the response and pageinate if necessary
        response_data = ListEntitiesResponse(**json.loads(response.api_response))

        print(f"Fetched {len(response_data.results)}/{response_data.totalCount} records.")

        if not response_data.hasMoreResults:
            return APIResult(
                success=True,
                status_code=response.status_code,
                message="All employees fetched successfully.",
                data=response_data.results,
                api_response=response.api_response,
                records=response_data.totalCount,
            )

        # Paginate through the results
        
        request.cursor = response_data.cursor   # Cursor is a value from Glean representing the position in the overall results at which to start.
        print(f"Cursor value: {request.cursor}")
        remaining_records = (response_data.totalCount - len(response_data.results))

        employees = []
        employees.extend(Employee.from_client_api(employee) for employee in response_data.results)
        
        # Paginate through the results
        while response_data.hasMoreResults:
            
            response = self._make_request("POST", endpoint, headers=self.get_headers(), data=request.model_dump_json())
            response_data = ListEntitiesResponse.model_validate(json.loads(response.api_response))
            remaining_records -= len(response_data.results)
            employees.extend(Employee.from_client_api(employee) for employee in response_data.results)
            request.cursor = response_data.cursor
            print(f"Cursor value: {request.cursor}")
            print(f"Fetched {(response_data.totalCount - remaining_records)}/{response_data.totalCount} records.")
            print(f"{remaining_records} records remaining to be fetched...")

        
        return APIResult(
            success=True,
            status_code=response.status_code,
            message="All employees fetched successfully.",
            data=employees,
            api_response=response.api_response,
            records=response_data.totalCount,
        )