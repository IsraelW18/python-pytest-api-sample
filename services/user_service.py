"""
User service class for API testing framework.
Handles all user-related API operations.
"""

from typing import List, Optional, Dict, Any
from .base_service import BaseService
from core.models import User, APIResponse, UserList


class UserService(BaseService):
    """Service class for user-related API operations."""
    
    def __init__(self, api_client):
        """Initialize the UserService."""
        super().__init__(api_client)
        self.endpoint_base = "users"
    
    def get_all_users(self) -> APIResponse:
        """
        Get all users from the API.
        
        Returns:
            APIResponse with list of users
        """
        self.logger.info("Getting all users")
        response = self.get()
        
        if response.is_success:
            self.validate_list_response(response, min_items=1)
        
        return response
    
    def get_user_by_id(self, user_id: int) -> APIResponse:
        """
        Get a specific user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            APIResponse with user data
        """
        self.logger.info(f"Getting user with ID: {user_id}")
        response = self.get(f"{user_id}")
        
        if response.is_success:
            self.validate_response_structure(
                response, 
                required_fields=['id', 'name', 'username', 'email']
            )
        
        return response
    
    def create_user(self, user_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new user.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            APIResponse with created user data
        """
        self.logger.info(f"Creating new user: {user_data.get('username', 'Unknown')}")
        
        # Validate user data using User model
        try:
            user = User.from_dict(user_data)
            validated_data = user.to_dict()
        except ValueError as e:
            self.logger.error(f"Invalid user data: {e}")
            raise
        
        response = self.post(data=validated_data)
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['name', 'username', 'email']
            )
        
        return response
    
    def update_user_full(self, user_id: int, user_data: Dict[str, Any]) -> APIResponse:
        """
        Update a user completely (PUT request).
        
        Args:
            user_id: The ID of the user to update
            user_data: Complete user data
            
        Returns:
            APIResponse with updated user data
        """
        self.logger.info(f"Updating user {user_id} (full update)")
        
        # Validate user data
        try:
            user = User.from_dict(user_data)
            user.id = user_id
            validated_data = user.to_dict()
        except ValueError as e:
            self.logger.error(f"Invalid user data: {e}")
            raise
        
        response = self.put(f"{user_id}", data=validated_data)
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['id', 'name', 'username', 'email']
            )
        
        return response
    
    def update_user_partial(self, user_id: int, user_data: Dict[str, Any]) -> APIResponse:
        """
        Update a user partially (PATCH request).
        
        Args:
            user_id: The ID of the user to update
            user_data: Partial user data to update
            
        Returns:
            APIResponse with updated user data
        """
        self.logger.info(f"Updating user {user_id} (partial update)")
        response = self.patch(f"{user_id}", data=user_data)
        
        if response.is_success:
            # Validate that updated fields are present in response
            for field in user_data.keys():
                if field not in response.data:
                    self.logger.warning(f"Updated field '{field}' not found in response")
        
        return response
    
    def delete_user(self, user_id: int) -> APIResponse:
        """
        Delete a user by ID.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            APIResponse for delete operation
        """
        self.logger.info(f"Deleting user {user_id}")
        response = self.delete(f"{user_id}")
        return response
    
    def get_users_by_username(self, username: str) -> APIResponse:
        """
        Get users filtered by username.
        
        Args:
            username: Username to filter by
            
        Returns:
            APIResponse with filtered users
        """
        self.logger.info(f"Getting users by username: {username}")
        response = self.get(params={"username": username})
        
        if response.is_success:
            self.validate_list_response(response)
        
        return response
    
    def validate_user_structure(self, user_data: Dict[str, Any]) -> bool:
        """
        Validate user data structure including nested objects.
        
        Args:
            user_data: User data to validate
            
        Returns:
            True if structure is valid, False otherwise
        """
        required_fields = ['id', 'name', 'username', 'email']
        
        # Check basic required fields
        for field in required_fields:
            if field not in user_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate email format
        if '@' not in user_data.get('email', ''):
            self.logger.error("Invalid email format")
            return False
        
        # Validate address structure if present
        if 'address' in user_data and user_data['address']:
            address = user_data['address']
            address_required = ['street', 'suite', 'city', 'zipcode']
            
            for field in address_required:
                if field not in address:
                    self.logger.error(f"Missing address field: {field}")
                    return False
            
            # Validate geo coordinates if present
            if 'geo' in address and address['geo']:
                geo = address['geo']
                if 'lat' in geo and 'lng' in geo:
                    try:
                        float(geo['lat'])
                        float(geo['lng'])
                    except (ValueError, TypeError):
                        self.logger.error("Invalid geo coordinates format")
                        return False
        
        # Validate company structure if present
        if 'company' in user_data and user_data['company']:
            company = user_data['company']
            company_required = ['name', 'catchPhrase', 'bs']
            
            for field in company_required:
                if field not in company:
                    self.logger.error(f"Missing company field: {field}")
                    return False
        
        return True
    
    def convert_to_user_objects(self, users_data: List[Dict[str, Any]]) -> UserList:
        """
        Convert list of user dictionaries to User objects.
        
        Args:
            users_data: List of user dictionaries
            
        Returns:
            List of User objects
        """
        users = []
        for user_data in users_data:
            try:
                user = User.from_dict(user_data)
                users.append(user)
            except ValueError as e:
                self.logger.warning(f"Failed to convert user data: {e}")
        
        return users 