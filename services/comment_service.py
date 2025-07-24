"""
Comment service class for API testing framework.
Handles all comment-related API operations.
"""

from typing import List, Optional, Dict, Any
from .base_service import BaseService
from core.models import Comment, APIResponse, CommentList


class CommentService(BaseService):
    """Service class for comment-related API operations."""
    
    def __init__(self, api_client):
        """Initialize the CommentService."""
        super().__init__(api_client)
        self.endpoint_base = "comments"
    
    def get_all_comments(self) -> APIResponse:
        """
        Get all comments from the API.
        
        Returns:
            APIResponse with list of comments
        """
        self.logger.info("Getting all comments")
        response = self.get()
        
        if response.is_success:
            self.validate_list_response(response, min_items=1)
        
        return response
    
    def get_comment_by_id(self, comment_id: int) -> APIResponse:
        """
        Get a specific comment by ID.
        
        Args:
            comment_id: The ID of the comment to retrieve
            
        Returns:
            APIResponse with comment data
        """
        self.logger.info(f"Getting comment with ID: {comment_id}")
        response = self.get(f"{comment_id}")
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['id', 'postId', 'name', 'email', 'body']
            )
        
        return response
    
    def get_comments_by_post_id(self, post_id: int) -> APIResponse:
        """
        Get all comments for a specific post.
        
        Args:
            post_id: The ID of the post whose comments to retrieve
            
        Returns:
            APIResponse with list of comments
        """
        self.logger.info(f"Getting comments for post ID: {post_id}")
        response = self.get(params={"postId": post_id})
        
        if response.is_success:
            self.validate_list_response(response)
        
        return response
    
    def create_comment(self, comment_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new comment.
        
        Args:
            comment_data: Dictionary containing comment information
            
        Returns:
            APIResponse with created comment data
        """
        self.logger.info(f"Creating new comment for post: {comment_data.get('postId', 'Unknown')}")
        
        # Validate comment data using Comment model
        try:
            comment = Comment.from_dict(comment_data)
            validated_data = comment.to_dict()
        except ValueError as e:
            self.logger.error(f"Invalid comment data: {e}")
            raise
        
        response = self.post(data=validated_data)
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['name', 'email', 'body']
            )
        
        return response
    
    def update_comment_full(self, comment_id: int, comment_data: Dict[str, Any]) -> APIResponse:
        """
        Update a comment completely (PUT request).
        
        Args:
            comment_id: The ID of the comment to update
            comment_data: Complete comment data
            
        Returns:
            APIResponse with updated comment data
        """
        self.logger.info(f"Updating comment {comment_id} (full update)")
        
        # Validate comment data
        try:
            comment = Comment.from_dict(comment_data)
            comment.id = comment_id
            validated_data = comment.to_dict()
        except ValueError as e:
            self.logger.error(f"Invalid comment data: {e}")
            raise
        
        response = self.put(f"{comment_id}", data=validated_data)
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['id', 'name', 'email', 'body']
            )
        
        return response
    
    def update_comment_partial(self, comment_id: int, comment_data: Dict[str, Any]) -> APIResponse:
        """
        Update a comment partially (PATCH request).
        
        Args:
            comment_id: The ID of the comment to update
            comment_data: Partial comment data to update
            
        Returns:
            APIResponse with updated comment data
        """
        self.logger.info(f"Updating comment {comment_id} (partial update)")
        response = self.patch(f"{comment_id}", data=comment_data)
        
        if response.is_success:
            # Validate that updated fields are present in response
            for field in comment_data.keys():
                if field not in response.data:
                    self.logger.warning(f"Updated field '{field}' not found in response")
        
        return response
    
    def delete_comment(self, comment_id: int) -> APIResponse:
        """
        Delete a comment by ID.
        
        Args:
            comment_id: The ID of the comment to delete
            
        Returns:
            APIResponse for delete operation
        """
        self.logger.info(f"Deleting comment {comment_id}")
        response = self.delete(f"{comment_id}")
        return response
    
    def get_comments_by_email(self, email: str) -> APIResponse:
        """
        Get comments filtered by email.
        
        Args:
            email: Email to filter by
            
        Returns:
            APIResponse with filtered comments
        """
        self.logger.info(f"Getting comments by email: {email}")
        response = self.get(params={"email": email})
        
        if response.is_success:
            self.validate_list_response(response)
        
        return response
    
    def validate_comment_structure(self, comment_data: Dict[str, Any]) -> bool:
        """
        Validate comment data structure.
        
        Args:
            comment_data: Comment data to validate
            
        Returns:
            True if structure is valid, False otherwise
        """
        required_fields = ['id', 'postId', 'name', 'email', 'body']
        
        # Check required fields
        for field in required_fields:
            if field not in comment_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate data types
        if not isinstance(comment_data.get('id'), int):
            self.logger.error("Comment ID must be an integer")
            return False
        
        if not isinstance(comment_data.get('postId'), int):
            self.logger.error("Post ID must be an integer")
            return False
        
        if not isinstance(comment_data.get('name'), str):
            self.logger.error("Comment name must be a string")
            return False
        
        if not isinstance(comment_data.get('email'), str):
            self.logger.error("Comment email must be a string")
            return False
        
        if not isinstance(comment_data.get('body'), str):
            self.logger.error("Comment body must be a string")
            return False
        
        # Validate email format
        if '@' not in comment_data.get('email', ''):
            self.logger.error("Comment email must contain '@' symbol")
            return False
        
        # Validate content length
        if len(comment_data.get('body', '')) > 1000:
            self.logger.error("Comment body too long (max 1000 characters)")
            return False
        
        return True
    
    def search_comments_by_keyword(self, keyword: str) -> APIResponse:
        """
        Search comments by keyword in body (simulated with client-side filtering).
        
        Args:
            keyword: Keyword to search in comment bodies
            
        Returns:
            APIResponse with filtered comments
        """
        self.logger.info(f"Searching comments by keyword: {keyword}")
        
        # Get all comments first
        all_comments_response = self.get_all_comments()
        
        if not all_comments_response.is_success:
            return all_comments_response
        
        # Filter comments by keyword in body
        filtered_comments = []
        for comment in all_comments_response.data:
            if keyword.lower() in comment.get('body', '').lower():
                filtered_comments.append(comment)
        
        # Create new response with filtered data
        filtered_response = APIResponse(
            status_code=200,
            data=filtered_comments,
            headers=all_comments_response.headers,
            response_time=all_comments_response.response_time,
            request_url=all_comments_response.request_url,
            request_method=all_comments_response.request_method
        )
        
        self.logger.info(f"Found {len(filtered_comments)} comments matching keyword")
        return filtered_response
    
    def convert_to_comment_objects(self, comments_data: List[Dict[str, Any]]) -> CommentList:
        """
        Convert list of comment dictionaries to Comment objects.
        
        Args:
            comments_data: List of comment dictionaries
            
        Returns:
            List of Comment objects
        """
        comments = []
        for comment_data in comments_data:
            try:
                comment = Comment.from_dict(comment_data)
                comments.append(comment)
            except ValueError as e:
                self.logger.warning(f"Failed to convert comment data: {e}")
        
        return comments 