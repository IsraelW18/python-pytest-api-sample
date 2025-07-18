# python-pytest-api-sample

## 🚧 Under Construction...

## Project Structure
```
api_automation_project/
├── config/                         # Configuration files for base URL, headers, tokens, etc.
│   └── config.yaml                 # YAML config file to manage environment-specific settings
│
├── core/                           # Core reusable components of the framework
│   ├── api_client.py               # Generic wrapper for GET, POST, PUT, DELETE using requests
│   └── logger.py                   # Custom logger for request/response logging
│
├── data/                           # Test data for data-driven testing
│   └── test_data.json              # JSON file with sample payloads and expected values
│
├── tests/                          # All API test files go here
│   ├── test_posts.py               # Test cases related to POST endpoints
│   └── conftest.py                 # Pytest fixtures and shared setup/teardown logic
│
├── utils/                          # Helper functions and reusable assertions
│   └── assertions.py               # Custom assertions for validating API responses
│
├── reports/                        # Optional: HTML/Allure test execution reports
│   └── example_report.html         # Example generated report (optional)
│
├── schemas/                        # JSON Schema files for response structure validation
│   └── post_schema.json            # JSON schema for validating POST API response
│
├── mocks/                          # Optional: mock server configuration and files
│   └── mock_server.json            # Data to simulate server behavior (e.g., for offline testing)
│
├── requirements.txt                # All required Python packages for running the tests
├── pytest.ini                      # Pytest configuration file (e.g. log level, markers, etc.)
└── README.md                       # Project instructions, installation guide, contribution notes
```