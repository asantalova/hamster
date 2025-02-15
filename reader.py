import os

test_exectution_key = os.environ.get("TEST_EXECUTION_KEY", "Not found")
test_keys = os.environ.get("TEST_KEYS", "Not found")

print("Here are the keys: {} {}".format(test_exectution_key, test_keys))