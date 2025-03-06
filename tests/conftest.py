import pytest
from src import AcroDB

table_name = "MAG_Code-of-Points"
bucket_name = "dsci551-acrobucket"

@pytest.fixture
def test_object():
    return AcroDB(table_name=table_name, bucket_name=bucket_name)
    
@pytest.fixture
def test_mvtId():
    return "1"