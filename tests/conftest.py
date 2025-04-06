import pytest
from unittest.mock import MagicMock, patch
from src.AcroDB import AcroDB

@pytest.fixture
def table_name():
    return "MAG_Code-of-Points"

@pytest.fixture
def bucket_name():
    return "dsci551-acrobucket"

@pytest.fixture
def mock_acrodb(table_name, bucket_name):
    with patch("src.AcroDB.boto3") as mock_boto:
        # Mock DynamoDB Table
        mock_dynamodb = mock_boto.resource.return_value
        mock_table = mock_dynamodb.Table.return_value
        mock_table.table_name = table_name

        # Mock S3 Bucket
        mock_s3 = mock_boto.client.return_value
        mock_s3_bucket = MagicMock()
        mock_s3_bucket.name = bucket_name

        # Mock AcroDB instance
        mock_acro = AcroDB(table_name=table_name)
        mock_acro.get_table = MagicMock(return_value=MagicMock(table_name=table_name))
        mock_acro.get_bucket = MagicMock(return_value=bucket_name)
        mock_acro.get_item = MagicMock(return_value={"event": "test_event", "mvtId": "test_mvtId"})
        mock_acro.insert_s3_url = MagicMock(return_value={"message": f"event, mvtId test_event, test_mvtId successfully inserted to {table_name}"})

        yield mock_acro
