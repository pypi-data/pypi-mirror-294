# uipath_orchestrator_rest.LicensesNamedUserApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**licenses_named_user_get_licenses_named_user_by_robottype**](LicensesNamedUserApi.md#licenses_named_user_get_licenses_named_user_by_robottype) | **GET** /odata/LicensesNamedUser/UiPath.Server.Configuration.OData.GetLicensesNamedUser(robotType&#x3D;{robotType}) | Gets named-user licenses.


# **licenses_named_user_get_licenses_named_user_by_robottype**
> ODataValueOfIEnumerableOfLicenseNamedUserDto licenses_named_user_get_licenses_named_user_by_robottype(robot_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets named-user licenses.

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
api_instance = uipath_orchestrator_rest.LicensesNamedUserApi(uipath_orchestrator_rest.ApiClient(configuration))
robot_type = 'robot_type_example' # str | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets named-user licenses.
    api_response = api_instance.licenses_named_user_get_licenses_named_user_by_robottype(robot_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LicensesNamedUserApi->licenses_named_user_get_licenses_named_user_by_robottype: %s\n" % e)
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

[**ODataValueOfIEnumerableOfLicenseNamedUserDto**](ODataValueOfIEnumerableOfLicenseNamedUserDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

