import pytest
from unittest.mock import MagicMock
from src import AcroDB

def test_constructor(mock_acrodb):
    assert mock_acrodb is not None

def test_getters(mock_acrodb, table_name, bucket_name):
    assert mock_acrodb.get_table().table_name == table_name
    assert mock_acrodb.get_bucket() == bucket_name

@pytest.mark.parametrize(
    "new_table_name, new_bucket_name", 
    [("yin_table", "yin_bucket"), ("yan_table", "yan_bucket")]
)
def test_setters(mock_acrodb, new_table_name, new_bucket_name):
    # Mock setters
    mock_acrodb.set_table = MagicMock()
    mock_acrodb.set_bucket = MagicMock()

    # Set new values dynamically
    mock_acrodb.set_table(table_name=new_table_name)
    mock_acrodb.set_bucket(bucket_name=new_bucket_name)

    # Mock return values for getters
    mock_acrodb.get_table.return_value.table_name = new_table_name
    mock_acrodb.get_bucket.return_value = new_bucket_name

    # Assertions
    assert mock_acrodb.get_table().table_name == new_table_name
    assert mock_acrodb.get_bucket() == new_bucket_name

def test_get_item(mock_acrodb):
    assert mock_acrodb.get_item("test_mvtId")["mvtId"] == "test_mvtId"

def test_put_item(mock_acrodb, table_name):
    message = f"mvtId test_mvtId successfully inserted to {table_name}"
    assert mock_acrodb.put_item(Item={"mvtId": "test_mvtId"}, force=False)["message"] == message

def test_s3url_insert(mock_acrodb, table_name):
    message = f"mvtId test_mvtId successfully inserted to {table_name}"
    assert mock_acrodb.insert_s3_url("test_mvtId")["message"] == message
