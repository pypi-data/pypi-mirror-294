# uipath_orchestrator_rest.TestSetSchedulesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_set_schedules_delete_by_id**](TestSetSchedulesApi.md#test_set_schedules_delete_by_id) | **DELETE** /odata/TestSetSchedules({key}) | Delete an existing test set execution schedule
[**test_set_schedules_get**](TestSetSchedulesApi.md#test_set_schedules_get) | **GET** /odata/TestSetSchedules | Returns a list of test set execution schedules
[**test_set_schedules_get_by_id**](TestSetSchedulesApi.md#test_set_schedules_get_by_id) | **GET** /odata/TestSetSchedules({key}) | Return a specific test set execution schedule identified by key
[**test_set_schedules_post**](TestSetSchedulesApi.md#test_set_schedules_post) | **POST** /odata/TestSetSchedules | Creates a new test set execution schedule
[**test_set_schedules_put_by_id**](TestSetSchedulesApi.md#test_set_schedules_put_by_id) | **PUT** /odata/TestSetSchedules({key}) | Update an existing test set execution schedule
[**test_set_schedules_set_enabled**](TestSetSchedulesApi.md#test_set_schedules_set_enabled) | **POST** /odata/TestSetSchedules/UiPath.Server.Configuration.OData.SetEnabled | Enables / disables a list of test set execution schedules.


# **test_set_schedules_delete_by_id**
> test_set_schedules_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Delete an existing test set execution schedule

OAuth required scopes: OR.TestSetSchedules or OR.TestSetSchedules.Write.  Required permissions: TestSetSchedules.Delete.  Responses:  204 The test set execution schedule was deleted  403 If the caller doesn't have permissions to delete test set execution schedules

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
api_instance = uipath_orchestrator_rest.TestSetSchedulesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | ID of the test set execution schedule to be deleted
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Delete an existing test set execution schedule
    api_instance.test_set_schedules_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestSetSchedulesApi->test_set_schedules_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| ID of the test set execution schedule to be deleted | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_set_schedules_get**
> ODataValueOfIEnumerableOfTestSetScheduleDto test_set_schedules_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns a list of test set execution schedules

OAuth required scopes: OR.TestSetSchedules or OR.TestSetSchedules.Read.  Required permissions: TestSetSchedules.View.  Responses:  200 Returns a list of test set execution schedules filtered with queryOptions  403 If the caller doesn't have permissions to view test set execution schedules

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
api_instance = uipath_orchestrator_rest.TestSetSchedulesApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns a list of test set execution schedules
    api_response = api_instance.test_set_schedules_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetSchedulesApi->test_set_schedules_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfTestSetScheduleDto**](ODataValueOfIEnumerableOfTestSetScheduleDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_set_schedules_get_by_id**
> TestSetScheduleDto test_set_schedules_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Return a specific test set execution schedule identified by key

OAuth required scopes: OR.TestSetSchedules or OR.TestSetSchedules.Read.  Required permissions: TestSetSchedules.View.  Responses:  200 Return a specific test set execution schedule identified by key  403 If the caller doesn't have permissions to view test set execution schedules  404 It the test set execution schedule is not found

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
api_instance = uipath_orchestrator_rest.TestSetSchedulesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Return a specific test set execution schedule identified by key
    api_response = api_instance.test_set_schedules_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetSchedulesApi->test_set_schedules_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestSetScheduleDto**](TestSetScheduleDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_set_schedules_post**
> TestSetScheduleDto test_set_schedules_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a new test set execution schedule

OAuth required scopes: OR.TestSetSchedules or OR.TestSetSchedules.Write.  Required permissions: TestSetSchedules.Create.  Responses:  201 Returns the newly created test set execution schedule  403 If the caller doesn't have permissions to create test set execution schedules

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
api_instance = uipath_orchestrator_rest.TestSetSchedulesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestSetScheduleDto() # TestSetScheduleDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a new test set execution schedule
    api_response = api_instance.test_set_schedules_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetSchedulesApi->test_set_schedules_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestSetScheduleDto**](TestSetScheduleDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestSetScheduleDto**](TestSetScheduleDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_set_schedules_put_by_id**
> TestSetScheduleDto test_set_schedules_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Update an existing test set execution schedule

OAuth required scopes: OR.TestSetSchedules or OR.TestSetSchedules.Write.  Required permissions: TestSetSchedules.Edit.  Responses:  201 Returns the updated test set execution schedule  403 If the caller doesn't have permissions to update test set execution schedules

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
api_instance = uipath_orchestrator_rest.TestSetSchedulesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | ID of the test set execution schedule to be updated
body = uipath_orchestrator_rest.TestSetScheduleDto() # TestSetScheduleDto | Update information (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Update an existing test set execution schedule
    api_response = api_instance.test_set_schedules_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetSchedulesApi->test_set_schedules_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| ID of the test set execution schedule to be updated | 
 **body** | [**TestSetScheduleDto**](TestSetScheduleDto.md)| Update information | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestSetScheduleDto**](TestSetScheduleDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_set_schedules_set_enabled**
> ODataValueOfBoolean test_set_schedules_set_enabled(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Enables / disables a list of test set execution schedules.

OAuth required scopes: OR.TestSetSchedules or OR.TestSetSchedules.Write.  Required permissions: TestSetSchedules.Edit.

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
api_instance = uipath_orchestrator_rest.TestSetSchedulesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestSetSchedulesEnabledRequest() # TestSetSchedulesEnabledRequest | <para />enabled: if true the test set schedules will be enabled, if false they will be disabled.              <para />scheduleIds: the ids of the test set schedules to be enabled or disabled. (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Enables / disables a list of test set execution schedules.
    api_response = api_instance.test_set_schedules_set_enabled(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestSetSchedulesApi->test_set_schedules_set_enabled: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestSetSchedulesEnabledRequest**](TestSetSchedulesEnabledRequest.md)| &lt;para /&gt;enabled: if true the test set schedules will be enabled, if false they will be disabled.              &lt;para /&gt;scheduleIds: the ids of the test set schedules to be enabled or disabled. | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfBoolean**](ODataValueOfBoolean.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

