from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AcroDB import AcroDB
from ChatDB import ChatDB

# AcroDB
table_name, bucket_name = "MAG_Code-of-Points", "dsci551-acrobucket"
acro1 = AcroDB(table_name=table_name, bucket_name=bucket_name)

table_name, bucket_name = "Parkourpedia", "dsci551-acrobucket"
acro2 = AcroDB(table_name=table_name, bucket_name=bucket_name)

# ChatDB
chat = ChatDB(acrodb_list=[acro1, acro2])
chat.set_api_key(API_KEY=open("../secrets/API_KEY").read())
chat.set_prompt(prompt_path="prompts/main.txt")

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
async def query_chatdb(request: QueryRequest):
    """Handles queries from the frontend."""
    response = chat.translate_chat(request.query)
    result = chat.exec_items(chat.exec_response(response))
    return {"result": result}