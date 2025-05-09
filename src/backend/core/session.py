from boto3 import Session
from fastapi import Body
from ..models.request import QueryRequest
from AcroDB.AcroDB import AcroDB

from backend.core.cache import SessionCache
session_cache = SessionCache(ttl_seconds=3600)

def get_dynamodb_resources(request: QueryRequest = Body(...)) -> dict:
    """Return cached or fresh DynamoDB resources per user request."""
    user_key = f"{request.aws_access_key_id}:{request.aws_session_token}"

    cached_resources = session_cache.get(user_key)
    if cached_resources:
        return cached_resources

    # If token is expired, this will fail during session creation (safe fallback)
    session = Session(
        aws_access_key_id=request.aws_access_key_id,
        aws_secret_access_key=request.aws_secret_access_key,
        aws_session_token=request.aws_session_token,
        region_name="us-east-1"
    )
    dynamodb = session.resource("dynamodb")

    resources = {
        "MAG_Code-of-Points": AcroDB(table=dynamodb.Table("MAG_Code-of-Points")),
        "WAG_Code-of-Points": AcroDB(table=dynamodb.Table("WAG_Code-of-Points")),
        "Parkourpedia": AcroDB(table=dynamodb.Table("Parkourpedia")),
    }

    session_cache.set(user_key, resources)
    return resources
