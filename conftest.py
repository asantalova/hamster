import json
import pytest
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Service
from webdriver_manager.chrome import ChromeDriverManager

#Store test results globally
test_results = []
node_to_xray = {} # mapping of test nodeid to xray id
start_time = None # session start time


#======================FIXTURES======================

@pytest.fixture()
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-gpu") # for CI/CD
    #chrome_options.add_argument("--no sandbox") # for CI/CD
    #chrome_options.add_argument("disable-dev-shm-usage") # for CI/CD
    #chrome_options.binary_location = "/usr/bin/chromium-browser"
    service = Service(ChromeDriverManager.install())
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


#======================HELPERS======================
#Custom command option for pytest
def pytest_addoption(parser):
    parser.addoption("--xray-keys", action="store", default="")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    global start_time
    start_time = time.time()

#======================XRAY MARK======================

#Select tests for execution by xray mark 
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    test_keys = config.getoption("--xray-keys").split(",") 
    
    selected_items = []
    deselected_items = []

    for item in items:
        marker = item.get_closest_marker("xray")
        if marker:
            test_key = marker.kwargs.get("test_key")
            node_to_xray[item._nodeid] = marker.kwargs["test_key"]
            #if test_key:
            #    item._nodeid = f"{test_key}"

            if test_keys and test_keys != [""]:
                if test_key in test_keys:
                    selected_items.append(item)
                else: 
                    deselected_items.append(item)
            else:
                selected_items.append(item)
        else:
            deselected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items

#======================TEST LOGGING HOOKS======================

# Capture test results
def pytest_runtest_logreport(report):

    if report.when == "call":
        test_name = node_to_xray.get(report.nodeid, report.nodeid)
        test_info = {
            "test": test_name,
            "location": report.nodeid,
            "outcome": report.outcome,
            "duration": round(report.duration,2)
        }

        if report.failed:
            error_msg = str(report.longrepr).splitlines()[-1]
            failed_line = next (
                (line.strip() for line in str(report.longrepr).splitlines() if "assert" in line), 
                "No assertion found"
            )

            failed_line = re.sub(r'\s+', ' ', failed_line.strip())

            test_info["error"] = {
                "message": error_msg, #short failure message
                "failed_line": failed_line #the exact failed assertion
            }
        
        if report.skipped:
            test_info["skip_reason"] = report.longrepr[2]

        test_results.append(test_info)

# Summary at the end of a session
def pytest_sessionfinish(session, exitstatus):

    total_duration = round(time.time() - start_time, 2)

    summary = {
        "total_tests": session.testscollected,
        "passed": sum (1 for t in test_results if t["outcome"] == "passed"),
        "failed": sum (1 for t in test_results if t["outcome"] == "failed"),
        "skipped": sum (1 for t in test_results if t["outcome"] == "skipped"),
        "exit_status": exitstatus, # 0 - all passed successfully, 1 - at least one failed
        "total_execution_time": total_duration,
        "tests": test_results
    }

    with open("test_results.json", "w") as f:
        json.dump(summary, f, indent=4)
