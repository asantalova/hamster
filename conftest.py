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
        case_tag_marker = item.get_closest_marker("case_tag")
        if case_tag_marker:
            tag_name = case_tag_marker.args[0]
            item._nodeid = f"{tag_name}"