import pytest
from selenium import webdriver

@pytest.fixture()
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

#Custom command-line option for pytest
def pytest_addoption(parser):
    parser.addoption("--xray-keys", action="store", default="")

#Select tests for execution by xray mark 
def pytest_collection_modifyitems(config, items):
    test_keys = config.getoption("--xray-keys").split(",")
    if not test_keys or test_keys == [""]:
        return 
    
    selected_items = []
    deselected_items = []

    for item in items:
        marker = item.get_closest_marker("xray")
        if marker:
            test_key = marker.kwargs.get("test_key")
            if test_key:
                item._nodeid = f"{test_key}"

            if test_key in test_keys:
                selected_items.append(item)
            else: 
                deselected_items.append(item)
        else:
            deselected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items