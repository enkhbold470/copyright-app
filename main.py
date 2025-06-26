#!/usr/bin/env python3
"""
Main entry point for the Copyright Watermark Tool
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app import app, logger, config

def main():
    """Main function to run the application"""
    try:
        logger.info(f"Starting Copyright Watermark Tool in {config.ENV} mode")
        logger.info(f"Debug mode: {config.DEBUG}")
        logger.info(f"Host: {config.HOST}, Port: {config.PORT}")
        
        # Run the Flask app
        app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
