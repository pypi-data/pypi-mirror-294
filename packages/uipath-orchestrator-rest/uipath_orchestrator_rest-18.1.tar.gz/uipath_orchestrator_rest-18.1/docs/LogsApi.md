# uipath_orchestrator_rest.LogsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**logs_post**](LogsApi.md#logs_post) | **POST** /api/Logs | Inserts a log entry with a specified message in JSON format.
[**logs_submit_logs**](LogsApi.md#logs_submit_logs) | **POST** /api/Logs/SubmitLogs | Inserts a collection of log entries, each in a specific JSON format.


# **logs_post**
> logs_post(body=body)

Inserts a log entry with a specified message in JSON format.

OAuth required scopes: OR.Monitoring or OR.Monitoring.Write.  Required permissions: (Logs.Create).  Example of jMessage parameter.                     {           \"message\": \"TTT execution started\",           \"level\": \"Information\",           \"timeStamp\": \"2017-01-18T14:46:07.4152893+02:00\",           \"windowsIdentity\": \"DESKTOP-1L50L0P\\\\WindowsUser\",           \"agentSessionId\": \"00000000-0000-0000-0000-000000000000\",           \"processName\": \"TTT\",           \"fileName\": \"Main\",           \"jobId\": \"8066c309-cef8-4b47-9163-b273fc14cc43\"       } DEPRECATED:  Use SubmitLogs instead Please refer to https://docs.uipath.com/orchestrator/reference

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAuth2
configuration = uipath_orchestrator_rest.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = uipath_orchestrator_rest.LogsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = NULL # object |  (optional)

try:
    # Inserts a log entry with a specified message in JSON format.
    api_instance.logs_post(body=body)
except ApiException as e:
    print("Exception when calling LogsApi->logs_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logs_submit_logs**
> logs_submit_logs(body=body)

Inserts a collection of log entries, each in a specific JSON format.

OAuth required scopes: OR.Monitoring or OR.Monitoring.Write.  Required permissions: (Logs.Create).  Example of log entry:       {           \"message\": \"TTT execution started\",           \"level\": \"Information\",           \"timeStamp\": \"2017-01-18T14:46:07.4152893+02:00\",           \"windowsIdentity\": \"DESKTOP-1L50L0P\\\\WindowsUser\",           \"agentSessionId\": \"00000000-0000-0000-0000-000000000000\",           \"processName\": \"TTT\",           \"fileName\": \"Main\",           \"jobId\": \"8066c309-cef8-4b47-9163-b273fc14cc43\"       }

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAuth2
configuration = uipath_orchestrator_rest.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = uipath_orchestrator_rest.LogsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = [uipath_orchestrator_rest.list[str]()] # list[str] | Collection of string representations of JSON objects (optional)

try:
    # Inserts a collection of log entries, each in a specific JSON format.
    api_instance.logs_submit_logs(body=body)
except ApiException as e:
    print("Exception when calling LogsApi->logs_submit_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **list[str]**| Collection of string representations of JSON objects | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

