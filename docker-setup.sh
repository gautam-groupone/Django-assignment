#!/bin/bash

echo "🚀 Setting up Grunge Django project with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Build the Docker image
echo "🔨 Building Docker image..."
make docker-build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
    
    # Run the containers
    echo "🚀 Starting the application..."
    make docker-run
    
    if [ $? -eq 0 ]; then
        echo "✅ Application started successfully!"
        echo ""
        echo "🌐 Your Django app is now running at: http://localhost:8001"
        echo "📚 Django admin: http://localhost:8001/admin"
        echo "🔌 API endpoints: http://localhost:8001/api/v1/"
        echo ""
        echo "📋 Useful commands:"
        echo "   make docker-stop    - Stop the application"
        echo "   make docker-run     - Start the application"
        echo "   make docker-build   - Rebuild the Docker image"
        echo ""
        echo "🔍 To view logs: docker-compose logs -f"
        echo "🛑 To stop: make docker-stop"
    else
        echo "❌ Failed to start the application"
        exit 1
    fi
else
    echo "❌ Failed to build Docker image"
    exit 1
fi
