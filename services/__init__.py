"""
Services package for API testing framework.
Contains service classes for different API endpoints (similar to Page Object Model for APIs).
"""

from .user_service import UserService
from .post_service import PostService
from .comment_service import CommentService
from .base_service import BaseService

__all__ = [
    'BaseService',
    'UserService', 
    'PostService',
    'CommentService'
] 