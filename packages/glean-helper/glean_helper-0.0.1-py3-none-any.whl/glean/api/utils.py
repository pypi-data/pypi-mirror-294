# from enum import Enum
# from typing import Optional, Dict, Union, List
# from api.base import BaseAPI, APIResult
# from config import get_settings, check_api_key
# from pydantic import ValidationError, HttpUrl
# from api.client import APIVersion as ClientAPIVersion, ClientAPI
# from api.index import APIVersion as IndexAPIVersion, IndexAPI
# from models.helper import Employee


# class Banners:

#     @staticmethod
#     def generate_location_mapping_template(employee_list):
#         mapping = {
#             "default": "https://cdn.example.com/default.png",
#             "custom_locations": {},
#             "countries": {}
#         }

#         for employee in employee_list:
#             location = getattr(employee.metadata, 'location', None)
#             structured_location = getattr(employee.metadata, 'structuredLocation', None)

#             if structured_location:
#                 country = getattr(structured_location, 'country', None) or "Unknown"
#                 state = getattr(structured_location, 'state', None) or "Unknown"
#                 city = getattr(structured_location, 'city', None) or "Unknown"

#                 # Add country if not exists
#                 if country not in mapping["countries"]:
#                     mapping["countries"][country] = {
#                         "photo_url": f"https://cdn.example.com/{country.lower()}.png",
#                         "states": {}
#                     }

#                 # Add state if not exists
#                 if state not in mapping["countries"][country]["states"]:
#                     mapping["countries"][country]["states"][state] = {
#                         "photo_url": f"https://cdn.example.com/{country.lower()}/{state.lower()}.png",
#                         "cities": {}
#                     }

#                 # Add city if not exists
#                 if city not in mapping["countries"][country]["states"][state]["cities"]:
#                     mapping["countries"][country]["states"][state]["cities"][city] = {
#                         "photo_url": f"https://cdn.example.com/{country.lower()}/{state.lower()}/{city.lower()}.png"
#                     }

#                 # Add custom location if it doesn't match city, state, or country
#                 if location and location not in [city, state, country]:
#                     if location not in mapping["custom_locations"]:
#                         mapping["custom_locations"][location] = f"https://cdn.example.com/custom/{location.lower()}.png"

#         return mapping

#     @staticmethod
#     def get_banner_url_from_mapping(location_data: dict, mapping: dict) -> HttpUrl:
#         """
#         Returns the URL of a banner image based on the location data of an employee and a mapping of locations to image URLs.

#         Mapping must be a dict with the following structure:
#         {
#             "default": "https://cdn.example.com/default.png",
#             "custom_locations": {
#                 "Space HQ": "https://cdn.example.com/wp-content/uploads/SpaceHQ.png"
#             },
#             "countries": {
#                 "Australia": {
#                     "photo_url": "https://cdn.example.com/wp-content/uploads/30103801/Remote-location-NSW.png",
#                     "states": {
#                         "Victoria": {
#                             "photo_url": "https://cdn.example.com/wp-content/uploads/Remote-location-VIC.png",
#                             "cities": {
#                                 "Melbourne": {
#                                     "photo_url": "https://cdn.example.com/wp-content/uploads/Melbourne.png"
#                                 },
#                                 "Geelong": {
#                                     "photo_url": "https://cdn.example.com/wp-content/uploads/Geelong.png"
#                                 }
#                             }
#                         }
#                         "Western Australia": {
#                             "photo_url": "https://cdn.example.com/wp-content/uploads/Remote-location-WA.png"
#                             "cities": {
#                                 "Perth": {
#                                     "photo_url": "https://cdn.example.com/wp-content/uploads/Perth.png"
#                                 },
#                                 "Fremantle": {
#                                     "photo_url": "https://cdn.example.com/wp-content/uploads/Fremantle.png"
#                                 }
#                         }
#                     }
#                 },
#                 "India": {
#                     "photo_url": "https://cdn.example.com/wp-content/uploads/India.png",
#                     "states": {
#                         "Karnataka": {
#                             "cities": {
#                                 "Bangalore": {
#                                     "photo_url": "https://cdn.example.com/wp-content/uploads/Bangalore.png"
#                                 }
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#         """
#         location = location_data.get('location')
#         structured_location = location_data.get('structuredLocation', {})
#         country = structured_location.get('country') or 'Unknown'
#         state = structured_location.get('state') or "Unknown"
#         city = structured_location.get('city') or "Unknown"

