## Development Setup
```bash
# Install dependencies
poetry install

# Run migrations
poetry run alembic upgrade head

# Start server
poetry run fastapi dev app/main.py
```

## Testing
```bash
# Run unit tests
poetry run pytest tests/

# Run integration tests
poetry run pytest tests/test_integration.py
```