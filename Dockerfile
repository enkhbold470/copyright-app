FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Create app directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY . .

# Install dependencies
RUN uv sync --frozen

# Create uploads and output directories
RUN mkdir -p uploads output

# Set environment variables
ENV ENV=production
ENV HOST=0.0.0.0
ENV PORT=8080
ENV DEBUG=false

# Expose port
EXPOSE 8080

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Run the application
CMD ["uv", "run", "python", "main.py"] 