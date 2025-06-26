#!/bin/bash

# Deploy script for Copyright Watermark Tool
# Run this on your Linux server

set -e

echo "🚀 Deploying Copyright Watermark Tool..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Install dependencies
echo "Installing dependencies..."
uv sync

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    if [ -f env.example ]; then
        cp env.example .env
    else
        echo "Warning: env.example not found, creating basic .env"
        cat > .env << EOF
ENV=production
SECRET_KEY=change-me-in-production
HOST=0.0.0.0
PORT=8080
DEBUG=false
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=output
EOF
    fi
    
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    sed -i "s/your-secret-key-change-in-production/$SECRET_KEY/" .env
    sed -i "s/ENV=development/ENV=production/" .env
    sed -i "s/DEBUG=true/DEBUG=false/" .env
    
    echo "⚠️  Please edit .env file to customize your settings"
fi

# Create directories
mkdir -p uploads output

# Set permissions
chmod 755 uploads output

echo "✅ Deployment complete!"
echo ""
echo "To run the application:"
echo "  uv run python main.py"
echo ""
echo "For systemd service:"
echo "  1. Edit copyright-app.service and update paths"
echo "  2. sudo cp copyright-app.service /etc/systemd/system/"
echo "  3. sudo systemctl enable copyright-app"
echo "  4. sudo systemctl start copyright-app"
echo ""
echo "For Docker:"
echo "  docker build -t copyright-app ."
echo "  docker run -p 8080:8080 copyright-app" 