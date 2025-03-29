from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AcroDB import AcroDB
from ChatDB import ChatDB
from ChatCache import ChatCache

# AcroDB
table_name, bucket_name = "MAG_Code-of-Points", "dsci551-acrobucket"
acro1 = AcroDB(table_name=table_name, bucket_name=bucket_name)

table_name, bucket_name = "Parkourpedia", "dsci551-acrobucket"
acro2 = AcroDB(table_name=table_name, bucket_name=bucket_name)

# ChatDB
chat = ChatDB(acrodb_list=[acro1, acro2])
chat.set_api_key(API_KEY=open("../secrets/API_KEY").read())
chat.set_prompt(prompt_path="prompts/main.txt")

# ChatCache
cache = ChatCache()

# FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify ["http://localhost:3000"] for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class QueryRequest(BaseModel):
    query: str

@app.post('/query')
async def query_chatdb(
        request: QueryRequest, 
        page: int = Query(1, alias="page", ge=1),
        limit: int = Query(5, alias="limit", ge=1, le=50)
    ):
    """Handles queries from the frontend."""
    response = chat.translate_chat(request.query)
    if response in cache.cache_sequence:
        result = cache.cache_response[response]
    else:
        result = chat.exec_items(chat.exec_response(response))
        cache.addPair(response=response, result=result)

    # Pagination logic: Slice results
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_results = result[start_idx:end_idx]

    # Determine if more results exist
    has_more = end_idx < len(result)

    return {"result": paginated_results, "has_more": has_more}