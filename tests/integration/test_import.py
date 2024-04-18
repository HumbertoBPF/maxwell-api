import random

import pytest
import requests

IMPORT_ENDPOINT = "http://localhost:3000/import"


def test_should_require_request_body():
    """Tests if the endpoint returns 400 Bad Request when no request body is sent"""
    response = requests.post(IMPORT_ENDPOINT)
    assert response.status_code == 400


def test_should_require_table_param():
    """Tests if the endpoint returns 400 Bad Request when an empty response body is sent"""
    response = requests.post(IMPORT_ENDPOINT, json={})
    assert response.status_code == 400


@pytest.mark.parametrize("table", [
    random.choice([True, False]),
    random.randint(1, 100),
    ""
])
def test_should_require_table_param_to_be_non_empty_string(table):
    """Tests if the endpoint returns 400 Bad Request when the table parameter is not a non-empty string"""
    response = requests.post(IMPORT_ENDPOINT, json={"table": table})
    assert response.status_code == 400


def test_should_not_accept_non_json_response_body():
    """Tests that the endpoint returns 400 Bad Request when the Content-Type is not application/json"""
    response = requests.post(IMPORT_ENDPOINT, data={"table": "TableName"})
    assert response.status_code == 400


def test_should_fetch_first_page_of_items():
    """Tests that the endpoint returns 200 Ok and the first page of items when the table parameter is a string"""
    response = requests.post(IMPORT_ENDPOINT, json={"table": "TableName"})

    assert response.status_code == 200

    response_body = response.json()

    assert "items" in response_body
    assert "last_evaluated_key" in response_body


def test_should_validate_start_key():
    """
    Tests that the endpoint returns 400 Bad Request when the start_key parameter has not the format
    {"table": {"S": value}, "id": {"S": value}}
    """
    response = requests.post(IMPORT_ENDPOINT, json={
        "table": "TableName",
        "start_key": "startKey"
    })
    assert response.status_code == 400


def test_should_fetch_items_starting_from_specified_key():
    """Tests that the endpoint returns 200 Ok and the items from the specified start key"""
    response = requests.post(IMPORT_ENDPOINT, json={
        "table": "TableName",
        "start_key": {
            "table": {"S": "TableName"},
            "id": {"S": "id"}
        }
    })

    assert response.status_code == 200

    response_body = response.json()

    assert "items" in response_body
    assert "last_evaluated_key" in response_body
