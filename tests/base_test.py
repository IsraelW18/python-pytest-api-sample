"""
Base test class for API testing framework.
Provides common functionality and patterns for all test classes.
"""

import pytest
from typing import Dict, Any, List
from core.logger import get_logger
from core.models import APIResponse
from utils.assertions import (
    assert_status_code, 
    assert_response_time, 
    assert_json_structure,
    assert_json_list
)


class BaseAPITest:
    """
    Base class for all API test classes.
    Implements common test patterns and utilities following AAA pattern.
    """
    
    def setup_method(self):
        """Setup method called before each test method."""
        self.logger = get_logger()
    
    def teardown_method(self):
        """Teardown method called after each test method."""
        pass
    
    # Common assertion patterns
    def assert_successful_response(self, response: APIResponse, 
                                 expected_status: int = 200,
                                 max_response_time: float = 2.0) -> None:
        """
        Assert that response indicates success with good performance.
        
        Args:
            response: APIResponse to validate
            expected_status: Expected HTTP status code
            max_response_time: Maximum acceptable response time
        """
        assert_status_code(response, expected_status)
        assert_response_time(response, max_response_time)
    
    def assert_list_response(self, response: APIResponse, 
                           min_items: int = 1,
                           required_fields: List[str] = None) -> None:
        """
        Assert that response contains a valid list with expected structure.
        
        Args:
            response: APIResponse to validate
            min_items: Minimum expected items in list
            required_fields: Required fields in each list item
        """
        self.assert_successful_response(response)
        assert_json_list(response, min_items=min_items)
        
        if required_fields and response.data:
            # Validate structure of first item as sample
            first_item_response = APIResponse(
                status_code=response.status_code,
                data=response.data[0],
                headers=response.headers,
                response_time=response.response_time
            )
            assert_json_structure(first_item_response, required_fields)
    
    def assert_single_item_response(self, response: APIResponse,
                                  required_fields: List[str]) -> None:
        """
        Assert that response contains a single valid item.
        
        Args:
            response: APIResponse to validate
            required_fields: Required fields in the item
        """
        self.assert_successful_response(response)
        assert_json_structure(response, required_fields)
    
    def assert_creation_response(self, response: APIResponse, 
                               created_data: Dict[str, Any],
                               required_fields: List[str] = None) -> None:
        """
        Assert that creation response is valid and contains expected data.
        
        Args:
            response: APIResponse to validate
            created_data: Data that was sent for creation
            required_fields: Required fields in response
        """
        self.assert_successful_response(response, expected_status=201)
        
        if required_fields:
            assert_json_structure(response, required_fields)
        
        # Verify that sent data is reflected in response
        for key, value in created_data.items():
            if key in response.data:
                assert response.data[key] == value, \
                    f"Created {key} should be {value}, got {response.data[key]}"
    
    def assert_update_response(self, response: APIResponse,
                             updated_data: Dict[str, Any]) -> None:
        """
        Assert that update response is valid and contains updated data.
        
        Args:
            response: APIResponse to validate
            updated_data: Data that was sent for update
        """
        self.assert_successful_response(response)
        
        # Verify that updated data is reflected in response
        for key, value in updated_data.items():
            if key in response.data:
                assert response.data[key] == value, \
                    f"Updated {key} should be {value}, got {response.data[key]}"
    
    def assert_deletion_response(self, response: APIResponse) -> None:
        """
        Assert that deletion response is valid.
        
        Args:
            response: APIResponse to validate
        """
        # JSONPlaceholder returns 200 for DELETE operations
        assert_status_code(response, [200, 204])
        assert_response_time(response, 2.0)
    
    def assert_not_found_response(self, response: APIResponse) -> None:
        """
        Assert that response indicates resource not found.
        
        Args:
            response: APIResponse to validate
        """
        assert_status_code(response, 404)
        assert_response_time(response, 2.0)
    
    def assert_bad_request_response(self, response: APIResponse) -> None:
        """
        Assert that response indicates bad request.
        
        Args:
            response: APIResponse to validate
        """
        assert_status_code(response, 400)
        assert_response_time(response, 2.0)
    
    # Common test patterns
    def perform_get_all_test(self, service, min_items: int = 1,
                           required_fields: List[str] = None) -> APIResponse:
        """
        Perform a standard "get all items" test.
        
        Args:
            service: Service instance to use
            min_items: Minimum expected items
            required_fields: Required fields in each item
            
        Returns:
            APIResponse from the operation
        """
        # Arrange - Nothing specific needed
        
        # Act
        response = service.get()
        
        # Assert
        self.assert_list_response(response, min_items, required_fields)
        
        return response
    
    def perform_get_by_id_test(self, service, item_id: int,
                             required_fields: List[str]) -> APIResponse:
        """
        Perform a standard "get by ID" test.
        
        Args:
            service: Service instance to use
            item_id: ID of item to retrieve
            required_fields: Required fields in response
            
        Returns:
            APIResponse from the operation
        """
        # Arrange - Nothing specific needed
        
        # Act
        response = service.get(f"{item_id}")
        
        # Assert
        self.assert_single_item_response(response, required_fields)
        assert response.data["id"] == item_id, \
            f"Response ID should be {item_id}, got {response.data.get('id')}"
        
        return response
    
    def perform_creation_test(self, service, test_data: Dict[str, Any],
                            required_fields: List[str] = None) -> APIResponse:
        """
        Perform a standard "create item" test.
        
        Args:
            service: Service instance to use
            test_data: Data to create item with
            required_fields: Required fields in response
            
        Returns:
            APIResponse from the operation
        """
        # Arrange - test_data parameter provides the arrangement
        
        # Act
        response = service.post(data=test_data)
        
        # Assert
        self.assert_creation_response(response, test_data, required_fields)
        
        return response
    
    def perform_update_test(self, service, item_id: int, 
                          update_data: Dict[str, Any]) -> APIResponse:
        """
        Perform a standard "update item" test.
        
        Args:
            service: Service instance to use
            item_id: ID of item to update
            update_data: Data to update item with
            
        Returns:
            APIResponse from the operation
        """
        # Arrange - update_data parameter provides the arrangement
        
        # Act
        response = service.patch(f"{item_id}", data=update_data)
        
        # Assert
        self.assert_update_response(response, update_data)
        
        return response
    
    def perform_deletion_test(self, service, item_id: int) -> APIResponse:
        """
        Perform a standard "delete item" test.
        
        Args:
            service: Service instance to use
            item_id: ID of item to delete
            
        Returns:
            APIResponse from the operation
        """
        # Arrange - Nothing specific needed
        
        # Act
        response = service.delete(f"{item_id}")
        
        # Assert
        self.assert_deletion_response(response)
        
        return response
    
    def perform_not_found_test(self, service, invalid_id: int) -> APIResponse:
        """
        Perform a standard "not found" test.
        
        Args:
            service: Service instance to use
            invalid_id: Invalid ID that should not exist
            
        Returns:
            APIResponse from the operation
        """
        # Arrange - invalid_id parameter provides the arrangement
        
        # Act
        response = service.get(f"{invalid_id}", expected_status=404)
        
        # Assert
        self.assert_not_found_response(response)
        
        return response 