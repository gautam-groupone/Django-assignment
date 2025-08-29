#!/bin/bash
set -e

echo "Running Django tests with pytest..."
pytest -v --tb=short

echo "Tests completed successfully!"
