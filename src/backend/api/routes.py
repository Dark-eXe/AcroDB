from fastapi import APIRouter, Query
from pydantic import BaseModel
from backend.core.session import get_dynamodb_resources
from backend.core.config import PROMPT_PATH
from backend.services.query_handler import handle_query

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    openai_api_key: str

@router.post("/query")
async def query_chatdb(
    request: QueryRequest,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=50)
):
    try:
        # Will only create once and cache globally
        resources = get_dynamodb_resources(request)
    except Exception as e:
        return {"error": f"Failed to initialize session: {str(e)}"}

    result, has_more = handle_query(
        query=request.query,
        acrodb_resources=resources,
        openai_key=request.openai_api_key,
        prompt_path=PROMPT_PATH,
        page=page,
        limit=limit
    )
    return {"result": result, "has_more": has_more}