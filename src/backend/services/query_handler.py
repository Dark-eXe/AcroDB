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

def rewrite_multimedia_urls(items: list[dict]) -> list[dict]:
    """Attach CloudFront base URL to image paths unless already full URLs (e.g., Instagram)."""
    for item in items:
        url = item.get("image_s3_url")
        if url:
            parsed_url = urlparse(url)
            if parsed_url.hostname != "www.instagram.com":
                item["image_s3_url"] = f"{CLOUDFRONT_BASE_URL}/{url}"
    return items

def handle_query(query, acrodb_resources, openai_key, prompt_path, page, limit):
    """Translate user query, execute it, paginate, and rewrite image URLs."""
    chat = ChatDB(acrodb_list=list(acrodb_resources.values()))
    chat.set_api_key(API_KEY=openai_key)
    chat.set_prompt(prompt_path=prompt_path)

    response = chat.translate_chat(query)
    print(f"--> {response}")

    if response in cache.cache_sequence:
        result = cache.cache_response[response]
    else:
        result = chat.exec_items(chat.exec_response(response))
        cache.addPair(response=response, result=result)

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated = result[start_idx:end_idx]

    return rewrite_multimedia_urls(paginated), end_idx < len(result)