import requests

from tests.integration.test_export import EXPORT_ENDPOINT
from tests.integration.test_import import IMPORT_ENDPOINT
from tests.integration.utils import create_test_item, assert_first_page, assert_second_page, assert_updated_first_page


def test_should_create_update_and_delete_items():
    table_name = "TableName"
    # Creating 5 items
    data = {
        "table": table_name,
        "items": [
            create_test_item(1, "label-1"),
            create_test_item(2, "label-2"),
            create_test_item(3, "label-3"),
            create_test_item(4, "label-4"),
            create_test_item(5, "label-5")
        ]
    }

    response = requests.post(EXPORT_ENDPOINT, json=data)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body.get("unprocessed_items") == {}
    # Creating 6 items
    data = {
        "table": table_name,
        "items": [
            create_test_item(6, "label-6"),
            create_test_item(7, "label-7"),
            create_test_item(8, "label-8"),
            create_test_item(9, "label-9"),
            create_test_item(10, "label-10"),
            create_test_item(11, "label-11")
        ]
    }

    response = requests.post(EXPORT_ENDPOINT, json=data)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body.get("unprocessed_items") == {}
    # Fetching first page
    response = requests.post(IMPORT_ENDPOINT, json={
        "table": table_name
    })

    assert response.status_code == 200

    response_body = response.json()

    last_evaluated_key = response_body.get("last_evaluated_key")
    items = response_body.get("items")

    assert len(items) == 10
    assert_first_page(items)
    # Fetching second page
    response = requests.post(IMPORT_ENDPOINT, json={
        "table": table_name,
        "start_key": last_evaluated_key
    })

    assert response.status_code == 200

    response_body = response.json()

    items = response_body.get("items")

    assert len(items) == 1
    assert_second_page(items)
    # Updating item
    data = {
        "table": table_name,
        "items": [
            create_test_item(1, "new-label-1"),
        ]
    }

    response = requests.post(EXPORT_ENDPOINT, json=data)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body.get("unprocessed_items") == {}
    # Fetching first page
    response = requests.post(IMPORT_ENDPOINT, json={
        "table": table_name
    })

    assert response.status_code == 200

    response_body = response.json()

    last_evaluated_key = response_body.get("last_evaluated_key")
    items = response_body.get("items")

    assert len(items) == 10
    assert_updated_first_page(items)
    # Fetching second page
    response = requests.post(IMPORT_ENDPOINT, json={
        "table": table_name,
        "start_key": last_evaluated_key
    })

    assert response.status_code == 200

    response_body = response.json()

    items = response_body.get("items")

    assert len(items) == 1
    assert_second_page(items)
    # Deleting 5 items
    data = {
        "table": table_name,
        "items": [
            create_test_item(1, "label-1", deleted=True),
            create_test_item(2, "label-2", deleted=True),
            create_test_item(3, "label-3", deleted=True),
            create_test_item(4, "label-4", deleted=True),
            create_test_item(5, "label-5", deleted=True)
        ]
    }

    response = requests.post(EXPORT_ENDPOINT, json=data)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body.get("unprocessed_items") == {}
    # Deleting 6 items
    data = {
        "table": table_name,
        "items": [
            create_test_item(6, "label-6", deleted=True),
            create_test_item(7, "label-7", deleted=True),
            create_test_item(8, "label-8", deleted=True),
            create_test_item(9, "label-9", deleted=True),
            create_test_item(10, "label-10", deleted=True),
            create_test_item(11, "label-11", deleted=True)
        ]
    }

    response = requests.post(EXPORT_ENDPOINT, json=data)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body.get("unprocessed_items") == {}
    # Fetching first page
    response = requests.post(IMPORT_ENDPOINT, json={
        "table": table_name
    })

    assert response.status_code == 200

    response_body = response.json()

    items = response_body.get("items")

    assert len(items) == 0
