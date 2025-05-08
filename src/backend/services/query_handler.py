import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))) # add abspath of src/ to runtime import search path
from AcroDB.ChatDB import ChatDB
from AcroDB.ChatCache import ChatCache

cache = ChatCache()

def handle_query(query, acrodb_resources, openai_key, prompt_path, page, limit):
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
    paginated_results = result[start_idx:end_idx]
    has_more = end_idx < len(result)

    return paginated_results, has_more