"""
Data models and DTOs for API testing framework.
Provides structured representation of API entities with validation.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class Address:
    """Model representing a user's address."""
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate address data."""
        required_fields = ['street', 'suite', 'city', 'zipcode']
        for field_name in required_fields:
            if not getattr(self, field_name):
                raise ValueError(f"Address field '{field_name}' is required")
        
        # Validate geo coordinates if provided
        if self.geo:
            if 'lat' in self.geo and 'lng' in self.geo:
                try:
                    float(self.geo['lat'])
                    float(self.geo['lng'])
                except ValueError:
                    raise ValueError("Geo coordinates must be valid float values")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Address':
        """Create Address instance from dictionary."""
        return cls(
            street=data.get('street', ''),
            suite=data.get('suite', ''),
            city=data.get('city', ''),
            zipcode=data.get('zipcode', ''),
            geo=data.get('geo', {})
        )


@dataclass
class Company:
    """Model representing a user's company."""
    name: str
    catch_phrase: str
    bs: str
    
    def __post_init__(self):
        """Validate company data."""
        required_fields = ['name', 'catch_phrase', 'bs']
        for field_name in required_fields:
            if not getattr(self, field_name):
                raise ValueError(f"Company field '{field_name}' is required")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Company':
        """Create Company instance from dictionary."""
        return cls(
            name=data.get('name', ''),
            catch_phrase=data.get('catchPhrase', ''),
            bs=data.get('bs', '')
        )


@dataclass
class User:
    """Model representing a user entity."""
    id: Optional[int] = None
    name: str = ""
    username: str = ""
    email: str = ""
    address: Optional[Address] = None
    phone: str = ""
    website: str = ""
    company: Optional[Company] = None
    
    def __post_init__(self):
        """Validate user data."""
        if self.email and '@' not in self.email:
            raise ValueError("Email must contain '@' symbol")
        
        if self.phone and len(self.phone.replace('-', '').replace(' ', '')) < 10:
            raise ValueError("Phone number must be at least 10 digits")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User instance from dictionary."""
        address = None
        if 'address' in data and data['address']:
            address = Address.from_dict(data['address'])
        
        company = None
        if 'company' in data and data['company']:
            company = Company.from_dict(data['company'])
        
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            username=data.get('username', ''),
            email=data.get('email', ''),
            address=address,
            phone=data.get('phone', ''),
            website=data.get('website', ''),
            company=company
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert User instance to dictionary."""
        result = {
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'website': self.website
        }
        
        if self.id is not None:
            result['id'] = self.id
        
        if self.address:
            result['address'] = {
                'street': self.address.street,
                'suite': self.address.suite,
                'city': self.address.city,
                'zipcode': self.address.zipcode,
                'geo': self.address.geo
            }
        
        if self.company:
            result['company'] = {
                'name': self.company.name,
                'catchPhrase': self.company.catch_phrase,
                'bs': self.company.bs
            }
        
        return result


@dataclass
class Post:
    """Model representing a post entity."""
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: str = ""
    body: str = ""
    
    def __post_init__(self):
        """Validate post data."""
        if not self.title and not self.body:
            raise ValueError("Post must have either title or body")
        
        if self.title and len(self.title) > 255:
            raise ValueError("Post title cannot exceed 255 characters")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        """Create Post instance from dictionary."""
        return cls(
            id=data.get('id'),
            user_id=data.get('userId'),
            title=data.get('title', ''),
            body=data.get('body', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Post instance to dictionary."""
        result = {
            'title': self.title,
            'body': self.body
        }
        
        if self.id is not None:
            result['id'] = self.id
        
        if self.user_id is not None:
            result['userId'] = self.user_id
        
        return result


@dataclass
class Comment:
    """Model representing a comment entity."""
    id: Optional[int] = None
    post_id: Optional[int] = None
    name: str = ""
    email: str = ""
    body: str = ""
    
    def __post_init__(self):
        """Validate comment data."""
        if self.email and '@' not in self.email:
            raise ValueError("Comment email must contain '@' symbol")
        
        if not self.body:
            raise ValueError("Comment body is required")
        
        if len(self.body) > 1000:
            raise ValueError("Comment body cannot exceed 1000 characters")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """Create Comment instance from dictionary."""
        return cls(
            id=data.get('id'),
            post_id=data.get('postId'),
            name=data.get('name', ''),
            email=data.get('email', ''),
            body=data.get('body', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Comment instance to dictionary."""
        result = {
            'name': self.name,
            'email': self.email,
            'body': self.body
        }
        
        if self.id is not None:
            result['id'] = self.id
        
        if self.post_id is not None:
            result['postId'] = self.post_id
        
        return result


@dataclass
class APIResponse:
    """Model representing an API response with metadata."""
    status_code: int
    data: Any
    headers: Dict[str, str] = field(default_factory=dict)
    response_time: Optional[float] = None
    request_url: str = ""
    request_method: str = ""
    
    @property
    def is_success(self) -> bool:
        """Check if response indicates success (2xx status code)."""
        return 200 <= self.status_code < 300
    
    @property
    def is_client_error(self) -> bool:
        """Check if response indicates client error (4xx status code)."""
        return 400 <= self.status_code < 500
    
    @property
    def is_server_error(self) -> bool:
        """Check if response indicates server error (5xx status code)."""
        return 500 <= self.status_code < 600


# Type hints for common API collections
UserList = List[User]
PostList = List[Post]
CommentList = List[Comment] 