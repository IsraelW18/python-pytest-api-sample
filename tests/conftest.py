# tests/conftest.py
"""
Pytest configuration and fixtures for API testing framework.
Provides shared test fixtures and setup for all test modules.
"""

import os
import sys
import pytest
import json
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.api_client import APIClient
from core.logger import get_logger, setup_test_logging
from services import UserService, PostService, CommentService
from utils.config_loader import load_config


@pytest.fixture(scope="session")
def api_client():
    """
    Creates a single shared instance of the APIClient for all tests.
    
    Returns:
        APIClient: Configured API client instance
    """
    return APIClient()


@pytest.fixture(scope="session")
def logger():
    """
    Sets up the professional logging system for tests.
    
    Returns:
        APITestLogger: Configured logger instance
    """
    return get_logger()


@pytest.fixture(scope="session")
def user_service(api_client):
    """
    Creates a UserService instance for user-related API operations.
    
    Args:
        api_client: APIClient fixture
        
    Returns:
        UserService: Service for user endpoint operations
    """
    return UserService(api_client)


@pytest.fixture(scope="session")
def post_service(api_client):
    """
    Creates a PostService instance for post-related API operations.
    
    Args:
        api_client: APIClient fixture
        
    Returns:
        PostService: Service for post endpoint operations
    """
    return PostService(api_client)


@pytest.fixture(scope="session")
def comment_service(api_client):
    """
    Creates a CommentService instance for comment-related API operations.
    
    Args:
        api_client: APIClient fixture
        
    Returns:
        CommentService: Service for comment endpoint operations
    """
    return CommentService(api_client)


@pytest.fixture(scope="session")
def test_data():
    """
    Loads test data from JSON file.
    
    Returns:
        dict: Test data configuration
    """
    data_file = Path(__file__).parent.parent / "data" / "test_data.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def config():
    """
    Loads application configuration.
    
    Returns:
        dict: Application configuration
    """
    return load_config()


@pytest.fixture(autouse=True)
def setup_test_environment(logger):
    """
    Automatically sets up test environment for each test.
    
    Args:
        logger: Logger fixture
    """
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)


@pytest.fixture
def valid_user_data(test_data):
    """
    Provides valid user data for testing.
    
    Args:
        test_data: Test data fixture
        
    Returns:
        dict: Valid user data
    """
    return test_data["users"]["valid_user"].copy()


@pytest.fixture
def valid_post_data(test_data):
    """
    Provides valid post data for testing.
    
    Args:
        test_data: Test data fixture
        
    Returns:
        dict: Valid post data
    """
    return test_data["posts"]["valid_post"].copy()


@pytest.fixture
def valid_comment_data(test_data):
    """
    Provides valid comment data for testing.
    
    Args:
        test_data: Test data fixture
        
    Returns:
        dict: Valid comment data
    """
    return test_data["comments"]["valid_comment"].copy()


@pytest.fixture
def performance_config(test_data):
    """
    Provides performance testing configuration.
    
    Args:
        test_data: Test data fixture
        
    Returns:
        dict: Performance configuration
    """
    return test_data["test_scenarios"]["performance"]


# Pytest hooks for enhanced reporting
def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Ensure reports directory exists
    Path("reports").mkdir(exist_ok=True)


def pytest_runtest_setup(item):
    """Setup before each test."""
    logger = get_logger()
    test_name = f"{item.cls.__name__}::{item.name}" if item.cls else item.name
    logger.log_test_start(test_name)


def pytest_runtest_teardown(item, nextitem):
    """Cleanup after each test."""
    logger = get_logger()
    test_name = f"{item.cls.__name__}::{item.name}" if item.cls else item.name
    
    # Determine test status
    test_status = "PASSED"
    if hasattr(item, '_request') and hasattr(item._request, 'node'):
        if hasattr(item._request.node, 'rep_call'):
            if item._request.node.rep_call.failed:
                test_status = "FAILED"
            elif item._request.node.rep_call.skipped:
                test_status = "SKIPPED"
    
    logger.log_test_end(test_name, test_status)
