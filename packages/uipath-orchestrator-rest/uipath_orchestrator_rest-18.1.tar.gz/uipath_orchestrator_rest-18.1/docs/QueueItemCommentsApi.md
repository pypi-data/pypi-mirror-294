# uipath_orchestrator_rest.QueueItemCommentsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**queue_item_comments_delete_by_id**](QueueItemCommentsApi.md#queue_item_comments_delete_by_id) | **DELETE** /odata/QueueItemComments({key}) | Deletes a QueueItemComment.
[**queue_item_comments_get**](QueueItemCommentsApi.md#queue_item_comments_get) | **GET** /odata/QueueItemComments | Gets the QueueItemComments.
[**queue_item_comments_get_by_id**](QueueItemCommentsApi.md#queue_item_comments_get_by_id) | **GET** /odata/QueueItemComments({key}) | Gets a QueueItemComment by Id.
[**queue_item_comments_get_queue_item_comments_history_by_queueitemid**](QueueItemCommentsApi.md#queue_item_comments_get_queue_item_comments_history_by_queueitemid) | **GET** /odata/QueueItemComments/UiPath.Server.Configuration.OData.GetQueueItemCommentsHistory(queueItemId&#x3D;{queueItemId}) | Returns a collection of Queue Item Comments associated to a Queue Item and all its related Queue Items.  A Queue Item is related to another if it was created as a retry of a failed Queue Item. They also share the same Key.
[**queue_item_comments_post**](QueueItemCommentsApi.md#queue_item_comments_post) | **POST** /odata/QueueItemComments | Creates a QueueItemComment.
[**queue_item_comments_put_by_id**](QueueItemCommentsApi.md#queue_item_comments_put_by_id) | **PUT** /odata/QueueItemComments({key}) | Updates a QueueItemComment


# **queue_item_comments_delete_by_id**
> queue_item_comments_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Deletes a QueueItemComment.

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
api_instance = uipath_orchestrator_rest.QueueItemCommentsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Deletes a QueueItemComment.
    api_instance.queue_item_comments_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueItemCommentsApi->queue_item_comments_delete_by_id: %s\n" % e)
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

# **queue_item_comments_get**
> ODataValueOfIEnumerableOfQueueItemCommentDto queue_item_comments_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets the QueueItemComments.

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
api_instance = uipath_orchestrator_rest.QueueItemCommentsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets the QueueItemComments.
    api_response = api_instance.queue_item_comments_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemCommentsApi->queue_item_comments_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfQueueItemCommentDto**](ODataValueOfIEnumerableOfQueueItemCommentDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_item_comments_get_by_id**
> QueueItemCommentDto queue_item_comments_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a QueueItemComment by Id.

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
api_instance = uipath_orchestrator_rest.QueueItemCommentsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a QueueItemComment by Id.
    api_response = api_instance.queue_item_comments_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemCommentsApi->queue_item_comments_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**QueueItemCommentDto**](QueueItemCommentDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_item_comments_get_queue_item_comments_history_by_queueitemid**
> ODataValueOfIEnumerableOfQueueItemCommentDto queue_item_comments_get_queue_item_comments_history_by_queueitemid(queue_item_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns a collection of Queue Item Comments associated to a Queue Item and all its related Queue Items.  A Queue Item is related to another if it was created as a retry of a failed Queue Item. They also share the same Key.

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
api_instance = uipath_orchestrator_rest.QueueItemCommentsApi(uipath_orchestrator_rest.ApiClient(configuration))
queue_item_id = 789 # int | The Id of the Queue Item for which the comment history is requested.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns a collection of Queue Item Comments associated to a Queue Item and all its related Queue Items.  A Queue Item is related to another if it was created as a retry of a failed Queue Item. They also share the same Key.
    api_response = api_instance.queue_item_comments_get_queue_item_comments_history_by_queueitemid(queue_item_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemCommentsApi->queue_item_comments_get_queue_item_comments_history_by_queueitemid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queue_item_id** | **int**| The Id of the Queue Item for which the comment history is requested. | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfQueueItemCommentDto**](ODataValueOfIEnumerableOfQueueItemCommentDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_item_comments_post**
> QueueItemCommentDto queue_item_comments_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a QueueItemComment.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.Edit.  Note: If the CreationTime is passed in in the UiPath.Orchestrator.Application.Dto.Queues.QueueItemCommentDto it will be overriden with server UTC time.

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
api_instance = uipath_orchestrator_rest.QueueItemCommentsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.QueueItemCommentDto() # QueueItemCommentDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a QueueItemComment.
    api_response = api_instance.queue_item_comments_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueItemCommentsApi->queue_item_comments_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QueueItemCommentDto**](QueueItemCommentDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**QueueItemCommentDto**](QueueItemCommentDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_item_comments_put_by_id**
> queue_item_comments_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Updates a QueueItemComment

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
api_instance = uipath_orchestrator_rest.QueueItemCommentsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.QueueItemCommentDto() # QueueItemCommentDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Updates a QueueItemComment
    api_instance.queue_item_comments_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueItemCommentsApi->queue_item_comments_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**QueueItemCommentDto**](QueueItemCommentDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

