# uipath_orchestrator_rest.TestSetsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_sets_delete_by_id**](TestSetsApi.md#test_sets_delete_by_id) | **DELETE** /odata/TestSets({key}) | Delete a test set
[**test_sets_get**](TestSetsApi.md#test_sets_get) | **GET** /odata/TestSets | Returns a list of Test Sets cross-folder when no current folder is sent by header.  It will return Test Sets from folder where current user has TestSetsView.  If there is none, will return forbidden.
[**test_sets_get_by_id**](TestSetsApi.md#test_sets_get_by_id) | **GET** /odata/TestSets({key}) | Return a specific Test Set identified by key
[**test_sets_post**](TestSetsApi.md#test_sets_post) | **POST** /odata/TestSets | Creates a new Test Set
[**test_sets_put_by_id**](TestSetsApi.md#test_sets_put_by_id) | **PUT** /odata/TestSets({key}) | Update an existing Test Set


# **test_sets_delete_by_id**
> test_sets_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Delete a test set

OAuth required scopes: OR.TestSets or OR.TestSets.Write.  Required permissions: TestSets.Delete.  Responses:  204 The Test Set was deleted  403 If the caller doesn't have permissions to delete Test Sets

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
api_instance = uipath_orchestrator_rest.TestSetsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | ID of the Test Set to delete
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Delete a test set
    api_instance.test_sets_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestSetsApi->test_sets_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| ID of the Test Set to delete | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_sets_get**
> ODataValueOfIEnumerableOfTestSetDto test_sets_get(mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns a list of Test Sets cross-folder when no current folder is sent by header.  It will return Test Sets from folder where current user has TestSetsView.  If there is none, will return forbidden.

OAuth required scopes: OR.TestSets or OR.TestSets.Read.  Required permissions: TestSets.View.  Responses:  200 Returns a list of Test Sets filtered with queryOptions  403 If the caller doesn't have permissions to view Test Sets

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
api_instance = uipath_orchestrator_rest.TestSetsApi(uipath_orchestrator_rest.ApiClient(configuration))
mandatory_permissions = ['mandatory_permissions_example'] # list[str] |  (optional)
at_least_one_permissions = ['at_least_one_permissions_example'] # list[str] |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns a list of Test Sets cross-folder when no current folder is sent by header.  It will return Test Sets from folder where current user has TestSetsView.  If there is none, will return forbidden.
    api_response = api_instance.test_sets_get(mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetsApi->test_sets_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mandatory_permissions** | [**list[str]**](str.md)|  | [optional] 
 **at_least_one_permissions** | [**list[str]**](str.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfTestSetDto**](ODataValueOfIEnumerableOfTestSetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_sets_get_by_id**
> TestSetDto test_sets_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Return a specific Test Set identified by key

OAuth required scopes: OR.TestSets or OR.TestSets.Read.  Required permissions: TestSets.View.  Responses:  200 Return a specific Test Set identified by key  403 If the caller doesn't have permissions to view Test Sets  404 If the Test Set is not found

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
api_instance = uipath_orchestrator_rest.TestSetsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Return a specific Test Set identified by key
    api_response = api_instance.test_sets_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetsApi->test_sets_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestSetDto**](TestSetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_sets_post**
> TestSetDto test_sets_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a new Test Set

OAuth required scopes: OR.TestSets or OR.TestSets.Write.  Required permissions: TestSets.Create.  Responses:  201 Returns the newly created Test Set  403 If the caller doesn't have permissions to create Test Sets

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
api_instance = uipath_orchestrator_rest.TestSetsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestSetDto() # TestSetDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a new Test Set
    api_response = api_instance.test_sets_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetsApi->test_sets_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestSetDto**](TestSetDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestSetDto**](TestSetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_sets_put_by_id**
> TestSetDto test_sets_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Update an existing Test Set

OAuth required scopes: OR.TestSets or OR.TestSets.Write.  Required permissions: TestSets.Edit.  Responses:  200 Returns the updated Test Set  403 If the caller doesn't have permissions to update Test Sets

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
api_instance = uipath_orchestrator_rest.TestSetsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | ID of the Test Set to be updated
body = uipath_orchestrator_rest.TestSetDto() # TestSetDto | Update information (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Update an existing Test Set
    api_response = api_instance.test_sets_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetsApi->test_sets_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| ID of the Test Set to be updated | 
 **body** | [**TestSetDto**](TestSetDto.md)| Update information | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestSetDto**](TestSetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

