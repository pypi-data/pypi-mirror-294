# uipath_orchestrator_rest.LicensingApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**licensing_acquire**](LicensingApi.md#licensing_acquire) | **POST** /api/Licensing/Acquire | Acquire license units
[**licensing_release**](LicensingApi.md#licensing_release) | **PUT** /api/Licensing/Release | Release acquired license units


# **licensing_acquire**
> LicenseResultDto licensing_acquire(body=body)

Acquire license units

OAuth required scopes: OR.Administration or OR.Administration.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.LicensingApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.ConsumptionLicenseDto() # ConsumptionLicenseDto |  (optional)

try:
    # Acquire license units
    api_response = api_instance.licensing_acquire(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LicensingApi->licensing_acquire: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConsumptionLicenseDto**](ConsumptionLicenseDto.md)|  | [optional] 

### Return type

[**LicenseResultDto**](LicenseResultDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **licensing_release**
> LicenseResultDto licensing_release(body=body)

Release acquired license units

OAuth required scopes: OR.Administration or OR.Administration.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.LicensingApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.ConsumptionLicenseDto() # ConsumptionLicenseDto |  (optional)

try:
    # Release acquired license units
    api_response = api_instance.licensing_release(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LicensingApi->licensing_release: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConsumptionLicenseDto**](ConsumptionLicenseDto.md)|  | [optional] 

### Return type

[**LicenseResultDto**](LicenseResultDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

