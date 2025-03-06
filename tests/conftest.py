import pytest
from src import AcroDB


@pytest.fixture
def test_object():
    return AcroDB(table_name="MAG_Code-of-Points", bucket_name="dsci551-acrobucket")