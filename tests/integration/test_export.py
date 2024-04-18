import random

import pytest
import requests

EXPORT_ENDPOINT = "http://localhost:3000/export"


def test_should_require_request_body():
    """Tests that the endpoint returns 400 Bad Request when no request body is sent"""
    response = requests.post(EXPORT_ENDPOINT)
    assert response.status_code == 400


@pytest.mark.parametrize("missing_field", [
    "table",
    "items"
])
def test_should_validate_required_params(missing_field):
    """Tests that the endpoint returns 400 Bad Request when a required parameter is not sent"""
    data = {
        "table": "TableName",
        "items": []
    }

    del data[missing_field]

    response = requests.post(EXPORT_ENDPOINT, json=data)
    assert response.status_code == 400


@pytest.mark.parametrize("table", [
    random.choice([True, False]),
    random.randint(1, 100),
    ""
])
def test_should_require_table_param_to_be_non_empty_string(table):
    """Tests that the endpoint returns 400 Bad Request when the table parameter is not a non-empty string"""
    data = {
        "table": table,
        "items": []
    }
    response = requests.post(EXPORT_ENDPOINT, json=data)
    assert response.status_code == 400


@pytest.mark.parametrize("items", [
    random.choice([True, False]),
    random.randint(1, 100),
    "string",
    {"key": "value"}
])
def test_should_require_items_param_to_be_list(items):
    """Tests that the endpoint returns 400 Bad Request when the items parameter is not a list"""
    data = {
        "table": "TableName",
        "items": items
    }
    response = requests.post(EXPORT_ENDPOINT, json=data)
    assert response.status_code == 400


def test_should_not_accept_non_json_request_body():
    """Tests that the endpoint returns 400 Bad Request when the Content-Type header is not application/json"""
    data = {
        "table": "TableName",
        "items": []
    }
    response = requests.post(EXPORT_ENDPOINT, data=data)
    assert response.status_code == 400


def test_should_accept_an_empty_list_of_items():
    """Tests that the endpoint returns 200 Ok when an empty list of item is sent"""
    data = {
        "table": "TableName",
        "items": []
    }
    response = requests.post(EXPORT_ENDPOINT, json=data)

    assert response.status_code == 200

    response_body = response.json()

    assert response_body.get("unprocessed_items") == {}
