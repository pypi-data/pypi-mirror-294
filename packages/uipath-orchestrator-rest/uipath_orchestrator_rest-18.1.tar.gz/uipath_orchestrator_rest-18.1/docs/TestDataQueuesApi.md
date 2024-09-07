# uipath_orchestrator_rest.TestDataQueuesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_data_queues_delete_by_id**](TestDataQueuesApi.md#test_data_queues_delete_by_id) | **DELETE** /odata/TestDataQueues({key}) | Delete an existing test data queue
[**test_data_queues_get**](TestDataQueuesApi.md#test_data_queues_get) | **GET** /odata/TestDataQueues | Return a list of test data queues
[**test_data_queues_get_by_id**](TestDataQueuesApi.md#test_data_queues_get_by_id) | **GET** /odata/TestDataQueues({key}) | Return a specific test data queue identified by key
[**test_data_queues_post**](TestDataQueuesApi.md#test_data_queues_post) | **POST** /odata/TestDataQueues | Create a new test data queue
[**test_data_queues_put_by_id**](TestDataQueuesApi.md#test_data_queues_put_by_id) | **PUT** /odata/TestDataQueues({key}) | Update an existing test data queue


# **test_data_queues_delete_by_id**
> test_data_queues_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Delete an existing test data queue

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueues.Delete.  Responses:  204 The test data queue was deleted  403 If the caller doesn't have permissions to delete test data queues

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
api_instance = uipath_orchestrator_rest.TestDataQueuesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Id of the test data queue to be deleted
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Delete an existing test data queue
    api_instance.test_data_queues_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestDataQueuesApi->test_data_queues_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Id of the test data queue to be deleted | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queues_get**
> ODataValueOfIEnumerableOfTestDataQueueDto test_data_queues_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Return a list of test data queues

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Read.  Required permissions: TestDataQueues.View.  Responses:  200 Returns a list of test data queues filtered with queryOptions  403 If the caller doesn't have permissions to view test data queues

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
api_instance = uipath_orchestrator_rest.TestDataQueuesApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Return a list of test data queues
    api_response = api_instance.test_data_queues_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestDataQueuesApi->test_data_queues_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfTestDataQueueDto**](ODataValueOfIEnumerableOfTestDataQueueDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queues_get_by_id**
> TestDataQueueDto test_data_queues_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Return a specific test data queue identified by key

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Read.  Required permissions: TestDataQueues.View.  Responses:  200 Returns a specific test data queue identified by key  403 If the caller doesn't have permissions to view test data queues  404 If the test data queue is not found

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
api_instance = uipath_orchestrator_rest.TestDataQueuesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Return a specific test data queue identified by key
    api_response = api_instance.test_data_queues_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestDataQueuesApi->test_data_queues_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestDataQueueDto**](TestDataQueueDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queues_post**
> TestDataQueueDto test_data_queues_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Create a new test data queue

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueues.Create.  Responses:  201 Returns the newly created test data queue  403 If the caller doesn't have permissions to create test data queues  409 If a queue with the same name already exists

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
api_instance = uipath_orchestrator_rest.TestDataQueuesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestDataQueueDto() # TestDataQueueDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Create a new test data queue
    api_response = api_instance.test_data_queues_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestDataQueuesApi->test_data_queues_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestDataQueueDto**](TestDataQueueDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestDataQueueDto**](TestDataQueueDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queues_put_by_id**
> TestDataQueueDto test_data_queues_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Update an existing test data queue

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueues.Edit.  Responses:  200 Returns the updated test data queue  403 If the caller doesn't have permissions to update test data queues  409 If trying to change the queue name

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
api_instance = uipath_orchestrator_rest.TestDataQueuesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Id of the test data queue to be updated
body = uipath_orchestrator_rest.TestDataQueueDto() # TestDataQueueDto | Update information (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Update an existing test data queue
    api_response = api_instance.test_data_queues_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestDataQueuesApi->test_data_queues_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Id of the test data queue to be updated | 
 **body** | [**TestDataQueueDto**](TestDataQueueDto.md)| Update information | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestDataQueueDto**](TestDataQueueDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

