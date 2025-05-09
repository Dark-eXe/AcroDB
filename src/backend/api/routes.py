from fastapi import APIRouter, Query, Body, Depends
from backend.core.session import get_dynamodb_resources
from backend.core.config import PROMPT_PATH
from backend.models.request import QueryRequest
from backend.services.query_handler import handle_query
import logging

router = APIRouter()

@router.post("/query")
async def query_chatdb(
    request: QueryRequest = Body(...),
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=50),
    resources: dict = Depends(get_dynamodb_resources)
):
    print("Query:", request.query)
    logger = logging.getLogger(__name__)
    logger.info(f"User {request.aws_access_key_id} submitted: {request.query}")

    result, has_more = handle_query(
        query=request.query,
        acrodb_resources=resources,
        openai_key=request.openai_api_key,
        prompt_path=PROMPT_PATH,
        page=page,
        limit=limit
    )
    return {"result": result, "has_more": has_more}
