# uipath_orchestrator_rest.QueueItemsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**queue_items_delete_bulk**](QueueItemsApi.md#queue_items_delete_bulk) | **POST** /odata/QueueItems/UiPathODataSvc.DeleteBulk | Sets the given queue items&#39; status to Deleted.
[**queue_items_delete_by_id**](QueueItemsApi.md#queue_items_delete_by_id) | **DELETE** /odata/QueueItems({key}) | Deletes a queue item by Id.
[**queue_items_get**](QueueItemsApi.md#queue_items_get) | **GET** /odata/QueueItems | Gets a collection of queue items.
[**queue_items_get_by_id**](QueueItemsApi.md#queue_items_get_by_id) | **GET** /odata/QueueItems({key}) | Gets a queue item by Id.
[**queue_items_get_item_last_retry_by_id**](QueueItemsApi.md#queue_items_get_item_last_retry_by_id) | **GET** /odata/QueueItems({key})/UiPath.Server.Configuration.OData.GetItemLastRetry | Returns the last retry of a queue item.
[**queue_items_get_item_processing_history_by_id**](QueueItemsApi.md#queue_items_get_item_processing_history_by_id) | **GET** /odata/QueueItems({key})/UiPathODataSvc.GetItemProcessingHistory | Returns data about the processing history of the given queue item. Allows odata query options.
[**queue_items_get_reviewers**](QueueItemsApi.md#queue_items_get_reviewers) | **GET** /odata/QueueItems/UiPath.Server.Configuration.OData.GetReviewers | Returns a collection of users having the permission for Queue Items review. Allows odata query options.
[**queue_items_put_by_id**](QueueItemsApi.md#queue_items_put_by_id) | **PUT** /odata/QueueItems({key}) | Updates the QueueItem properties with the new values provided.
[**queue_items_set_item_review_status**](QueueItemsApi.md#queue_items_set_item_review_status) | **POST** /odata/QueueItems/UiPathODataSvc.SetItemReviewStatus | Updates the review status of the specified queue items to an indicated state.
[**queue_items_set_item_reviewer**](QueueItemsApi.md#queue_items_set_item_reviewer) | **POST** /odata/QueueItems/UiPathODataSvc.SetItemReviewer | Sets the reviewer for multiple queue items
[**queue_items_set_transaction_progress_by_id**](QueueItemsApi.md#queue_items_set_transaction_progress_by_id) | **POST** /odata/QueueItems({key})/UiPathODataSvc.SetTransactionProgress | Updates the progress field of a queue item with the status &#39;In Progress&#39;.
[**queue_items_unset_item_reviewer**](QueueItemsApi.md#queue_items_unset_item_reviewer) | **POST** /odata/QueueItems/UiPathODataSvc.UnsetItemReviewer | Unsets the reviewer for multiple queue items


# **queue_items_delete_bulk**
> BulkOperationResponseDtoOfInt64 queue_items_delete_bulk(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Sets the given queue items' status to Deleted.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.Delete.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.QueueItemDeleteBulkRequest() # QueueItemDeleteBulkRequest | QueueItems - The collection of ids of queue items to delete. (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Sets the given queue items' status to Deleted.
    api_response = api_instance.queue_items_delete_bulk(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_delete_bulk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QueueItemDeleteBulkRequest**](QueueItemDeleteBulkRequest.md)| QueueItems - The collection of ids of queue items to delete. | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BulkOperationResponseDtoOfInt64**](BulkOperationResponseDtoOfInt64.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_delete_by_id**
> queue_items_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Deletes a queue item by Id.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.Delete.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Deletes a queue item by Id.
    api_instance.queue_items_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_get**
> ODataValueOfIEnumerableOfQueueItemDto queue_items_get(mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a collection of queue items.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View and Transactions.View.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
mandatory_permissions = ['mandatory_permissions_example'] # list[str] | If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; all permissions in this set must be met (optional)
at_least_one_permissions = ['at_least_one_permissions_example'] # list[str] | If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; at least one permission in this set must be met (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a collection of queue items.
    api_response = api_instance.queue_items_get(mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mandatory_permissions** | [**list[str]**](str.md)| If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; all permissions in this set must be met | [optional] 
 **at_least_one_permissions** | [**list[str]**](str.md)| If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; at least one permission in this set must be met | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfQueueItemDto**](ODataValueOfIEnumerableOfQueueItemDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_get_by_id**
> QueueItemDto queue_items_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a queue item by Id.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View and Transactions.View.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a queue item by Id.
    api_response = api_instance.queue_items_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**QueueItemDto**](QueueItemDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_get_item_last_retry_by_id**
> QueueItemDto queue_items_get_item_last_retry_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns the last retry of a queue item.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View and Transactions.View.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns the last retry of a queue item.
    api_response = api_instance.queue_items_get_item_last_retry_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_get_item_last_retry_by_id: %s\n" % e)
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
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**QueueItemDto**](QueueItemDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_get_item_processing_history_by_id**
> ODataValueOfIEnumerableOfQueueItemDto queue_items_get_item_processing_history_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns data about the processing history of the given queue item. Allows odata query options.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View and Transactions.View.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns data about the processing history of the given queue item. Allows odata query options.
    api_response = api_instance.queue_items_get_item_processing_history_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_get_item_processing_history_by_id: %s\n" % e)
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
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfQueueItemDto**](ODataValueOfIEnumerableOfQueueItemDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_get_reviewers**
> ODataValueOfIEnumerableOfSimpleUserDto queue_items_get_reviewers(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns a collection of users having the permission for Queue Items review. Allows odata query options.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View and Transactions.Edit.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns a collection of users having the permission for Queue Items review. Allows odata query options.
    api_response = api_instance.queue_items_get_reviewers(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_get_reviewers: %s\n" % e)
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

[**ODataValueOfIEnumerableOfSimpleUserDto**](ODataValueOfIEnumerableOfSimpleUserDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_put_by_id**
> queue_items_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Updates the QueueItem properties with the new values provided.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.Edit and Transactions.Edit.  Only UiPath.Orchestrator.Application.Dto.Queues.QueueItemDto.Progress, UiPath.Orchestrator.Application.Dto.Queues.QueueItemDto.Priority, UiPath.Orchestrator.Application.Dto.Queues.QueueItemDto.DueDate, UiPath.Orchestrator.Application.Dto.Queues.QueueItemDto.DeferDate and UiPath.Orchestrator.Application.Dto.Queues.QueueItemDto.SpecificContent will be updated from given queueItemDto object.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.QueueItemDataDto() # QueueItemDataDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Updates the QueueItem properties with the new values provided.
    api_instance.queue_items_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**QueueItemDataDto**](QueueItemDataDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_set_item_review_status**
> BulkOperationResponseDtoOfInt64 queue_items_set_item_review_status(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Updates the review status of the specified queue items to an indicated state.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.Edit.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.QueueSetItemReviewStatusRequest() # QueueSetItemReviewStatusRequest | <para />QueueItems - The collection of ids of queue items for which the state is set.              <para />Status - The new value for the review status. (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Updates the review status of the specified queue items to an indicated state.
    api_response = api_instance.queue_items_set_item_review_status(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_set_item_review_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QueueSetItemReviewStatusRequest**](QueueSetItemReviewStatusRequest.md)| &lt;para /&gt;QueueItems - The collection of ids of queue items for which the state is set.              &lt;para /&gt;Status - The new value for the review status. | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BulkOperationResponseDtoOfInt64**](BulkOperationResponseDtoOfInt64.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_set_item_reviewer**
> BulkOperationResponseDtoOfInt64 queue_items_set_item_reviewer(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Sets the reviewer for multiple queue items

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.Edit.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.QueueSetItemReviewerRequest() # QueueSetItemReviewerRequest | <para />UserId - The ID of the user to be set as the reviewer. If not set, the reviewer is cleared.              <para />QueueItems - The collection of ids of queue items for which the reviewer is set. (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Sets the reviewer for multiple queue items
    api_response = api_instance.queue_items_set_item_reviewer(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_set_item_reviewer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QueueSetItemReviewerRequest**](QueueSetItemReviewerRequest.md)| &lt;para /&gt;UserId - The ID of the user to be set as the reviewer. If not set, the reviewer is cleared.              &lt;para /&gt;QueueItems - The collection of ids of queue items for which the reviewer is set. | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BulkOperationResponseDtoOfInt64**](BulkOperationResponseDtoOfInt64.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_set_transaction_progress_by_id**
> queue_items_set_transaction_progress_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Updates the progress field of a queue item with the status 'In Progress'.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.Edit.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.QueueSetTransactionProgressRequest() # QueueSetTransactionProgressRequest | <para />QueueItemId - The item's id.              <para />Progress - The value for the Progress field. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Updates the progress field of a queue item with the status 'In Progress'.
    api_instance.queue_items_set_transaction_progress_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_set_transaction_progress_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**QueueSetTransactionProgressRequest**](QueueSetTransactionProgressRequest.md)| &lt;para /&gt;QueueItemId - The item&#39;s id.              &lt;para /&gt;Progress - The value for the Progress field. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_items_unset_item_reviewer**
> BulkOperationResponseDtoOfInt64 queue_items_unset_item_reviewer(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Unsets the reviewer for multiple queue items

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.Edit.

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
api_instance = uipath_orchestrator_rest.QueueItemsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.QueueUnsetItemReviewerRequest() # QueueUnsetItemReviewerRequest | <para />QueueItems - The collection of ids of queue items for which the reviewer is unset. (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Unsets the reviewer for multiple queue items
    api_response = api_instance.queue_items_unset_item_reviewer(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemsApi->queue_items_unset_item_reviewer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QueueUnsetItemReviewerRequest**](QueueUnsetItemReviewerRequest.md)| &lt;para /&gt;QueueItems - The collection of ids of queue items for which the reviewer is unset. | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BulkOperationResponseDtoOfInt64**](BulkOperationResponseDtoOfInt64.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

