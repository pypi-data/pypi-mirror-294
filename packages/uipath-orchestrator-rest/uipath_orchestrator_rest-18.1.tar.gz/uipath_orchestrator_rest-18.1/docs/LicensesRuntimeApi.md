# uipath_orchestrator_rest.LicensesRuntimeApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**licenses_runtime_get_licenses_runtime_by_robottype**](LicensesRuntimeApi.md#licenses_runtime_get_licenses_runtime_by_robottype) | **GET** /odata/LicensesRuntime/UiPath.Server.Configuration.OData.GetLicensesRuntime(robotType&#x3D;{robotType}) | Gets runtime licenses.
[**licenses_runtime_toggle_enabled_by_key**](LicensesRuntimeApi.md#licenses_runtime_toggle_enabled_by_key) | **POST** /odata/LicensesRuntime({key})/UiPath.Server.Configuration.OData.ToggleEnabled | Toggles machine licensing on/off.


# **licenses_runtime_get_licenses_runtime_by_robottype**
> ODataValueOfIEnumerableOfLicenseRuntimeDto licenses_runtime_get_licenses_runtime_by_robottype(robot_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets runtime licenses.

OAuth required scopes: OR.License or OR.License.Read.  Required permissions: License.View.

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
api_instance = uipath_orchestrator_rest.LicensesRuntimeApi(uipath_orchestrator_rest.ApiClient(configuration))
robot_type = 'robot_type_example' # str | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets runtime licenses.
    api_response = api_instance.licenses_runtime_get_licenses_runtime_by_robottype(robot_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LicensesRuntimeApi->licenses_runtime_get_licenses_runtime_by_robottype: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **robot_type** | **str**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfLicenseRuntimeDto**](ODataValueOfIEnumerableOfLicenseRuntimeDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **licenses_runtime_toggle_enabled_by_key**
> licenses_runtime_toggle_enabled_by_key(key, body=body)

Toggles machine licensing on/off.

OAuth required scopes: OR.License or OR.License.Write.  Required permissions: Machines.Edit.

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
api_instance = uipath_orchestrator_rest.LicensesRuntimeApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
body = uipath_orchestrator_rest.LicensesToggleEnabledRequest() # LicensesToggleEnabledRequest |  (optional)

try:
    # Toggles machine licensing on/off.
    api_instance.licenses_runtime_toggle_enabled_by_key(key, body=body)
except ApiException as e:
    print("Exception when calling LicensesRuntimeApi->licenses_runtime_toggle_enabled_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **body** | [**LicensesToggleEnabledRequest**](LicensesToggleEnabledRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

