"""
Test data loader utility for API testing framework.
Provides functions for loading and managing test data from external sources.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from core.logger import get_logger


class DataLoader:
    """Utility class for loading and managing test data."""
    
    def __init__(self, data_file_path: str = None):
        """
        Initialize the test data loader.
        
        Args:
            data_file_path: Path to the test data file (optional)
        """
        self.logger = get_logger()
        if data_file_path:
            self.data_file = Path(data_file_path)
        else:
            self.data_file = Path(__file__).parent.parent / "data" / "test_data.json"
        
        self._data = None
    
    @property
    def data(self) -> Dict[str, Any]:
        """
        Load and return test data (cached after first load).
        
        Returns:
            Dict containing all test data
        """
        if self._data is None:
            self._load_data()
        return self._data
    
    def _load_data(self) -> None:
        """Load test data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            self.logger.info(f"Test data loaded from {self.data_file}")
        except FileNotFoundError:
            self.logger.error(f"Test data file not found: {self.data_file}")
            self._data = {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in test data file: {e}")
            self._data = {}
    
    def get_user_data(self, data_type: str = "valid_user") -> Dict[str, Any]:
        """
        Get user test data.
        
        Args:
            data_type: Type of user data to retrieve
            
        Returns:
            User data dictionary
        """
        return self.data.get("users", {}).get(data_type, {})
    
    def get_post_data(self, data_type: str = "valid_post") -> Dict[str, Any]:
        """
        Get post test data.
        
        Args:
            data_type: Type of post data to retrieve
            
        Returns:
            Post data dictionary
        """
        return self.data.get("posts", {}).get(data_type, {})
    
    def get_comment_data(self, data_type: str = "valid_comment") -> Dict[str, Any]:
        """
        Get comment test data.
        
        Args:
            data_type: Type of comment data to retrieve
            
        Returns:
            Comment data dictionary
        """
        return self.data.get("comments", {}).get(data_type, {})
    
    def get_validation_rules(self, entity_type: str) -> Dict[str, Any]:
        """
        Get validation rules for a specific entity type.
        
        Args:
            entity_type: Type of entity (user, post, comment)
            
        Returns:
            Validation rules dictionary
        """
        return self.data.get("validation_rules", {}).get(entity_type, {})
    
    def get_test_scenario(self, scenario_type: str) -> Dict[str, Any]:
        """
        Get test scenario configuration.
        
        Args:
            scenario_type: Type of scenario (pagination, performance, etc.)
            
        Returns:
            Scenario configuration dictionary
        """
        return self.data.get("test_scenarios", {}).get(scenario_type, {})
    
    def get_expected_counts(self) -> Dict[str, int]:
        """
        Get expected entity counts.
        
        Returns:
            Dictionary with expected counts for different entities
        """
        return self.data.get("expected_counts", {})
    
    def get_error_scenarios(self) -> Dict[str, Any]:
        """
        Get error scenario test data.
        
        Returns:
            Error scenarios dictionary
        """
        return self.data.get("error_scenarios", {})
    
    def get_invalid_data(self, entity_type: str) -> Dict[str, Dict[str, Any]]:
        """
        Get invalid test data for a specific entity type.
        
        Args:
            entity_type: Type of entity (users, posts, comments)
            
        Returns:
            Dictionary of invalid data scenarios
        """
        entity_data = self.data.get(entity_type, {})
        return entity_data.get("invalid_" + entity_type, {})


# Global instance for easy access
test_data_loader = DataLoader()


# Convenience functions
def load_test_data() -> Dict[str, Any]:
    """Load all test data."""
    return test_data_loader.data


def get_user_data(data_type: str = "valid_user") -> Dict[str, Any]:
    """Get user test data."""
    return test_data_loader.get_user_data(data_type)


def get_post_data(data_type: str = "valid_post") -> Dict[str, Any]:
    """Get post test data."""
    return test_data_loader.get_post_data(data_type)


def get_comment_data(data_type: str = "valid_comment") -> Dict[str, Any]:
    """Get comment test data."""
    return test_data_loader.get_comment_data(data_type)


def get_validation_rules(entity_type: str) -> Dict[str, Any]:
    """Get validation rules for entity type."""
    return test_data_loader.get_validation_rules(entity_type)


def get_test_scenario(scenario_type: str) -> Dict[str, Any]:
    """Get test scenario configuration."""
    return test_data_loader.get_test_scenario(scenario_type) 