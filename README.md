# Test Trial project

### Custom command to select tests for execution by xray marks. 
```sh
pytest src/tests/ --xray-keys="KEY-1","KEY-2"  
```
#### *If no keys are provided, all tests with xray marks will be selected for execution.


------------------------------------------------------------------------


### To upload the results to xray run upload_to_xray.py

#### Prerequisites:
1. XRAY API Keys are stored in cloud_auth.json.
2. Test execution key is exported from Jira payload.

```sh
python src/utils/xray_upload.py  
```