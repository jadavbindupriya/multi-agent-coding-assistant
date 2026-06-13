# Coding Standards

## Python Style
- Follow PEP 8 naming conventions
- Use type hints on all function signatures
- Add docstrings to all public functions and classes
- Maximum line length: 88 characters

## Error Handling
- Use specific exception types, never bare `except:`
- Validate inputs at function boundaries
- Return meaningful error messages

## Testing
- Write pytest tests for all functions
- Include edge cases: empty input, None, negative values
- Use property-based testing with hypothesis for complex logic
- Aim for 70%+ code coverage

## Security
- Never use eval() or exec() on user input
- Sanitize all external data
- Use parameterized queries for database access
