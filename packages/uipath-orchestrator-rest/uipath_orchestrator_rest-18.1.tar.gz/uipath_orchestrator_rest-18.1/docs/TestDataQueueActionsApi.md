# uipath_orchestrator_rest.TestDataQueueActionsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_data_queue_actions_add_item**](TestDataQueueActionsApi.md#test_data_queue_actions_add_item) | **POST** /api/TestDataQueueActions/AddItem | Add a new test data queue item
[**test_data_queue_actions_bulk_add_items**](TestDataQueueActionsApi.md#test_data_queue_actions_bulk_add_items) | **POST** /api/TestDataQueueActions/BulkAddItems | Bulk adds an array of data queue items
[**test_data_queue_actions_delete_all_items**](TestDataQueueActionsApi.md#test_data_queue_actions_delete_all_items) | **DELETE** /api/TestDataQueueActions/DeleteAllItems | Delete all items from a test data queue
[**test_data_queue_actions_delete_items**](TestDataQueueActionsApi.md#test_data_queue_actions_delete_items) | **DELETE** /api/TestDataQueueActions/DeleteItems | Delete specific test data queue items
[**test_data_queue_actions_get_next_item**](TestDataQueueActionsApi.md#test_data_queue_actions_get_next_item) | **POST** /api/TestDataQueueActions/GetNextItem | Get the next unconsumed test data queue item
[**test_data_queue_actions_set_all_items_consumed**](TestDataQueueActionsApi.md#test_data_queue_actions_set_all_items_consumed) | **POST** /api/TestDataQueueActions/SetAllItemsConsumed | Set the IsConsumed flag for all items from a test data queue
[**test_data_queue_actions_set_items_consumed**](TestDataQueueActionsApi.md#test_data_queue_actions_set_items_consumed) | **POST** /api/TestDataQueueActions/SetItemsConsumed | Set the IsConsumed flag for specific test data queue items


# **test_data_queue_actions_add_item**
> TestDataQueueItemDto test_data_queue_actions_add_item(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Add a new test data queue item

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueueItems.Create.  Responses:  201 Returns the added test data queue item  403 If the caller doesn't have permissions to create test data queue items  409 If the test data queue item content violates the content JSON schema set on the queue

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
api_instance = uipath_orchestrator_rest.TestDataQueueActionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestDataQueueAddItemDto() # TestDataQueueAddItemDto | QueueName: the test data queue name; Content: the item content (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Add a new test data queue item
    api_response = api_instance.test_data_queue_actions_add_item(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestDataQueueActionsApi->test_data_queue_actions_add_item: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestDataQueueAddItemDto**](TestDataQueueAddItemDto.md)| QueueName: the test data queue name; Content: the item content | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestDataQueueItemDto**](TestDataQueueItemDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queue_actions_bulk_add_items**
> int test_data_queue_actions_bulk_add_items(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Bulk adds an array of data queue items

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueueItems.Create.  Responses:  200 Returns the number of items added  403 If the caller doesn't have permissions to create test data queue items  409 If the test data queue items violates the content JSON schema set on the queue

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
api_instance = uipath_orchestrator_rest.TestDataQueueActionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestDataQueueBulkAddItemsDto() # TestDataQueueBulkAddItemsDto | QueueName: the test data queue name; Items: an array of item content (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Bulk adds an array of data queue items
    api_response = api_instance.test_data_queue_actions_bulk_add_items(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestDataQueueActionsApi->test_data_queue_actions_bulk_add_items: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestDataQueueBulkAddItemsDto**](TestDataQueueBulkAddItemsDto.md)| QueueName: the test data queue name; Items: an array of item content | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

**int**

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queue_actions_delete_all_items**
> test_data_queue_actions_delete_all_items(queue_name=queue_name, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Delete all items from a test data queue

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueueItems.Delete.  Responses:  202 All items from the test data queue were scheduled for deletion  403 If the caller doesn't have permissions to delete test data queue items

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
api_instance = uipath_orchestrator_rest.TestDataQueueActionsApi(uipath_orchestrator_rest.ApiClient(configuration))
queue_name = 'queue_name_example' # str | The name of the test data queue (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Delete all items from a test data queue
    api_instance.test_data_queue_actions_delete_all_items(queue_name=queue_name, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestDataQueueActionsApi->test_data_queue_actions_delete_all_items: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queue_name** | **str**| The name of the test data queue | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queue_actions_delete_items**
> test_data_queue_actions_delete_items(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Delete specific test data queue items

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueueItems.Delete.  Responses:  204 Deleted the test data queue items  403 If the caller doesn't have permissions to delete test data queue items

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
api_instance = uipath_orchestrator_rest.TestDataQueueActionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = [uipath_orchestrator_rest.list[int]()] # list[int] | The Ids of the test data queue items (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Delete specific test data queue items
    api_instance.test_data_queue_actions_delete_items(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestDataQueueActionsApi->test_data_queue_actions_delete_items: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **list[int]**| The Ids of the test data queue items | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queue_actions_get_next_item**
> TestDataQueueItemDto test_data_queue_actions_get_next_item(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get the next unconsumed test data queue item

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueueItems.View.  Responses:  200 Returns the next unconsumed test data queue item  204 If there are no unconsumed test data queue items in the queue  403 If the caller doesn't have permissions to view test data queue items  404 If the test data queue does not exist

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
api_instance = uipath_orchestrator_rest.TestDataQueueActionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestDataQueueGetNextItemDto() # TestDataQueueGetNextItemDto | QueueName:the test data queue name; SetConsumed: Whether to set the item's IsConsumed flag as true or false (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get the next unconsumed test data queue item
    api_response = api_instance.test_data_queue_actions_get_next_item(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestDataQueueActionsApi->test_data_queue_actions_get_next_item: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestDataQueueGetNextItemDto**](TestDataQueueGetNextItemDto.md)| QueueName:the test data queue name; SetConsumed: Whether to set the item&#39;s IsConsumed flag as true or false | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TestDataQueueItemDto**](TestDataQueueItemDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queue_actions_set_all_items_consumed**
> test_data_queue_actions_set_all_items_consumed(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Set the IsConsumed flag for all items from a test data queue

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueueItems.Edit.  Responses:  202 All items from the test data queue were scheduled for setting the IsConsumed flag  403 If the caller doesn't have permissions to edit test data queue items

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
api_instance = uipath_orchestrator_rest.TestDataQueueActionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestDataQueueSetAllItemsConsumedDto() # TestDataQueueSetAllItemsConsumedDto | QueueName: the name of the test data queue; IsConsumed: the value to be set on the items IsConsumed flag (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Set the IsConsumed flag for all items from a test data queue
    api_instance.test_data_queue_actions_set_all_items_consumed(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestDataQueueActionsApi->test_data_queue_actions_set_all_items_consumed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestDataQueueSetAllItemsConsumedDto**](TestDataQueueSetAllItemsConsumedDto.md)| QueueName: the name of the test data queue; IsConsumed: the value to be set on the items IsConsumed flag | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_queue_actions_set_items_consumed**
> test_data_queue_actions_set_items_consumed(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Set the IsConsumed flag for specific test data queue items

OAuth required scopes: OR.TestDataQueues or OR.TestDataQueues.Write.  Required permissions: TestDataQueueItems.Edit.  Responses:  200 If the operation succeeded  403 If the caller doesn't have permissions to edit test data queue items

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
api_instance = uipath_orchestrator_rest.TestDataQueueActionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestDataQueueSetItemsConsumedDto() # TestDataQueueSetItemsConsumedDto | ItemIds: the list of item ids for which to set the IsConsumed flag; IsConsumed: the value to be set on the items IsConsumed flag (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Set the IsConsumed flag for specific test data queue items
    api_instance.test_data_queue_actions_set_items_consumed(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestDataQueueActionsApi->test_data_queue_actions_set_items_consumed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestDataQueueSetItemsConsumedDto**](TestDataQueueSetItemsConsumedDto.md)| ItemIds: the list of item ids for which to set the IsConsumed flag; IsConsumed: the value to be set on the items IsConsumed flag | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

