from boto3 import Session

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))) # add abspath of src/ to runtime import search path
from AcroDB.AcroDB import AcroDB

_session = None
_resources = None

def get_dynamodb_resources(request=None):
    global _session, _resources

    if _resources is not None:
        return _resources

    if request is None:
        raise ValueError("Request is required to initialize session for the first time.")

    _session = Session(
        aws_access_key_id=request.aws_access_key_id,
        aws_secret_access_key=request.aws_secret_access_key,
        aws_session_token=request.aws_session_token,
        region_name="us-east-1"
    )
    dynamodb = _session.resource('dynamodb')
    
    _resources = {
        "MAG": AcroDB(table=dynamodb.Table("MAG_Code-of-Points")),
        "WAG": AcroDB(table=dynamodb.Table("WAG_Code-of-Points")),
        "Parkourpedia": AcroDB(table=dynamodb.Table("Parkourpedia"))
    }

    return _resources