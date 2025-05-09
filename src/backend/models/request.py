from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    openai_api_key: str