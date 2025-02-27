import os
import requests
import json

test_exectution_key = os.environ.get("TEST_EXECUTION_KEY", "Not found")
test_keys = os.environ.get("TEST_KEYS", "Not found") 
print(test_exectution_key)

#XRAY Cloud API Endpoints
XRAY_AUTH_URL = "https://xray.cloud.getxray.app/api/v2/authenticate"
XRAY_IMPORT_URL = "https://xray.cloud.getxray.app/api/v2/import/execution"

#Load credentials from cloud_auth.json
def load_xray_credentials():
    try:
        with open("cloud_auth_ops.json", "r") as file:
            credentials = json.load(file)
            return credentials["client_id"], credentials["client_secret"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print("Error: Invalid or missing 'cloud_auth.json'.")
        exit(1)

#Get Auth Token from Xray Cloud
def get_xray_token(client_id, client_secret):
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"client_id": client_id, "client_secret": client_secret})

    response = requests.post(XRAY_AUTH_URL, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json() #returns token
    else:
        print("Failed to authenticate with X-Ray: ", response.text)
        exit(1)


#Read and Parse test results from JSON
def load_test_results():
    try:
        with open("test_results.json", "r") as file:
            test_data = json.load(file)
            print("Test results loaded: ")
            executionResults=[]
            for test in test_data.get("tests", []):
                test_key = test.get("test","")
                status = map_status(test.get("outcome", "TO DO")) 

                executionResults.append({
                    "testKey": test_key,
                    "status": status
                })

            return executionResults
    except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Couldn't read or parse 'test_results.json'.")
            exit(1)

#Map pytest status
def map_status(pytest_status):
    status_map = {
        "passed": "PASSED",
        "failed": "FAILED",
        "skipped": "TO DO"
    }
    return status_map.get(pytest_status, "TO DO)")

#Format execution data
def format_execution_data(executionResults):
    return json.dumps({
        "testExecutionKey": test_exectution_key, #Jira test execution issue
        "tests": executionResults
    }, indent = 4)

#Upload Test Execution Results to Xray
def upload_results():
    client_id, client_secret = load_xray_credentials()
    token = get_xray_token(client_id, client_secret)
    executionResults = load_test_results()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = format_execution_data(executionResults)
    response = requests.post(XRAY_IMPORT_URL, headers=headers, data=payload)

    if response.status_code in [200, 201]:
        print("Test execution results uploaded successfully to Test Execution {}".format(test_exectution_key))
    else: 
        print("Failed to upload test results:", response.text)


if __name__ == "__main__":
    upload_results()