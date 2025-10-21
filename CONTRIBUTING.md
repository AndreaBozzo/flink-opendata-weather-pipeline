# Contributing to Flink OpenData Weather Pipeline

Thank you for your interest in contributing to this project!

## Development Setup

1. Fork the repository
2. Clone your fork locally
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

## Code Quality

Before submitting a pull request, ensure your code passes all quality checks:

```bash
# Format code
poetry run black .
poetry run isort .

# Run linting
poetry run flake8 .

# Run type checking
poetry run mypy .
```

## Testing

Run the test suite:

```bash
poetry run pytest
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass and code quality checks succeed
4. Update documentation if needed
5. Submit a pull request with a clear description of changes

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where applicable
- Write docstrings for all public functions and classes
- Keep functions focused and modular
- Maximum line length: 88 characters (Black default)

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add feature", "Fix bug")
- Reference issue numbers when applicable

## Questions?

Feel free to open an issue for any questions or suggestions!
