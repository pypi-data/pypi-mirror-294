# uipath_orchestrator_rest.StatusApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**status_get**](StatusApi.md#status_get) | **GET** /api/Status/Get | Returns whether the current endpoint should be serving traffic
[**status_verify_host_availibility**](StatusApi.md#status_verify_host_availibility) | **GET** /api/Status/VerifyHostAvailibility | 


# **status_get**
> status_get()

Returns whether the current endpoint should be serving traffic

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.StatusApi()

try:
    # Returns whether the current endpoint should be serving traffic
    api_instance.status_get()
except ApiException as e:
    print("Exception when calling StatusApi->status_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **status_verify_host_availibility**
> HostAvailabilityDto status_verify_host_availibility(url=url)



Required permissions: Webhooks.Create or Webhooks.Edit.

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
api_instance = uipath_orchestrator_rest.StatusApi(uipath_orchestrator_rest.ApiClient(configuration))
url = 'url_example' # str |  (optional)

try:
    api_response = api_instance.status_verify_host_availibility(url=url)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusApi->status_verify_host_availibility: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**|  | [optional] 

### Return type

[**HostAvailabilityDto**](HostAvailabilityDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

