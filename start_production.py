#!/usr/bin/env python3
"""
Production startup script for CraveBreaker Telegram Bot
Optimized for Cloud Run deployment with enhanced error handling
"""

import os
import sys
import logging
from main import main

# Configure production logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_environment():
    """Check that all required environment variables are set"""
    required_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def start_production():
    """Start the application in production mode"""
    logger.info("Starting CraveBreaker Bot in production mode...")
    
    # Check environment
    if not check_environment():
        logger.error("Environment check failed. Exiting.")
        sys.exit(1)
    
    # Set production environment variables
    os.environ['DEBUG'] = 'false'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    try:
        # Start the main application
        main()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Production startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_production()