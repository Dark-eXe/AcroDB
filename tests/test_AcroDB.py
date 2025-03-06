import boto3
import pytest
from src import AcroDB

table_name = "MAG_Code-of-Points"
bucket_name = "dsci551-acrobucket"

def test_constructor(test_object):
    if test_object:
        assert True

def test_getters(test_object):
    assert test_object.get_table().table_name == table_name
    assert test_object.get_bucket() == bucket_name

def test_setters(test_object):
    test_object.set_table(table_name="new_table")
    assert test_object.get_table().table_name == "new_table"

    test_object.set_bucket(bucket_name="new_bucket")
    assert test_object.get_bucket() == "new_bucket"

def test_get_item(test_object, test_mvtId):
    assert test_object.get_item(test_mvtId)["mvtId"] == test_mvtId

def test_put_item(test_object, test_mvtId):
    Item = test_object.get_item(test_mvtId)
    message = f"mvtId {test_mvtId} successfully inserted to {table_name}"
    assert test_object.put_item(Item=Item, force=False)["message"] == message

def test_s3url_insert(test_object, test_mvtId):
    message = f"mvtId {test_mvtId} successfully inserted to {table_name}"
    assert test_object.insert_s3_url(test_mvtId)["message"] == message