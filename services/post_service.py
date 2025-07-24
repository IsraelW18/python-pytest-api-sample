"""
Post service class for API testing framework.
Handles all post-related API operations.
"""

from typing import List, Optional, Dict, Any
from .base_service import BaseService
from core.models import Post, APIResponse, PostList


class PostService(BaseService):
    """Service class for post-related API operations."""
    
    def __init__(self, api_client):
        """Initialize the PostService."""
        super().__init__(api_client)
        self.endpoint_base = "posts"
    
    def get_all_posts(self) -> APIResponse:
        """
        Get all posts from the API.
        
        Returns:
            APIResponse with list of posts
        """
        self.logger.info("Getting all posts")
        response = self.get()
        
        if response.is_success:
            self.validate_list_response(response, min_items=1)
        
        return response
    
    def get_post_by_id(self, post_id: int) -> APIResponse:
        """
        Get a specific post by ID.
        
        Args:
            post_id: The ID of the post to retrieve
            
        Returns:
            APIResponse with post data
        """
        self.logger.info(f"Getting post with ID: {post_id}")
        response = self.get(f"{post_id}")
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['id', 'userId', 'title', 'body']
            )
        
        return response
    
    def get_posts_by_user_id(self, user_id: int) -> APIResponse:
        """
        Get all posts by a specific user.
        
        Args:
            user_id: The ID of the user whose posts to retrieve
            
        Returns:
            APIResponse with list of posts
        """
        self.logger.info(f"Getting posts for user ID: {user_id}")
        response = self.get(params={"userId": user_id})
        
        if response.is_success:
            self.validate_list_response(response)
        
        return response
    
    def create_post(self, post_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new post.
        
        Args:
            post_data: Dictionary containing post information
            
        Returns:
            APIResponse with created post data
        """
        self.logger.info(f"Creating new post: {post_data.get('title', 'Untitled')}")
        
        # Validate post data using Post model
        try:
            post = Post.from_dict(post_data)
            validated_data = post.to_dict()
        except ValueError as e:
            self.logger.error(f"Invalid post data: {e}")
            raise
        
        response = self.post(data=validated_data)
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['title', 'body']
            )
        
        return response
    
    def update_post_full(self, post_id: int, post_data: Dict[str, Any]) -> APIResponse:
        """
        Update a post completely (PUT request).
        
        Args:
            post_id: The ID of the post to update
            post_data: Complete post data
            
        Returns:
            APIResponse with updated post data
        """
        self.logger.info(f"Updating post {post_id} (full update)")
        
        # Validate post data
        try:
            post = Post.from_dict(post_data)
            post.id = post_id
            validated_data = post.to_dict()
        except ValueError as e:
            self.logger.error(f"Invalid post data: {e}")
            raise
        
        response = self.put(f"{post_id}", data=validated_data)
        
        if response.is_success:
            self.validate_response_structure(
                response,
                required_fields=['id', 'title', 'body']
            )
        
        return response
    
    def update_post_partial(self, post_id: int, post_data: Dict[str, Any]) -> APIResponse:
        """
        Update a post partially (PATCH request).
        
        Args:
            post_id: The ID of the post to update
            post_data: Partial post data to update
            
        Returns:
            APIResponse with updated post data
        """
        self.logger.info(f"Updating post {post_id} (partial update)")
        response = self.patch(f"{post_id}", data=post_data)
        
        if response.is_success:
            # Validate that updated fields are present in response
            for field in post_data.keys():
                if field not in response.data:
                    self.logger.warning(f"Updated field '{field}' not found in response")
        
        return response
    
    def delete_post(self, post_id: int) -> APIResponse:
        """
        Delete a post by ID.
        
        Args:
            post_id: The ID of the post to delete
            
        Returns:
            APIResponse for delete operation
        """
        self.logger.info(f"Deleting post {post_id}")
        response = self.delete(f"{post_id}")
        return response
    
    def validate_post_structure(self, post_data: Dict[str, Any]) -> bool:
        """
        Validate post data structure.
        
        Args:
            post_data: Post data to validate
            
        Returns:
            True if structure is valid, False otherwise
        """
        required_fields = ['id', 'userId', 'title', 'body']
        
        # Check required fields
        for field in required_fields:
            if field not in post_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate data types
        if not isinstance(post_data.get('id'), int):
            self.logger.error("Post ID must be an integer")
            return False
        
        if not isinstance(post_data.get('userId'), int):
            self.logger.error("User ID must be an integer")
            return False
        
        if not isinstance(post_data.get('title'), str):
            self.logger.error("Post title must be a string")
            return False
        
        if not isinstance(post_data.get('body'), str):
            self.logger.error("Post body must be a string")
            return False
        
        # Validate content length
        if len(post_data.get('title', '')) > 255:
            self.logger.error("Post title too long (max 255 characters)")
            return False
        
        return True
    
    def search_posts_by_title(self, title_keyword: str) -> APIResponse:
        """
        Search posts by title keyword (simulated with client-side filtering).
        
        Args:
            title_keyword: Keyword to search in post titles
            
        Returns:
            APIResponse with filtered posts
        """
        self.logger.info(f"Searching posts by title keyword: {title_keyword}")
        
        # Get all posts first
        all_posts_response = self.get_all_posts()
        
        if not all_posts_response.is_success:
            return all_posts_response
        
        # Filter posts by title keyword
        filtered_posts = []
        for post in all_posts_response.data:
            if title_keyword.lower() in post.get('title', '').lower():
                filtered_posts.append(post)
        
        # Create new response with filtered data
        filtered_response = APIResponse(
            status_code=200,
            data=filtered_posts,
            headers=all_posts_response.headers,
            response_time=all_posts_response.response_time,
            request_url=all_posts_response.request_url,
            request_method=all_posts_response.request_method
        )
        
        self.logger.info(f"Found {len(filtered_posts)} posts matching keyword")
        return filtered_response
    
    def convert_to_post_objects(self, posts_data: List[Dict[str, Any]]) -> PostList:
        """
        Convert list of post dictionaries to Post objects.
        
        Args:
            posts_data: List of post dictionaries
            
        Returns:
            List of Post objects
        """
        posts = []
        for post_data in posts_data:
            try:
                post = Post.from_dict(post_data)
                posts.append(post)
            except ValueError as e:
                self.logger.warning(f"Failed to convert post data: {e}")
        
        return posts 