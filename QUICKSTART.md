# Quick Start Guide

Need to get this running right now? Here's the fastest way.

## Development (local testing)

```bash
# Clone the repo
git clone https://github.com/enkhbold470/copyright-app
cd copyright-app

# Install dependencies
uv sync

# Copy environment file
cp env.example .env

# Run it
uv run python main.py
```

Go to `http://localhost:8080` and you're done.

## Production (actual server)

```bash
# On your Linux server
git clone <repo-url>
cd copyright-app

# Run the deploy script
./deploy.sh

# Start the app
uv run python main.py
```

Or use systemd:

```bash
# Edit the service file first
nano copyright-app.service
# Change all "/path/to/copyright-app" to your actual path

# Install service
sudo cp copyright-app.service /etc/systemd/system/
sudo systemctl enable copyright-app
sudo systemctl start copyright-app
```

## Docker (easiest for production)

```bash
# Build and run
docker build -t copyright-app .
docker run -d -p 8080:8080 --name copyright-app copyright-app

# Or with custom port
docker run -d -p 3000:8080 --name copyright-app copyright-app
```

## Environment variables

Copy `env.example` to `.env` and change:

- `SECRET_KEY`: Make it random
- `ENV`: Set to `production` for live servers
- `DEBUG`: Set to `false` for production
- `PORT`: Change if you need a different port

That's it. Simple as that. 