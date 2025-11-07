# Tests for AI for the Soul Newsletter

This directory contains tests for the Christianity newsletter generator.

## Setup

1. Make sure you have pytest installed:
   ```bash
   pip install pytest python-dotenv
   ```

2. Create a `.env` file in the project root with your API keys:
   ```bash
   cp .env.example .env
   # Then edit .env with your actual keys
   ```

## Running Tests

Run all tests:
```bash
pytest tests/
```

Run tests with verbose output:
```bash
pytest tests/ -v
```

Run a specific test file:
```bash
pytest tests/test_api_keys.py -v
```

Run tests and see print statements:
```bash
pytest tests/ -v -s
```

## Test Files

- `test_api_keys.py` - Tests that API keys are properly configured
- `test_researcher_basic.py` - Basic functionality tests for the researcher module

## Adding New Tests

When adding new tests:
1. Create a new file starting with `test_`
2. Use clear, descriptive function names
3. Add docstrings explaining what each test does
4. Use pytest fixtures for shared setup/teardown

## CI/CD

These tests will run automatically in GitHub Actions before deploying the newsletter.
