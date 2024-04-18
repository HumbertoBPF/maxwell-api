def create_test_item(pk, label, deleted=False):
    return {"id": pk, "label": label, "deleted": deleted}


def assert_test_item(item, pk, label):
    assert item["id"] == pk
    assert item["label"] == label
    assert item["deleted"] == "False"


def assert_first_page(items):
    assert_test_item(items[0], "1", "label-1")
    assert_test_item(items[1], "10", "label-10")
    assert_test_item(items[2], "11", "label-11")
    assert_test_item(items[3], "2", "label-2")
    assert_test_item(items[4], "3", "label-3")
    assert_test_item(items[5], "4", "label-4")
    assert_test_item(items[6], "5", "label-5")
    assert_test_item(items[7], "6", "label-6")
    assert_test_item(items[8], "7", "label-7")
    assert_test_item(items[9], "8", "label-8")


def assert_second_page(items):
    assert_test_item(items[0], "9", "label-9")


def assert_updated_first_page(items):
    assert_test_item(items[0], "1", "new-label-1")
    assert_test_item(items[1], "10", "label-10")
    assert_test_item(items[2], "11", "label-11")
    assert_test_item(items[3], "2", "label-2")
    assert_test_item(items[4], "3", "label-3")
    assert_test_item(items[5], "4", "label-4")
    assert_test_item(items[6], "5", "label-5")
    assert_test_item(items[7], "6", "label-6")
    assert_test_item(items[8], "7", "label-7")
    assert_test_item(items[9], "8", "label-8")
