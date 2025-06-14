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
    ├── static      # Static files
    ├── adapters.py  # Implementations of interfaces and repositories
    ├── config.py    # Configuration
    ├── interfaces.py  # Interfaces and custom exceptions
    ├── main.py        # Main entry point
    ├── models.py      # Data models
    ├── routes.py      # Routing and HTTP endpoints
    ├── services.py    # Business logic
tests/      # Unit and integration tests
```

## Key Principles
- Security-first approach
- Clean code practices
- Async by default

## Git Commits
- Use conventional commit prefixes (feat:, fix:, etc.)
- Keep messages concise and reference issues

## Security
- No secrets in code
- Validate inputs
- Encrypt sensitive data
