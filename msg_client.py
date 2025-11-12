import os
import requests

# Default API endpoints 
MESSAGES_URL = os.getenv(
    "MESSAGE_URL",
    "https://november7-730026606190.europe-west1.run.app/messages"
)

def fetch_messages():
    """
    Fetch message from the public API
    Returns a llist of message dictionaries
    """
    r = requests.get(MESSAGES_URL, timeout=30)
    r.raise_for_status()
    data = r.json()

    if isinstance(data,dict) and "messages" in data:
        return data["messages"]
    return data