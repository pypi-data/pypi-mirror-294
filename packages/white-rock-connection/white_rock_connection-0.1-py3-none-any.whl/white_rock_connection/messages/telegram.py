import os
import requests
import logging

class TelegramMessages:
    def __init__(self, token=None, chat_id=None):
        """
        Initializes the TelegramMessages class.

        :param token: Optional Telegram bot token. If not provided, it will use the token from environment variables.
        :param chat_id: Optional Telegram chat ID. If not provided, it will use the chat ID from environment variables.
        """
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
        if not self.token or not self.chat_id:
            raise ValueError("Both token and chat_id must be provided either as parameters or via environment variables.")
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def send(self, message, log = False):
        """
        Sends a message to the specified Telegram chat.

        :param message: The message to be sent.
        """
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message
            }
            response = requests.post(url, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            if log:
            	self.logger.info(f"Message sent successfully: {message}")
        except requests.RequestException as error:
            self.logger.critical(f"Error while sending Telegram message: {error}")


