# dimo-python-sdk

Python SDK for the DIMO platform. Published to PyPI as `dimo-python-sdk`.

## Stack
- Python 3.8+, setuptools
- Dependencies: requests, eth-account, eth-utils
- Testing: pytest

## Key Commands
```bash
# Setup
pip install -r requirements.txt
pip install -e .              # install locally in editable mode

# Test
pytest                        # run all tests
pytest -v                     # verbose output
pytest tests/test_dimo.py -v  # run specific file

# Publish (maintainers only)
python -m build
twine upload dist/*
```

## Project Structure
```
dimo/         # Main SDK package
  __init__.py
  ...
tests/        # pytest test suite
  test_dimo.py
  test_conversations.py
  test_errors.py
  test_permission_decoder.py
  test_request.py
pyproject.toml  # package metadata and build config
requirements.txt
```

## Development Guidelines
- Public API changes require version bump in `pyproject.toml`
- All new functionality needs corresponding tests
- Test coverage covers: auth, API endpoints, GraphQL queries, error handling
- Supports Python 3.8+ — avoid syntax or stdlib features newer than 3.8

## Gotchas
- eth-account version is pinned (`==0.13.4`) — don't change without testing wallet flows
- Run `pytest` before any PR — CI will fail on test failures
- The SDK talks to live DIMO APIs in integration tests; use mocks for unit tests
