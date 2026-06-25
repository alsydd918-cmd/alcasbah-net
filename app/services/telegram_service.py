import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def send_telegram_message(message, chat_id=None):
    """Send message to Telegram"""
    if not current_app.config.get('TELEGRAM_BOT_TOKEN'):
        logger.warning('Telegram bot token not configured')
        return False
    
    if not chat_id:
        chat_id = current_app.config.get('TELEGRAM_CHAT_ID')
    
    if not chat_id:
        logger.warning('Telegram chat ID not configured')
        return False
    
    try:
        url = f'https://api.telegram.org/bot{current_app.config["TELEGRAM_BOT_TOKEN"]}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f'Error sending telegram message: {e}')
        return False

def send_telegram_photo(photo_path, caption, chat_id=None):
    """Send photo to Telegram"""
    if not current_app.config.get('TELEGRAM_BOT_TOKEN'):
        return False
    
    if not chat_id:
        chat_id = current_app.config.get('TELEGRAM_CHAT_ID')
    
    try:
        url = f'https://api.telegram.org/bot{current_app.config["TELEGRAM_BOT_TOKEN"]}/sendPhoto'
        files = {'photo': open(photo_path, 'rb')}
        payload = {
            'chat_id': chat_id,
            'caption': caption
        }
        response = requests.post(url, files=files, data=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f'Error sending telegram photo: {e}')
        return False
