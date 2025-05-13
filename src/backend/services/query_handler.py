import sys
import os
from urllib.parse import urlparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from AcroDB.ChatDB import ChatDB
from AcroDB.ChatCache import ChatCache

# Global cache
cache = ChatCache()

# CloudFront base URL for multimedia assets
CLOUDFRONT_BASE_URL = "https://d1qh8wrq6r4xyn.cloudfront.net"

key_mapping = {
    "mvtId": "ID", 
    "event": "Event",
    "description": "Description",
    "difficulty": "Difficulty",
    "value": "Value",
    "group": "Group"}
def rename_keys(my_dict: dict, key_mapping: dict=key_mapping) -> None:
    """Renames keys in a dictionary based on a provided mapping."""
    for old_key, new_key in key_mapping.items():
        if old_key in my_dict:
            my_dict[new_key] = my_dict.pop(old_key)

def is_full_url(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except:
        return False

def prep_items(items: list[dict]) -> list[dict]:
    for item in items:
        if isinstance(item, dict):
            url = item.get("image_s3_url")
            if url and not is_full_url(url):
                item["image_s3_url"] = f"{CLOUDFRONT_BASE_URL}/{url}"
            rename_keys(item)
    return items

def handle_query(query, acrodb_resources, openai_key, prompt_path, page, limit):
    """Translate user query, execute it, paginate, and rewrite image URLs."""
    chat = ChatDB(acrodb_list=list(acrodb_resources.values()))
    chat.set_api_key(API_KEY=openai_key)
    chat.set_prompt(prompt_path=prompt_path)

    response = chat.translate_chat(query)
    print(f"--> {response}")

    if response not in cache.cache_response:
        full_result = chat.exec_items(chat.exec_response(response))
        cache.addPair(response=response, result=full_result)

    result = cache.cache_response[response]

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated = result[start_idx:end_idx]
    
    return prep_items(paginated), end_idx < len(result)