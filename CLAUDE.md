# Development Guide

## General Guidance

### Commands
- `mypy src/fasturl` - Run type checker on fasturl package
- `mypy tests` - Run type checker on tests
- `mypy .` - Run type checker on all code
- `uvicorn fasturl.main:app` - Start the development server
- `pytest ./tests` - Run tests
- `ruff check src/fasturl` - Run linter on fasturl package
- `ruff check tests` - Run linter on tests
- `ruff check .` - Run linter on all code
- `uv add <package_name>` - Add a package to the project
- `uv remove <package_name>` - Remove a package from the project
- `uv sync` - Update all packages in the project

### Documentation
The documentation is located in the `docs/` directory as well as in the @README.md file in the root directory.

## Rules

### Code Style
The coding style is defined in @rules/code_style.md

### Project Rules
The project overview is defined in @rules/project_overview.md

### Testing
The testing guidance is defined in @rules/testing.md

## Implementation Guidance

### API Endpoints
The API endpoints are defined in @product-requirements/api-endpoints.md

### Data Model
The data model is defined in @product-requirements/data-model.md

### Product Requirements
The product requirements are defined in @product-requirements/requirements.md
