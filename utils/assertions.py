"""
Custom assertion utilities for API testing framework.
Provides specialized assertions for common API testing scenarios.
"""

import re
import json
from typing import Any, Dict, List, Union, Optional
from core.models import APIResponse
from core.logger import get_logger


class APIAssertions:
    """Custom assertions for API testing with detailed error messages."""
    
    def __init__(self):
        self.logger = get_logger()
    
    def assert_status_code(self, response: APIResponse, expected_status: Union[int, List[int]], 
                          message: str = None) -> None:
        """
        Assert that response status code matches expected value(s).
        
        Args:
            response: APIResponse object
            expected_status: Expected status code or list of acceptable codes
            message: Custom error message
        """
        if isinstance(expected_status, int):
            expected_status = [expected_status]
        
        if response.status_code not in expected_status:
            error_msg = (
                message or 
                f"Expected status code {expected_status}, but got {response.status_code}. "
                f"Response: {response.data}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Status code assertion passed: {response.status_code}")
    
    def assert_response_time(self, response: APIResponse, max_time: float, 
                           message: str = None) -> None:
        """
        Assert that response time is within acceptable limits.
        
        Args:
            response: APIResponse object
            max_time: Maximum acceptable response time in seconds
            message: Custom error message
        """
        if response.response_time is None:
            raise AssertionError("Response time not available")
        
        if response.response_time > max_time:
            error_msg = (
                message or
                f"Response time {response.response_time:.3f}s exceeded maximum {max_time}s"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Response time assertion passed: {response.response_time:.3f}s")
    
    def assert_json_structure(self, response: APIResponse, required_fields: List[str],
                             message: str = None) -> None:
        """
        Assert that JSON response contains all required fields.
        
        Args:
            response: APIResponse object
            required_fields: List of required field names
            message: Custom error message
        """
        if not isinstance(response.data, dict):
            error_msg = f"Response data is not a JSON object: {type(response.data)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        missing_fields = []
        for field in required_fields:
            if field not in response.data:
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = (
                message or
                f"Missing required fields: {missing_fields}. "
                f"Available fields: {list(response.data.keys())}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"JSON structure assertion passed: {required_fields}")
    
    def assert_json_list(self, response: APIResponse, min_items: int = 0, 
                        max_items: int = None, message: str = None) -> None:
        """
        Assert that response contains a list with specified constraints.
        
        Args:
            response: APIResponse object
            min_items: Minimum number of items in the list
            max_items: Maximum number of items in the list (optional)
            message: Custom error message
        """
        if not isinstance(response.data, list):
            error_msg = f"Response data is not a list: {type(response.data)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        actual_count = len(response.data)
        
        if actual_count < min_items:
            error_msg = (
                message or
                f"List contains {actual_count} items, expected at least {min_items}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        if max_items is not None and actual_count > max_items:
            error_msg = (
                message or
                f"List contains {actual_count} items, expected at most {max_items}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"JSON list assertion passed: {actual_count} items")
    
    def assert_field_value(self, response: APIResponse, field_path: str, 
                          expected_value: Any, message: str = None) -> None:
        """
        Assert that a specific field has the expected value.
        
        Args:
            response: APIResponse object
            field_path: Dot-separated path to the field (e.g., "user.address.city")
            expected_value: Expected field value
            message: Custom error message
        """
        actual_value = self._get_nested_field(response.data, field_path)
        
        if actual_value != expected_value:
            error_msg = (
                message or
                f"Field '{field_path}' has value '{actual_value}', expected '{expected_value}'"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Field value assertion passed: {field_path} = {expected_value}")
    
    def assert_field_type(self, response: APIResponse, field_path: str, 
                         expected_type: type, message: str = None) -> None:
        """
        Assert that a specific field has the expected type.
        
        Args:
            response: APIResponse object
            field_path: Dot-separated path to the field
            expected_type: Expected Python type
            message: Custom error message
        """
        actual_value = self._get_nested_field(response.data, field_path)
        
        if not isinstance(actual_value, expected_type):
            error_msg = (
                message or
                f"Field '{field_path}' has type {type(actual_value).__name__}, "
                f"expected {expected_type.__name__}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Field type assertion passed: {field_path} is {expected_type.__name__}")
    
    def assert_email_format(self, response: APIResponse, field_path: str, 
                          message: str = None) -> None:
        """
        Assert that a field contains a valid email address.
        
        Args:
            response: APIResponse object
            field_path: Path to the email field
            message: Custom error message
        """
        email_value = self._get_nested_field(response.data, field_path)
        
        if not isinstance(email_value, str):
            error_msg = f"Email field '{field_path}' is not a string: {type(email_value)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email_value):
            error_msg = (
                message or
                f"Field '{field_path}' contains invalid email format: '{email_value}'"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Email format assertion passed: {field_path}")
    
    def assert_url_format(self, response: APIResponse, field_path: str, 
                         message: str = None) -> None:
        """
        Assert that a field contains a valid URL.
        
        Args:
            response: APIResponse object
            field_path: Path to the URL field
            message: Custom error message
        """
        url_value = self._get_nested_field(response.data, field_path)
        
        if not isinstance(url_value, str):
            error_msg = f"URL field '{field_path}' is not a string: {type(url_value)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, url_value, re.IGNORECASE):
            error_msg = (
                message or
                f"Field '{field_path}' contains invalid URL format: '{url_value}'"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"URL format assertion passed: {field_path}")
    
    def assert_numeric_range(self, response: APIResponse, field_path: str, 
                           min_value: Union[int, float] = None, 
                           max_value: Union[int, float] = None,
                           message: str = None) -> None:
        """
        Assert that a numeric field is within specified range.
        
        Args:
            response: APIResponse object
            field_path: Path to the numeric field
            min_value: Minimum acceptable value
            max_value: Maximum acceptable value
            message: Custom error message
        """
        numeric_value = self._get_nested_field(response.data, field_path)
        
        if not isinstance(numeric_value, (int, float)):
            error_msg = f"Field '{field_path}' is not numeric: {type(numeric_value)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        if min_value is not None and numeric_value < min_value:
            error_msg = (
                message or
                f"Field '{field_path}' value {numeric_value} is below minimum {min_value}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        if max_value is not None and numeric_value > max_value:
            error_msg = (
                message or
                f"Field '{field_path}' value {numeric_value} is above maximum {max_value}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Numeric range assertion passed: {field_path} = {numeric_value}")
    
    def assert_string_length(self, response: APIResponse, field_path: str,
                           min_length: int = None, max_length: int = None,
                           message: str = None) -> None:
        """
        Assert that a string field has acceptable length.
        
        Args:
            response: APIResponse object
            field_path: Path to the string field
            min_length: Minimum acceptable length
            max_length: Maximum acceptable length
            message: Custom error message
        """
        string_value = self._get_nested_field(response.data, field_path)
        
        if not isinstance(string_value, str):
            error_msg = f"Field '{field_path}' is not a string: {type(string_value)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        actual_length = len(string_value)
        
        if min_length is not None and actual_length < min_length:
            error_msg = (
                message or
                f"Field '{field_path}' length {actual_length} is below minimum {min_length}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        if max_length is not None and actual_length > max_length:
            error_msg = (
                message or
                f"Field '{field_path}' length {actual_length} is above maximum {max_length}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"String length assertion passed: {field_path} ({actual_length} chars)")
    
    def assert_contains_substring(self, response: APIResponse, field_path: str, 
                                substring: str, case_sensitive: bool = True,
                                message: str = None) -> None:
        """
        Assert that a string field contains a specific substring.
        
        Args:
            response: APIResponse object
            field_path: Path to the string field
            substring: Substring to search for
            case_sensitive: Whether the search is case-sensitive
            message: Custom error message
        """
        string_value = self._get_nested_field(response.data, field_path)
        
        if not isinstance(string_value, str):
            error_msg = f"Field '{field_path}' is not a string: {type(string_value)}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        search_value = string_value if case_sensitive else string_value.lower()
        search_substring = substring if case_sensitive else substring.lower()
        
        if search_substring not in search_value:
            error_msg = (
                message or
                f"Field '{field_path}' does not contain substring '{substring}'. "
                f"Actual value: '{string_value}'"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Substring assertion passed: '{substring}' found in {field_path}")
    
    def assert_header_present(self, response: APIResponse, header_name: str,
                            message: str = None) -> None:
        """
        Assert that a specific header is present in the response.
        
        Args:
            response: APIResponse object
            header_name: Name of the header to check
            message: Custom error message
        """
        if header_name not in response.headers:
            error_msg = (
                message or
                f"Header '{header_name}' not found. "
                f"Available headers: {list(response.headers.keys())}"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Header assertion passed: {header_name} present")
    
    def assert_header_value(self, response: APIResponse, header_name: str, 
                          expected_value: str, message: str = None) -> None:
        """
        Assert that a header has the expected value.
        
        Args:
            response: APIResponse object
            header_name: Name of the header
            expected_value: Expected header value
            message: Custom error message
        """
        if header_name not in response.headers:
            error_msg = f"Header '{header_name}' not found in response"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        actual_value = response.headers[header_name]
        if actual_value != expected_value:
            error_msg = (
                message or
                f"Header '{header_name}' has value '{actual_value}', "
                f"expected '{expected_value}'"
            )
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
        
        self.logger.info(f"Header value assertion passed: {header_name} = {expected_value}")
    
    def _get_nested_field(self, data: Any, field_path: str) -> Any:
        """
        Get a nested field value using dot notation.
        
        Args:
            data: Data object to search in
            field_path: Dot-separated path to the field
            
        Returns:
            Field value
            
        Raises:
            AssertionError: If field path is not found
        """
        current = data
        path_parts = field_path.split('.')
        
        try:
            for part in path_parts:
                if isinstance(current, dict):
                    current = current[part]
                elif isinstance(current, list):
                    current = current[int(part)]
                else:
                    raise KeyError(f"Cannot access field '{part}' in {type(current)}")
            
            return current
        
        except (KeyError, IndexError, ValueError, TypeError) as e:
            error_msg = f"Field path '{field_path}' not found in response data: {e}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)


# Global instance for easy access
api_assert = APIAssertions()

# Convenience functions for common assertions
def assert_status_code(response: APIResponse, expected_status: Union[int, List[int]], 
                      message: str = None) -> None:
    """Convenience function for status code assertion."""
    api_assert.assert_status_code(response, expected_status, message)

def assert_response_time(response: APIResponse, max_time: float, 
                        message: str = None) -> None:
    """Convenience function for response time assertion."""
    api_assert.assert_response_time(response, max_time, message)

def assert_json_structure(response: APIResponse, required_fields: List[str],
                         message: str = None) -> None:
    """Convenience function for JSON structure assertion."""
    api_assert.assert_json_structure(response, required_fields, message)

def assert_json_list(response: APIResponse, min_items: int = 0, 
                    max_items: int = None, message: str = None) -> None:
    """Convenience function for JSON list assertion."""
    api_assert.assert_json_list(response, min_items, max_items, message)
