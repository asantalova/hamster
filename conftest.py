import pytest
from selenium import webdriver

@pytest.fixture()
def browser():
    driver = webdriver.Chrome() # to connect to Selenium Grid use driver.remote() and Grid URL
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

#Modify test nodes IDs
def pytest_collection_modifyitems(items):
    for item in items:
        test_marker = item.get_closest_marker("xray")
        if test_marker:
            tag_name = test_marker.args[0]
            item._nodeid = f"{tag_name}"

#Custom command-line option for pytest
def pytest_addoption(parser):
    parser.addoption("--xray-keys", action="store", default="")

#Select tests for execution by xray mark 
def pytest_collection_modifyitems(config, items):
    test_keys = config.getoption("--xray-keys").split(",")

    selected_items = []
    deselected_items = []

    for item in items:
        marker = item.get_closest_marker("xray")
        if marker:
            test_key = marker.kwargs.get("test_key")

            if test_key in test_keys:
                selected_items.append(item)
            else: 
                deselected_items.append(item)
        else:
            deselected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items