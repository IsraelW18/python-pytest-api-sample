"""
Base service class for API testing framework.
Provides common functionality for all API service classes.
"""

import time
from typing import Optional, Dict, Any, Union
from core.api_client import APIClient
from core.models import APIResponse
from core.logger import get_logger


class BaseService:
    """
    Base class for all API service classes.
    Provides common functionality like logging, timing, and response handling.
    """
    
    def __init__(self, api_client: APIClient):
        """
        Initialize the base service.
        
        Args:
            api_client: The API client instance for making requests
        """
        self.client = api_client
        self.logger = get_logger()
        self.endpoint_base = ""  # Override in subclasses
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        expected_status: Union[int, list] = 200
    ) -> APIResponse:
        """
        Make an API request with logging and timing.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request payload for POST/PUT/PATCH requests
            params: Query parameters for GET requests
            expected_status: Expected status code(s) for validation
            
        Returns:
            APIResponse object with response data and metadata
        """
        # Prepare full endpoint
        full_endpoint = f"{self.endpoint_base}/{endpoint}".strip("/")
        full_url = f"{self.client.base_url}/{full_endpoint}"
        
        # Log request
        self.logger.log_api_request(method, full_url, data)
        
        # Measure response time
        start_time = time.time()
        
        # Make the request
        method_func = getattr(self.client, method.lower())
        if method.upper() in ['POST', 'PUT', 'PATCH']:
            response = method_func(full_endpoint, data=data)
        elif method.upper() == 'GET':
            response = method_func(full_endpoint, params=params)
        else:  # DELETE
            response = method_func(full_endpoint)
        
        response_time = time.time() - start_time
        
        # Log response
        self.logger.log_api_response(response.status_code, response_time)
        
        # Create APIResponse object
        try:
            response_data = response.json() if response.text else None
        except ValueError:
            response_data = response.text
        
        api_response = APIResponse(
            status_code=response.status_code,
            data=response_data,
            headers=dict(response.headers),
            response_time=response_time,
            request_url=full_url,
            request_method=method.upper()
        )
        
        # Validate status code if expected_status provided
        if expected_status:
            if isinstance(expected_status, int):
                expected_status = [expected_status]
            
            if api_response.status_code not in expected_status:
                self.logger.error(
                    f"Unexpected status code: {api_response.status_code}. "
                    f"Expected: {expected_status}"
                )
        
        return api_response
    
    def get(
        self, 
        endpoint: str = "", 
        params: Optional[Dict[str, Any]] = None,
        expected_status: Union[int, list] = 200
    ) -> APIResponse:
        """Make a GET request."""
        return self._make_request("GET", endpoint, params=params, expected_status=expected_status)
    
    def post(
        self, 
        endpoint: str = "", 
        data: Optional[Dict[str, Any]] = None,
        expected_status: Union[int, list] = 201
    ) -> APIResponse:
        """Make a POST request."""
        return self._make_request("POST", endpoint, data=data, expected_status=expected_status)
    
    def put(
        self, 
        endpoint: str = "", 
        data: Optional[Dict[str, Any]] = None,
        expected_status: Union[int, list] = 200
    ) -> APIResponse:
        """Make a PUT request."""
        return self._make_request("PUT", endpoint, data=data, expected_status=expected_status)
    
    def patch(
        self, 
        endpoint: str = "", 
        data: Optional[Dict[str, Any]] = None,
        expected_status: Union[int, list] = 200
    ) -> APIResponse:
        """Make a PATCH request."""
        return self._make_request("PATCH", endpoint, data=data, expected_status=expected_status)
    
    def delete(
        self, 
        endpoint: str = "",
        expected_status: Union[int, list] = [200, 204]
    ) -> APIResponse:
        """Make a DELETE request."""
        return self._make_request("DELETE", endpoint, expected_status=expected_status)
    
    def validate_response_structure(self, response: APIResponse, required_fields: list) -> bool:
        """
        Validate that response contains required fields.
        
        Args:
            response: APIResponse object to validate
            required_fields: List of required field names
            
        Returns:
            True if all required fields are present, False otherwise
        """
        if not isinstance(response.data, dict):
            self.logger.error(f"Response data is not a dictionary: {type(response.data)}")
            return False
        
        missing_fields = []
        for field in required_fields:
            if field not in response.data:
                missing_fields.append(field)
        
        if missing_fields:
            self.logger.error(f"Missing required fields: {missing_fields}")
            return False
        
        return True
    
    def validate_list_response(self, response: APIResponse, min_items: int = 0) -> bool:
        """
        Validate that response contains a list with minimum number of items.
        
        Args:
            response: APIResponse object to validate
            min_items: Minimum number of items expected in the list
            
        Returns:
            True if validation passes, False otherwise
        """
        if not isinstance(response.data, list):
            self.logger.error(f"Response data is not a list: {type(response.data)}")
            return False
        
        if len(response.data) < min_items:
            self.logger.error(
                f"List contains {len(response.data)} items, expected at least {min_items}"
            )
            return False
        
        return True 