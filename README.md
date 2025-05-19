# Flask API Project

A robust RESTful API built with Flask, featuring user authentication, request logging, and comprehensive user management functionality.

## Project Structure

```
flask-api
├── LICENSE
├── main.py                       # Entry point for the application
├── Makefile                      # Contains useful commands for the project
├── migrations                    # Database migration files using Alembic
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions                  # Migration version files
│       ├── 295d45358817_add_users_table.py
│       └── 4018509c0ce4_add_logs_table.py
├── README.md
├── requirements.txt              # Project dependencies
├── ruff.toml                     # Ruff linter configuration
├── src                           # Main source code directory
│   ├── api                       # API routes and endpoints
│   │   ├── __init__.py
│   │   └── v1                    # API version 1
│   │       ├── auth.py           # Authentication endpoints
│   │       ├── __init__.py
│   │       └── users.py          # User management endpoints
│   ├── config.py                 # Application configuration
│   ├── controllers               # Business logic layer
│   │   ├── auth.py               # Authentication logic
│   │   ├── __init__.py
│   │   ├── log.py                # Logging logic
│   │   └── user.py               # User management logic
│   ├── exceptions.py             # Custom exception classes
│   ├── extensions.py             # Flask extensions (e.g., SQLAlchemy)
│   ├── __init__.py
│   ├── logging.py                # Request logging functionality
│   ├── mixins.py                 # Reusable model mixins
│   ├── models                    # Database models
│   │   ├── __init__.py
│   │   ├── log.py                # Log model
│   │   └── user.py               # User model
│   ├── repositories              # Data access layer
│   │   ├── base.py               # Base repository with common operations
│   │   ├── __init__.py
│   │   ├── log.py                # Log repository
│   │   └── user.py               # User repository
│   ├── schemas                   # Pydantic schemas for validation
│   │   ├── auth.py               # Authentication schemas
│   │   ├── filter.py             # Filtering schemas
│   │   ├── __init__.py
│   │   ├── log.py                # Log schemas
│   │   ├── pagination.py         # Pagination schemas
│   │   └── user.py               # User schemas
│   ├── server.py                 # Flask app creation and configuration
│   └── utils                     # Utility functions
│       ├── auth.py               # Authentication utilities
│       ├── __init__.py
│       └── validators.py         # Input validators
└── tests                         # Test suite
    ├── api                       # API tests
    │   ├── __init__.py
    │   ├── test_auth_api.py      # Authentication API tests
    │   └── test_user_api.py      # User API tests
    ├── conftest.py               # Test fixtures and configuration
    ├── controllers               # Controller tests
    │   ├── __init__.py
    │   ├── test_auth_controller.py  # Authentication controller tests
    │   └── test_user_controller.py  # User controller tests
    ├── __init__.py
    └── repositories              # Repository tests
        ├── __init__.py
        └── test_base_repository.py  # Base repository tests
```

## Project Architecture

The project follows a clean, layered architecture:

1. **API Layer** (`src/api/v1`): HTTP endpoints that receive requests and return responses
2. **Controller Layer** (`src/controllers`): Business logic and validation
3. **Repository Layer** (`src/repositories`): Data access abstractions over database models
4. **Model Layer** (`src/models`): SQLAlchemy ORM models representing database tables
5. **Schema Layer** (`src/schemas`): Pydantic models for request/response validation and serialization

## API Endpoints

### Authentication

#### Login
- **URL**: `/api/v1/auth/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string"
  }
  ```
- **Status Codes**:
  - `200 OK`: Login successful
  - `401 Unauthorized`: Invalid credentials

#### Logout
- **URL**: `/api/v1/auth/logout`
- **Method**: `DELETE`
- **Response**: Empty object
- **Status Codes**:
  - `204 No Content`: Logout successful

### User Management

#### Get Users List
- **URL**: `/api/v1/users`
- **Method**: `GET`
- **Authentication**: Required
- **Query Parameters**:
  - `limit` (integer, optional): Maximum number of users to return
  - `offset` (integer, optional): Number of users to skip
  - `order_by` (string, optional): Field to order by
  - `username` (string, optional): Filter by username
  - `phone` (string, optional): Filter by phone number
  - `created_from` (string, optional): Filter by creation date (from)
  - `created_to` (string, optional): Filter by creation date (to)
- **Response**:
  ```json
  {
    "limit": "integer",
    "offset": "integer",
    "total": "integer",
    "items": [
      {
        "id": "integer",
        "username": "string",
        "phone": "string",
        "created": "string"
      }
    ]
  }
  ```
- **Status Codes**:
  - `200 OK`: Users retrieved successfully
  - `401 Unauthorized`: Authentication required

#### Get User by ID
- **URL**: `/api/v1/users/<user_id>`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "phone": "string",
    "created": "string"
  }
  ```
- **Status Codes**:
  - `200 OK`: User retrieved successfully
  - `404 Not Found`: User not found
  - `401 Unauthorized`: Authentication required

#### Register User
- **URL**: `/api/v1/users`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "string",
    "phone": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "phone": "string",
    "created": "string"
  }
  ```
- **Status Codes**:
  - `201 Created`: User created successfully
  - `400 Bad Request`: User already exists with this username

#### Update User
- **URL**: `/api/v1/users/<user_id>`
- **Method**: `PUT`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "username": "string",
    "phone": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "phone": "string",
    "created": "string"
  }
  ```
- **Status Codes**:
  - `200 OK`: User updated successfully
  - `404 Not Found`: User not found
  - `401 Unauthorized`: Authentication required

#### Delete User
- **URL**: `/api/v1/users/<user_id>`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: Empty object
- **Status Codes**:
  - `204 No Content`: User deleted successfully
  - `404 Not Found`: User not found
  - `401 Unauthorized`: Authentication required

## Special Features

### Request Logging
The application automatically logs all authenticated requests, including:
- HTTP method used
- Endpoint accessed
- HTTP status code returned
- User ID who made the request

### Jalali Date Conversion
The system stores timestamps using Jalali (Persian) calendar format in the Asia/Tehran timezone.

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flask-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db upgrade
```

### Running the Application

Start the development server:
```bash
python3 main.py
```

The API will be available at http://localhost:5000

### Running Tests

Execute the test suite:
```bash
pytest
```