#         # Check for custom location first
#         if location and location in mapping.get('custom_locations', {}):
#             return mapping['custom_locations'][location]

#         # Initialize with default URL
#         photo_url = mapping.get('default')

#         # Helper function to get URL for a given level
#         def get_url_for_level(current_level, key):
#             if isinstance(current_level, dict) and key in current_level:
#                 return current_level[key].get('photo_url')
#             return None

#         # Check for city
#         if country and state and city:
#             url = get_url_for_level(mapping.get('countries', {}).get(country, {}).get('states', {}).get(state, {}).get('cities', {}), city)
#             if url:
#                 return url

#         # Check for state
#         if country and state:
#             url = get_url_for_level(mapping.get('countries', {}).get(country, {}).get('states', {}), state)
#             if url:
#                 return url

#         # Check for country
#         if country:
#             url = get_url_for_level(mapping.get('countries', {}), country)
#             if url:
#                 return url

#         # If no match found, return default
#         return photo_url
    
#     @staticmethod
#     def set_banner_url_from_mapping(employee_data: dict, mapping: dict) -> dict:
#         """
#         Returns the employee configuration, with the banner photo URL set, to push to the Glean Indexing API.
#         """
#         location_data = {
#             "location": employee_data.get('location'),
#             "structuredLocation": employee_data.get('structuredLocation', {})
#         }
#         return {
#             "email": employee_data.get('email'),
#             "firstName": employee_data.get('firstName'),
#             "department": employee_data.get('department'),
#             "additionalFields": [
#                 {
#                     "key": "banner_photo_url",
#                     "value": [Banners.get_banner_url_from_mapping(location_data, mapping)]
#                 }
#             ]
#         }
    
# class Utilities(BaseAPI):
#     def __init__(self, backend_domain: Optional[str] = None):
#         super().__init__(backend_domain)

#         self.index = IndexAPI(backend_domain)
#         self.client = ClientAPI(backend_domain)

#     @classmethod
#     def get_headers(cls, api: str) -> Dict[str, str]:
#         if api not in ['index', 'client']:
#             raise ValueError(f"Internal error: Invalid API specified for get_headers in Utilities class: {api}")
        
#         settings = get_settings()
#         return {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {settings.GLEAN_INDEXING_API_KEY.get_secret_value() if api == "index" else settings.GLEAN_CLIENT_API_KEY.get_secret_value()}'
#         }
    
#     @check_api_key('both')
#     def set_user_banner_from_location(self, mapping: Optional[dict] = None, mapping_file: Optional[str] = "banner_map.json") -> APIResult:
#         """
#         Fetches the location of each employee in the Glean company directory, and updates the
#         banner image in each user's profile based on that location.

#         Requires both the Glean Indexing API and the Glean Client API.
#         The Client API is used to fetch user location information, and the Indexing API is used to update the user records.

#         Args:
#             mapping (dict): A dictionary mapping location names to image URLs.
#             The keys of the dict should be the location name, and the values should be the URL of the image to use.
#         """
#         if not mapping and not mapping_file:
#             raise ValidationError("Either a mapping dictionary or a file path to a JSON mapping file must be provided.")
        
#         if mapping_file:
#             # get full path to mapping file using os.path.join, assuming path in mapping_file is up one level from this file
#             import os
#             mapping_file = os.path.join(os.path.dirname(__file__), '..', mapping_file)

#             #load json file
#             import json
#             with open(mapping_file) as f:
#                 mapping = json.load(f)

#         # Fetch all employees from the Glean Client API
#         r = self.client.get_all_employees()
#         if not r.success:
#             return APIResult(success=False, message="Failed to fetch employees from the Glean Client API.", status_code=r.status_code, api_response=r.api_response)
        
#         employees = r.data

#         request = []
#         # Map each employee's location to the appropriate image URL
#         for employee in employees:
#             request.append(Banners.set_banner_url_from_mapping(employee.metadata.model_dump(), mapping))

#         print(request)
        
#         # Update the user records in the Glean Indexing API
#         response = self.index.employees(request, process_immediately=True)

#         if not response.success:
#             message = "Failed to update employee records in the Glean Indexing API."
#         else:
#             message = "Successfully updated employee records in the Glean Indexing API. Ensure that the banner_photo_url custom field is correctly mapped to the banner_photo_url field in the Glean backend."

#         return APIResult(
#             success=response.success,
#             status_code=response.status_code,
#             message=message,
#             api_response=response.api_response,
#             records_uploaded=response.records_uploaded,
#             upload_id=response.upload_id
#         )