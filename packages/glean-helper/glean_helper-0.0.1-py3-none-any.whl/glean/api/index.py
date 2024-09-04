from enum import Enum
from typing import Optional, Dict, Union, List
from .base import BaseAPI, APIResult
from ..config import get_settings, check_api_key
from pydantic import ValidationError
from ..models.people import Employee, IndexEmployee, IndexEmployees, Team, IndexTeam, IndexTeams, DeleteEmployee, DeleteTeam, generate_upload_id

class APIVersion(Enum):
    V1 = "v1"
    V2 = "v2"

class ProcessingTime(Enum):
    # Number of hours to wait for results to be reflected
    #   when process_immediately is called, vs normal:
    NORMAL = "3 hours"
    IMMEDIATE = "1 hour"

class IndexAPI(BaseAPI):
    def __init__(self, backend_domain: Optional[str] = None):
        super().__init__(domain=backend_domain)
        self.api_name = "index"

    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        settings = get_settings()
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GLEAN_INDEXING_API_KEY.get_secret_value()}'
        }
    
    @check_api_key('index')
    def process_immediately(self) -> APIResult:
        """
        Process all employees and teams recently uploaded immediately
        https://developers.glean.com/indexing/tag/People/paths/~1processallemployeesandteams/post/
        """
        endpoint = f"/api/{self.api_name}/{APIVersion.V1.value}/processallemployeesandteams"
        return self._make_request("POST", endpoint, headers=self.get_headers())

    @check_api_key('index')
    def employee(self, data: Union[dict, IndexEmployee, Employee]) -> APIResult:
        """
        Add or update information about an employee.

        This method accepts either a dictionary of employee data, an IndexEmployee object,
        or an Employee object. If a dictionary is provided, it attempts to validate it
        against both IndexEmployee and Employee models.

        If the employee data is in a flat structure & incorrect format, e.g. Location fields not nested under structuredLocation, or
        social network profiles not nested under socialNetworks, the format will be automatically corrected before submission to the API.

        TODO: Log a warning when this occurs.

        Args:
            data (Union[Dict, IndexEmployee, Employee]): The employee data to be indexed.

        Returns:
            requests.Response: The response from the Glean Indexing API.

        Raises:
            ValueError: If the input data is invalid or cannot be processed.
        """

        if isinstance(data, dict):
            # Try to validate as IndexEmployee first
            try:
                validated_data = IndexEmployee(**data)
            except ValidationError:
                # If that fails, try to validate as Employee and fix missing fields
                fixed_data = Employee.fix_missing_fields(data)
                # TODO: Log a warning if any fields were fixed
                # TODO: Debug log the original input data and fixed data.
                employee_data = Employee(**fixed_data)
                validated_data = IndexEmployee(employee=employee_data)

                # ValidationError will also be raised here if the data is invalid (ie. Missing fields.)
                # TODO: Nice error message, e.g. "Your data was not formatted correctly. Please provide an Employee or IndexEmployee object, or dictionary serialized in these formats."
                
        elif isinstance(data, Employee):
            # If it's an Employee object, wrap it in IndexEmployee
            validated_data = IndexEmployee(employee=data)
        elif isinstance(data, IndexEmployee):
            # If it's already an IndexEmployee, use it as is
            validated_data = data
        else:
            raise ValidationError("Your data was not formatted correctly. Please provide an Employee or IndexEmployee object, or dictionary serialized in these formats.")

        # Prepare the endpoint and make the API request
        endpoint = f"/api/{self.api_name}/{APIVersion.V1.value}/indexemployee"
        response = self._make_request("POST", endpoint, headers=self.get_headers(), data=validated_data.model_dump_json())
        response.records_uploaded = 1
        response.version = validated_data.version
        response.message = "Upload complete. Please allow up to 3 hours for the data to be visible in the Glean app."
        return response

    @check_api_key('index')
    def employees(self, data: Union[Dict, IndexEmployees, List[Employee], List[Dict]], process_immediately: bool = False, disable_stale_data_deletion_check: bool = False) -> APIResult:
        """
        Bulk index a list of employees.
        
        This method handles various input formats and prepares the data for submission to the Glean API.
        
        Args:
            data: Can be one of the following types:
                - IndexEmployees object
                - Dictionary (representing IndexEmployees)
                - List of Employee objects
                - List of dictionaries (each representing an Employee object)
            process_immediately: If True, invoke the process immediately endpoint after uploading.
        
        Returns:
            APIResult: The result of the API call.
        
        Raises:
            pydantic.ValidationError: If the input data format is invalid or cannot be processed.
            ValueError: If any batch upload fails.
        """
        endpoint = f"/api/{self.api_name}/{APIVersion.V1.value}/bulkindexemployees"
        settings = get_settings()
        
        # Validate and process input data
        if isinstance(data, IndexEmployees):
            validated_data = data
        elif isinstance(data, dict):
            upload_id = data.get('uploadId') or data.get('upload_id') or generate_upload_id()
            data['uploadId'] = upload_id
            validated_data = IndexEmployees(**data)
        elif isinstance(data, list):
            if all(isinstance(item, Employee) for item in data):
                validated_data = IndexEmployees(employees=data)
            elif all(isinstance(item, dict) for item in data):
                employees = [Employee(**Employee.fix_missing_fields(item)) for item in data]
                validated_data = IndexEmployees(employees=employees)
            else:
                raise ValidationError("List must contain either all Employee objects or all dictionaries.")
        else:
            # This should never be reached, but is here for completeness
            raise ValidationError("Invalid input data type. Expected IndexEmployees, dict, or list.")

        # Process employee data in batches
        upload_id = validated_data.uploadId or generate_upload_id()
        employees = validated_data.employees or []
        total_count = 0
        warning_message = ""

        total_records = len(employees)
        print(f"Beginning upload of {total_records} records to Glean...")

        for i in range(0, total_records, settings.BATCH_SIZE):
            batch = employees[i:i+settings.BATCH_SIZE]
            is_last_page = i + settings.BATCH_SIZE >= total_records

            batch_payload = IndexEmployees(
                uploadId=upload_id,
                employees=batch,
                disableStaleDataDeletionCheck=validated_data.disableStaleDataDeletionCheck if is_last_page else False,
                isFirstPage=(i == 0),
                isLastPage=is_last_page,
                forceRestartUpload=(i == 0)
            )

            response = self._make_request("POST", endpoint, headers=self.get_headers(), data=batch_payload.model_dump_json())
            response.upload_id = upload_id

            if response.status_code == 400 and "Employees uploaded successfully" in response.api_response:
                # Mark the response as successful if the API returns a 400 with a success message
                response.status_code = 200
                response.success = True

                # Cache the warning message from the API
                warning_message = response.api_response

            if not response.success:
                error_message = f"Upload failed after processing {total_count}/{total_records} records."
                print(error_message)
                print(response.api_response)
                response.message = error_message
                response.records_uploaded = total_count
                return response

            total_count += len(batch)
            print(f"Uploaded {total_count}/{total_records} records to Glean")

            if is_last_page:
                message_parts = [f"Upload complete."]
                
                if warning_message:
                    response.api_response = warning_message  # Add back the warning message to the response
                    message_parts.append(f"The Glean API also returned a warning: See the API response for details.")

                wait_time = ProcessingTime.NORMAL.value
                
                if process_immediately:
                    process_now_response = self.process_immediately()
                    if process_now_response.success:
                        wait_time = ProcessingTime.IMMEDIATE.value
                        message_parts.append(f"Immediate processing of uploaded data scheduled successfully.")
                    else:
                        message_parts.append(f"Immediate processing of the data could not be completed.")
                
                message_parts.append(f"Please allow {wait_time} for the data to be visible in the Glean app.")
                
                success_message = " ".join(message_parts)
                print(success_message)
                print(response.api_response)
                response.message = success_message
                response.records_uploaded = total_count
                return response

        # This should never be reached, but is here for completeness
        raise ValueError("Unexpected end of batch processing")
    
    def team(self, data: IndexTeam):
        """
        Add or update information about a team
        https://developers.glean.com/indexing/tag/People/paths/~1indexteam/post/
        """
        endpoint = f"/api/{self.api_name}/{APIVersion.V2.value}/indexteam"
        return self._make_request("POST", endpoint, headers=self.get_headers(), data=data.model_dump())
    
    @check_api_key('index')
    def teams(self, data: Union[Dict, IndexTeams, List[Team], List[Dict]], process_immediately: bool = False) -> APIResult:
        """
        Bulk index a list of teams
        https://developers.glean.com/indexing/tag/People/paths/~1bulkindexteams/post/
        
        This method handles various input formats and prepares the data for submission to the Glean API.
        
        Args:
            data: Can be one of the following types:
                - IndexTeams object
                - Dictionary (representing IndexTeams)
                - List of Team objects
                - List of dictionaries (each representing a Team object)
            process_immediately: If True, invoke the process immediately endpoint after uploading.
        
        Returns:
            APIResult: The result of the API call.
        
        Raises:
            pydantic.ValidationError: If the input data format is invalid or cannot be processed.
            ValueError: If any batch upload fails.
        """
        endpoint = f"/api/{self.api_name}/{APIVersion.V1.value}/bulkindexteams"
        settings = get_settings()
        
        # Validate and process input data
        if isinstance(data, IndexTeams):
            # If the data is already an IndexTeams object, then it's the correct format so use it as is
            validated_data = data
        elif isinstance(data, dict):
            # If the data is a dictionary, try to validate it as an IndexTeams object.
            # Set the upload ID if it's not already set.
            upload_id = data.get('uploadId') or data.get('upload_id') or generate_upload_id()
            data['uploadId'] = upload_id
            validated_data = IndexTeams(**data)
        elif isinstance(data, list):
            # If the data is a list, check if it's a list of Team objects or a list of dicts (list of team data)
            if all(isinstance(item, Team) for item in data):
                # List of Team objects, so map to IndexTeams object for API request
                validated_data = IndexTeams(teams=data)
            elif all(isinstance(item, dict) for item in data):
                # List of dicts, each representing team data, so map to Team objects and then to IndexTeams object
                teams = [Team(**item) for item in data]
                validated_data = IndexTeams(teams=teams)
            else:
                raise ValidationError("List must contain either all Team objects or all dictionaries containing team data.")
        else:
            # This should never be reached, but is here for completeness
            raise ValidationError("Invalid input data type. Expected IndexTeams, dict, or list.")

        # Process team data in batches
        upload_id = validated_data.uploadId or generate_upload_id()
        teams = validated_data.teams or []
        total_count = 0
        warning_message = ""

        total_records = len(teams)
        print(f"Beginning upload of {total_records} records to Glean...")

        for i in range(0, total_records, settings.BATCH_SIZE):
            batch = teams[i:i+settings.BATCH_SIZE]
            is_last_page = i + settings.BATCH_SIZE >= total_records

            batch_payload = IndexTeams(
                uploadId=upload_id,
                teams=batch,
                isFirstPage=(i == 0),
                isLastPage=is_last_page,
                forceRestartUpload=(i == 0)
            )

            response = self._make_request("POST", endpoint, headers=self.get_headers(), data=batch_payload.model_dump_json())
            response.upload_id = upload_id

            if response.status_code == 400 and "uploaded successfully" in response.api_response:
                # Mark the response as successful if the API returns a 400 with a success message
                response.status_code = 200
                response.success = True

                # Cache the warning message from the API
                warning_message = response.api_response

            if not response.success:
                error_message = f"Upload failed after processing {total_count}/{total_records} records."
                print(error_message)
                print(response.api_response)
                response.message = error_message
                response.records_uploaded = total_count
                return response

            total_count += len(batch)
            print(f"Uploaded {total_count}/{total_records} records to Glean.")

            if is_last_page:
                message_parts = [f"Upload complete."]
                
                if warning_message:
                    response.api_response = warning_message  # Add back the warning message to the response
                    message_parts.append(f"The Glean API also returned a warning: See the API response for details.")

                wait_time = ProcessingTime.NORMAL.value
                
                if process_immediately:
                    process_now_response = self.process_immediately()
                    if process_now_response.success:
                        wait_time = ProcessingTime.IMMEDIATE.value
                        message_parts.append(f"Immediate processing of uploaded data scheduled successfully.")
                        response.api_response = response.api_response + "\n" + process_now_response.api_response
                    else:
                        message_parts.append(f"Immediate processing of the data could not be completed.")
                        response.api_response = response.api_response + "\n" + process_now_response.api_response
                
                message_parts.append(f"Please allow {wait_time} for the data to be visible in the Glean app.")
                
                success_message = " ".join(message_parts)
                print(success_message)
                print(response.api_response)
                response.message = success_message
                response.records_uploaded = total_count
                return response

        # This should never be reached, but is here for completeness
        raise ValueError("Unexpected end of batch processing")
    
    def delete_employee(self, data: DeleteEmployee):
        """
        Delete information about an employee
        https://developers.glean.com/indexing/tag/People/paths/~1deleteemployee/post/
        """
        endpoint = f"/api/{self.api_name}/{APIVersion.V2.value}/deleteemployee"
        return self._make_request("POST", endpoint, headers=self.get_headers(), data=data.model_dump())
    
    def delete_team(self, data: DeleteTeam):
        """
        Delete information about a team
        https://developers.glean.com/indexing/tag/People/paths/~1deleteteam/post/
        """
        endpoint = f"/api/{self.api_name}/{APIVersion.V2.value}/deleteteam"
        return self._make_request("POST", endpoint, headers=self.get_headers(), data=data.model_dump())
    