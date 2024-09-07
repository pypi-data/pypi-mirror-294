# uipath_orchestrator_rest.AccountApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**account_authenticate**](AccountApi.md#account_authenticate) | **POST** /api/Account/Authenticate | Authenticates the user based on user name and password


# **account_authenticate**
> AjaxResponse account_authenticate(body=body)

Authenticates the user based on user name and password

Authenticates the user based on user name and password. DEPRECATED:  Please user other means to authenticate in your application. This endpoint will be removed in future releases. Please refer to https://docs.uipath.com/orchestrator/reference

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.AccountApi()
body = uipath_orchestrator_rest.LoginModel() # LoginModel | The login parameters. (optional)

try:
    # Authenticates the user based on user name and password
    api_response = api_instance.account_authenticate(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountApi->account_authenticate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LoginModel**](LoginModel.md)| The login parameters. | [optional] 

### Return type

[**AjaxResponse**](AjaxResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

