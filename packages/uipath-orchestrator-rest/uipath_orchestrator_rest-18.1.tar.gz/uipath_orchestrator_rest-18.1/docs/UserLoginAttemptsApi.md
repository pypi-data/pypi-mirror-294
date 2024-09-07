# UIPathAPI.UserLoginAttemptsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**user_login_attempts_get_by_id**](UserLoginAttemptsApi.md#user_login_attempts_get_by_id) | **GET** /odata/UserLoginAttempts({key}) | Gets the user&#39;s login attempts


# **user_login_attempts_get_by_id**
> ODataValueOfIEnumerableOfUserLoginAttemptDto user_login_attempts_get_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets the user's login attempts

OAuth required scopes: OR.Users or OR.Users.Read.  Requires authentication. DEPRECATED:  This API is deprecated. Since we switched to access token authentication, user login attempts are no longer saved in Orchestrator. Only use it to retrieve historical data. Please refer to https://docs.uipath.com/orchestrator/reference

### Example
```python
from __future__ import print_function
import time
import UIPathAPI
from UIPathAPI.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAuth2
configuration = UIPathAPI.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = UIPathAPI.UserLoginAttemptsApi(UIPathAPI.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets the user's login attempts
    api_response = api_instance.user_login_attempts_get_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserLoginAttemptsApi->user_login_attempts_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfUserLoginAttemptDto**](ODataValueOfIEnumerableOfUserLoginAttemptDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

