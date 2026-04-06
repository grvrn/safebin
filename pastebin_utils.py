import requests
import os

API_POST_URL = "https://pastebin.com/api/api_post.php"
API_RAW_URL = "https://pastebin.com/raw/"

def post_to_pastebin(content, name=None, format="text", private=0, expire="1H"):
    """
    Posts content to Pastebin using API Key from environment.
    
    Args:
        content (str): The body of the paste.
        name (str, optional): Title of the paste.
        format (str, optional): Syntax highlighting. Defaults to 'text'.
        private (int, optional): 0 = public, 1 = unlisted, 2 = private. Defaults to 0.
        expire (str, optional): Expiration time. Defaults to '1H'.
    """
    api_dev_key = os.getenv("PASTEBIN_API_DEV_KEY")
    if not api_dev_key:
        return "Error: PASTEBIN_API_DEV_KEY not found in environment."

    data = {
        'api_dev_key': api_dev_key,
        'api_option': 'paste',
        'api_paste_code': content,
        'api_paste_name': name,
        'api_paste_format': format,
        'api_paste_private': private,
        'api_paste_expire_date': expire
    }
    
    response = requests.post(API_POST_URL, data=data)
    return response.text

def get_from_pastebin(paste_key):
    """
    Retrieves raw content from a public/unlisted Pastebin paste.
    
    Args:
        paste_key (str): The unique ID of the paste (found in its URL).
        
    Returns:
        str: Raw paste content, or an error if not found/accessible.
    """
    response = requests.get(f"{API_RAW_URL}{paste_key}")
    return response.text