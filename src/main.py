from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AcroDB import AcroDB
from ChatDB import ChatDB
from ChatCache import ChatCache
from boto3 import Session

global session
session = None

# ChatCache
cache = ChatCache()

# FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class QueryRequest(BaseModel):
    query: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    openai_api_key: str

@app.post('/query')
async def query_chatdb(
    request: QueryRequest, 
    page: int = Query(1, alias="page", ge=1),
    limit: int = Query(5, alias="limit", ge=1, le=50)
):
    """Handles queries from the frontend."""

    global session, mag, parkour, wag, chat
    if session is None:
        print("Creating session.")
        try:
            session = Session(
                aws_access_key_id=request.aws_access_key_id,
                aws_secret_access_key=request.aws_secret_access_key,
                aws_session_token=request.aws_session_token,
                region_name="us-east-1"
            )
            dynamodb = session.resource("dynamodb")
        except Exception as e:
            import logging
            logging.error(f"Failed to initialize session: {str(e)}")
            return {"error": "An internal error occurred. Please try again later."}

        # Re-create AcroDB instances using user credentials
        mag = AcroDB(table=dynamodb.Table("MAG_Code-of-Points"))
        parkour = AcroDB(table=dynamodb.Table("Parkourpedia"))
        wag = AcroDB(table=dynamodb.Table("WAG_Code-of-Points"))

        # New ChatDB using the user's OpenAI key
        chat = ChatDB(acrodb_list=[mag, parkour, wag])
        chat.set_api_key(API_KEY=request.openai_api_key)
        chat.set_prompt(prompt_path="prompts/main.txt")

    # Run translation + caching
    response = chat.translate_chat(request.query)
    print("Translation:")
    print(request.query)
    print("--> " + str(response))
    if response in cache.cache_sequence:
        result = cache.cache_response[response]
    else:
        result = chat.exec_items(chat.exec_response(response))
        cache.addPair(response=response, result=result)

    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_results = result[start_idx:end_idx]
    has_more = end_idx < len(result)

    return {"result": paginated_results, "has_more": has_more}