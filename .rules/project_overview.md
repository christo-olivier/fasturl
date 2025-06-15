# Project Overview

## Stack
- Python
- FastAPI
- Pydantic
- SQLite

## Directory Structure
```bash
docs/       # Documentation
src/        # Source code
├── fasturl/         # Main application package
    ├── static/      # Static files
    ├── adapters.py  # Implementations of interfaces as repositories or adapters
    ├── config.py    # Configuration from env variables
    ├── interfaces.py  # Interfaces as abstract base classes with their own custom exceptions where appropriate
    ├── main.py        # Main entry point
    ├── models.py      # Data models
    ├── routes.py      # HTTP endpoints
    ├── services.py    # Business logic
tests/      # Unit and integration tests
```

## Configuration Management
- All configuration is read either from environment variables, `.env` files, or docker secrets mounted on the file system
- Pydantic Settings are used to validate and load the configuration

## Key Principles
- Security-first approach
- Clean code practices
- Async by default

## Linting and Type Checking
- Ruff for linting
- Mypy for type checking

## Git Commits
- Use conventional commit prefixes (feat:, fix:, etc.)
- Keep messages concise and reference issues

## Security
- No secrets in code
- Validate inputs
- Encrypt sensitive data
