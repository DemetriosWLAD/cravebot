#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CraveBreaker Telegram Bot - Cloud Run Deployment Entry Point
This file serves as the main entry point for Cloud Run deployment,
providing health checks and running the Telegram bot.
"""

import asyncio
import logging
import os
import threading
from flask import Flask, jsonify, send_file, render_template_string
from simple_bot import SimpleCraveBreakerBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create Flask app for health checks
app = Flask(__name__)

# Global bot instance
bot_instance = None
bot_task = None

@app.route('/')
def health_check():
    """Health check endpoint for Cloud Run deployment"""
    return jsonify({
        'status': 'healthy',
        'service': 'CraveBreaker Telegram Bot',
        'version': '1.0.0'
    }), 200

@app.route('/health')
def health():
    """Alternative health check endpoint"""
    return jsonify({'status': 'ok'}), 200

@app.route('/status')
def status():
    """Bot status endpoint"""
    global bot_instance
    return jsonify({
        'bot_status': 'running' if bot_instance else 'not_started',
        'bot_token_configured': bool(os.getenv('TELEGRAM_BOT_TOKEN'))
    }), 200

@app.route('/files')
def download_page():
    """Page for downloading deployment files"""
    download_html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CraveBreaker - Скачать файлы</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
            .container { background: white; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; margin-bottom: 30px; }
            .download-btn { 
                display: inline-block; 
                background: #3498db; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-size: 18px; 
                margin: 10px;
                transition: background 0.3s;
            }
            .download-btn:hover { background: #2980b9; }
            .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 CraveBreaker Bot - Файлы для развертывания</h1>
            <div class="success">
                ✅ Готовый архив для развертывания на облачных платформах
            </div>
            <a href="/download" class="download-btn">📦 Скачать CraveBreaker_Deploy.zip</a>
            <p>Архив содержит все необходимые файлы для развертывания бота на Render, Railway, Koyeb и других платформах.</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(download_html)

@app.route('/download')
def download_zip():
    """Download deployment archive"""
    zip_path = "CraveBreaker_Deploy.zip"
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True, download_name="CraveBreaker_Deploy.zip")
    else:
        return "Архив не найден. Файл может быть в процессе создания.", 404

def run_bot_async():
    """Run the Telegram bot in async context"""
    global bot_instance, bot_task
    
    async def start_bot():
        bot_instance = SimpleCraveBreakerBot()
        
        # Check if bot token is configured
        if not bot_instance.bot_token:
            logger.error("TELEGRAM_BOT_TOKEN is not configured!")
            return
            
        logger.info("Starting CraveBreaker Telegram Bot...")
        
        # Initialize database
        await bot_instance.init_db()
        
        # Start bot polling
        await bot_instance.run_bot()
    
    # Create new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        bot_task = loop.create_task(start_bot())
        loop.run_until_complete(bot_task)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        loop.close()

def start_bot_in_thread():
    """Start the bot in a separate thread"""
    bot_thread = threading.Thread(target=run_bot_async, daemon=True)
    bot_thread.start()
    logger.info("Bot thread started")
    return bot_thread

if __name__ == "__main__":
    # Start the Telegram bot in a separate thread
    start_bot_in_thread()
    
    # Start Flask server for health checks
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Always bind to all interfaces for Cloud Run
    
    logger.info(f"Starting Flask health check server on {host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)