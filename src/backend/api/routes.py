from fastapi import APIRouter, Request, Query, Depends
from backend.models.request import QueryRequest
from backend.services.query_handler import handle_query
from backend.core.session import get_dynamodb_resources
from backend.core.config import PROMPT_PATH
from backend.core.rate_limit import limiter
import logging

router = APIRouter()

@router.post("/query")
@limiter.limit("12/minute")
async def query_chatdb(
    request: Request,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    resources: dict = Depends(get_dynamodb_resources)
):
    body_dict = await request.json()
    body = QueryRequest(**body_dict)

    logger = logging.getLogger(__name__)
    logger.info(f"User {body.aws_access_key_id} submitted: {body.query}")

    result, has_more = handle_query(
        query=body.query,
        acrodb_resources=resources,
        openai_key=body.openai_api_key,
        prompt_path=PROMPT_PATH,
        page=page,
        limit=limit
    )
    return {"result": result, "has_more": has_more}
