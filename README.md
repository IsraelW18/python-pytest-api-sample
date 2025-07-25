# 🚀 Professional API Testing Framework
### Enterprise-Grade Python Framework for REST API Testing with JSONPlaceholder

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-8.4.1-green)](https://pytest.org/)
[![License](https://img.shields.io/badge/license-MIT--0-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📋 Table of Contents
- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [🛠️ Installation](#️-installation)
- [🚦 Quick Start](#-quick-start)
- [🧪 Running Tests](#-running-tests)
- [📊 Reporting](#-reporting)
- [🔧 Configuration](#-configuration)
- [📝 API Documentation](#-api-documentation)
- [🤝 Contributing](#-contributing)
- [👤 Author](#-author)

---

## 🎯 Overview

This is a **professional-grade API testing framework** built with Python and Pytest, specifically designed for comprehensive testing of REST APIs. The framework follows industry best practices and implements a **Service Object Model (SOM)** - the API testing equivalent of Page Object Model (POM) used in UI testing.

### 🎯 Target API
The framework is configured to test [JSONPlaceholder](https://jsonplaceholder.typicode.com), a free fake REST API for testing and prototyping, providing endpoints for:
- 👥 Users (`/users`)
- 📝 Posts (`/posts`) 
- 💬 Comments (`/comments`)

---

## ✨ Key Features

### 🏛️ **Professional Architecture**
- **Service Object Model (SOM)**: Modular service classes for each API endpoint
- **Data Models & DTOs**: Structured data representation with validation
- **Custom Assertions**: Specialized assertions for API testing scenarios
- **Comprehensive Logging**: Multi-level logging with file and console output

### 🔧 **Advanced Testing Capabilities**
- **JSON Schema Validation**: Automatic response structure validation
- **Response Time Monitoring**: Performance tracking and assertions
- **Data-Driven Testing**: External test data management
- **Parameterized Tests**: Efficient test case multiplication
- **Custom Markers**: Organized test categorization

### 📊 **Professional Reporting**
- **HTML Reports**: Beautiful, interactive test reports
- **Coverage Reports**: Code coverage analysis and visualization
- **Allure Integration**: Enterprise-grade test reporting
- **Performance Metrics**: Response time tracking and analysis

### 🛡️ **Quality Assurance**
- **Type Hints**: Full type annotation coverage
- **Code Formatting**: Black code formatter integration
- **Linting**: Flake8 static analysis
- **CI/CD Ready**: GitHub Actions compatible

---

## 🏗️ Architecture

The framework implements a layered architecture following the **Service Object Model (SOM)** pattern:

```
┌─────────────────┐
│   Test Layer    │  ← Test classes with AAA pattern
├─────────────────┤
│ Assertion Layer │  ← Custom API-specific assertions
├─────────────────┤
│  Service Layer  │  ← Business logic for each endpoint (SOM)
├─────────────────┤
│   Model Layer   │  ← Data models and DTOs
├─────────────────┤
│  Client Layer   │  ← HTTP client and core functionality
└─────────────────┘
```

### 🔄 Service Object Model (SOM)
Similar to how POM encapsulates UI elements and actions, SOM encapsulates:
- **API Endpoints**: Each service class represents an API resource
- **HTTP Operations**: Methods for GET, POST, PUT, PATCH, DELETE
- **Business Logic**: Complex operations and data transformations
- **Validation**: Response structure and data validation

---

## 📁 Project Structure

```
pytest-python-api-sample/
├── 📂 core/                          # Core framework components
│   ├── __init__.py
│   ├── api_client.py                 # HTTP client implementation
│   ├── logger.py                     # Professional logging system
│   └── models.py                     # Data models and DTOs
├── 📂 services/                      # Service Object Model (SOM)
│   ├── __init__.py
│   ├── base_service.py               # Base service class
│   ├── user_service.py               # User endpoint service
│   ├── post_service.py               # Post endpoint service
│   └── comment_service.py            # Comment endpoint service
├── 📂 utils/                         # Utility modules
│   ├── assertions.py                 # Custom API assertions
│   └── config_loader.py              # Configuration management
├── 📂 tests/                         # Test implementation
│   ├── conftest.py                   # Pytest fixtures and setup
│   ├── test_users.py                 # User endpoint tests
│   ├── test_posts.py                 # Post endpoint tests
│   └── test_comments.py              # Comment endpoint tests
├── 📂 data/                          # Test data management
│   └── test_data.json                # External test data
├── 📂 schemas/                       # JSON schema validation
│   ├── user_schema.json              # User response schema
│   ├── post_schema.json              # Post response schema
│   └── comment_schema.json           # Comment response schema
├── 📂 config/                        # Configuration files
│   └── config.yaml                   # API configuration
├── 📂 reports/                       # Test reports and artifacts
├── 📂 logs/                          # Log files
├── 📄 pytest.ini                     # Pytest configuration
├── 📄 requirements.txt               # Python dependencies
└── 📄 README.md                      # Project documentation
```

---

## 🛠️ Installation

### Prerequisites
- **Python 3.8+** 
- **pip** package manager
- **Git** (for cloning)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/pytest-python-api-sample.git
cd pytest-python-api-sample
```

### 2️⃣ Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Verify Installation
```bash
pytest --version
python -c "import requests; print('✅ Installation successful!')"
```

---

## 🚦 Quick Start

### Basic Test Execution
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_users.py

# Run specific test function
pytest tests/test_users.py::TestUsersAPI::test_get_single_user

# Run with verbose output
pytest -v
```

### Using Custom Markers
```bash
# Run only integration tests
pytest -m integration

# Run only GET request tests
pytest -m get

# Run user endpoint tests
pytest -m users

# Run positive test cases
pytest -m positive
```

### Generate Reports
```bash
# HTML report
pytest --html=reports/report.html

# Coverage report
pytest --cov=core --cov=services --cov-report=html

# Allure report
pytest --alluredir=reports/allure
allure serve reports/allure
```

---

## 🧪 Running Tests

### Test Categories

#### 🔄 **By Test Type**
```bash
pytest -m unit           # Unit tests
pytest -m integration    # Integration tests
pytest -m smoke          # Smoke tests
pytest -m regression     # Regression tests
pytest -m performance    # Performance tests
```

#### 🌐 **By HTTP Method**
```bash
pytest -m get            # GET request tests
pytest -m post           # POST request tests
pytest -m put            # PUT request tests
pytest -m patch          # PATCH request tests
pytest -m delete         # DELETE request tests
```

#### 📍 **By Endpoint**
```bash
pytest -m users          # User endpoint tests
pytest -m posts          # Post endpoint tests
pytest -m comments       # Comment endpoint tests
```

#### ✅ **By Test Nature**
```bash
pytest -m positive       # Happy path tests
pytest -m negative       # Error scenario tests
pytest -m boundary       # Boundary value tests
```

### Parallel Execution
```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

### Environment Configuration
```bash
# Set log level
LOG_LEVEL=DEBUG pytest

# Set API base URL
API_BASE_URL=https://custom-api.com pytest

# Set test environment
TEST_ENVIRONMENT=staging pytest
```

---

## 📊 Reporting

### HTML Reports
Generate beautiful, interactive HTML reports:
```bash
pytest --html=reports/pytest_report.html --self-contained-html
```

### Coverage Reports
Track code coverage across the framework:
```bash
pytest --cov=core --cov=services --cov-report=html:reports/coverage
```

### Allure Reports
Enterprise-grade reporting with Allure:
```bash
# Generate Allure data
pytest --alluredir=reports/allure

# Serve interactive report
allure serve reports/allure

# Generate static report
allure generate reports/allure -o reports/allure-report
```

### Performance Metrics
Monitor API performance:
```bash
# Run with timing information
pytest --durations=10

# Benchmark tests (requires pytest-benchmark)
pytest --benchmark-only
```

---

## 🔧 Configuration

### API Configuration (`config/config.yaml`)
```yaml
base_url: "https://jsonplaceholder.typicode.com"
headers:
  Content-Type: "application/json"
  User-Agent: "API-Testing-Framework/1.0"
timeout: 10
retry_attempts: 3
```

### Test Configuration (`pytest.ini`)
The framework includes comprehensive pytest configuration:
- Custom markers for test organization
- HTML and coverage reporting
- Parallel execution support
- Performance monitoring
- Logging configuration

### Environment Variables
```bash
# API Configuration
export API_BASE_URL="https://jsonplaceholder.typicode.com"
export LOG_LEVEL="INFO"
export TEST_ENVIRONMENT="local"

# Test Execution
export PYTEST_WORKERS="4"
export COVERAGE_THRESHOLD="80"
```

---

## 📝 API Documentation

### Service Classes

#### UserService
```python
from services import UserService

user_service = UserService(api_client)

# Get all users
response = user_service.get_all_users()

# Get user by ID
response = user_service.get_user_by_id(1)

# Create user
user_data = {"name": "Test User", "username": "test", "email": "test@example.com"}
response = user_service.create_user(user_data)
```

#### PostService
```python
from services import PostService

post_service = PostService(api_client)

# Get all posts
response = post_service.get_all_posts()

# Get posts by user
response = post_service.get_posts_by_user_id(1)

# Create post
post_data = {"title": "Test Post", "body": "Test content", "userId": 1}
response = post_service.create_post(post_data)
```

#### CommentService
```python
from services import CommentService

comment_service = CommentService(api_client)

# Get all comments
response = comment_service.get_all_comments()

# Get comments by post
response = comment_service.get_comments_by_post_id(1)
```

### Custom Assertions
```python
from utils.assertions import assert_status_code, assert_response_time, assert_json_structure

# Status code assertion
assert_status_code(response, 200)

# Response time assertion
assert_response_time(response, max_time=2.0)

# JSON structure assertion
assert_json_structure(response, required_fields=["id", "name", "email"])
```

---

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest`
5. Run linting: `flake8`
6. Format code: `black .`
7. Commit changes: `git commit -m 'Add amazing feature'`
8. Push to branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Code Standards
- **Type Hints**: All functions must include type hints
- **Docstrings**: Use Google-style docstrings
- **Testing**: Maintain 80%+ code coverage
- **Formatting**: Use Black for code formatting
- **Linting**: Pass Flake8 checks

### Commit Convention
```
type(scope): description

feat(users): add user validation service
fix(posts): resolve post creation bug
docs(readme): update installation instructions
test(comments): add boundary value tests
```

---

## 👤 Author

**Israel Wasserman**
- 🔗 [LinkedIn](https://www.linkedin.com/in/israel-wasserman)
- 💼 Senior QA Engineer | Python Automation Developer
- 📧 Email: [contact information]

### About the Author
Senior QA Engineer with extensive experience in:
- 🔧 Test Automation Framework Development
- 🐍 Python Development and Best Practices
- 🌐 API Testing and Validation
- 🏗️ CI/CD Pipeline Integration
- 📊 Test Strategy and Quality Metrics

---

## 📄 License

This project is licensed under the **MIT No Attribution License** - see the [LICENSE](LICENSE) file for details.

**Simple Summary:** You can use this code for any purpose without any restrictions or attribution requirements.


---

<div align="center">

**⭐ Star this repository if it helped you! ⭐**

*Built with ❤️ for the testing community*

</div>

