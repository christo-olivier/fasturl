# Development Guide

## General Guidance

### Commands
- `uvicorn fasturl.main:app` - Start the development server
- `pytest ./tests` - Run tests
- `uv add <package_name>` - Add a package to the project
- `uv remove <package_name>` - Remove a package from the project
- `uv sync` - Update all packages in the project

### Documentation
The documentation is located in the `docs/` directory as well as in the @README.md file in the root directory.

## Rules

### Code Style
The coding style is defined in @.rules/code_style.md

### Project Rules
The project overview is defined in @.rules/project_overview.md

### Testing
The testing standards are defined in @.rules/testing.md

## Implementation Guidance

### API Endpoints
The API endpoints are defined in @product-requirements/api-endpoints.md

### Data Model
The data model is defined in @product-requirements/data-model.md

### Product Requirements
The product requirements are defined in @product-requirements/requirements.md
