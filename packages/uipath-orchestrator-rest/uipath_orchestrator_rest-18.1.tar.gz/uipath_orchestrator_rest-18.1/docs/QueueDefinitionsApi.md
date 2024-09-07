# uipath_orchestrator_rest.QueueDefinitionsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**queue_definitions_delete_by_id**](QueueDefinitionsApi.md#queue_definitions_delete_by_id) | **DELETE** /odata/QueueDefinitions({key}) | Deletes a queue based on its key.
[**queue_definitions_export_by_id**](QueueDefinitionsApi.md#queue_definitions_export_by_id) | **POST** /odata/QueueDefinitions({key})/UiPathODataSvc.Export | Requests a CSV export of filtered items.
[**queue_definitions_get**](QueueDefinitionsApi.md#queue_definitions_get) | **GET** /odata/QueueDefinitions | Gets the list of queue definitions.
[**queue_definitions_get_by_id**](QueueDefinitionsApi.md#queue_definitions_get_by_id) | **GET** /odata/QueueDefinitions({key}) | Gets a single queue definition based on its Id.
[**queue_definitions_get_folders_for_queue_by_id**](QueueDefinitionsApi.md#queue_definitions_get_folders_for_queue_by_id) | **GET** /odata/QueueDefinitions/UiPath.Server.Configuration.OData.GetFoldersForQueue(id&#x3D;{id}) | Get all accesible folders where the queue is shared, and the total count of folders where it is shared (including unaccessible folders).
[**queue_definitions_get_json_schema_definition_by_id_and_jsonschematype**](QueueDefinitionsApi.md#queue_definitions_get_json_schema_definition_by_id_and_jsonschematype) | **GET** /odata/QueueDefinitions({key})/UiPathODataSvc.GetJsonSchemaDefinition(jsonSchemaType&#x3D;{jsonSchemaType}) | Gets a given queue item JSON schema as a .json file, based on queue definition id.
[**queue_definitions_get_queues_across_folders**](QueueDefinitionsApi.md#queue_definitions_get_queues_across_folders) | **GET** /odata/QueueDefinitions/UiPath.Server.Configuration.OData.GetQueuesAcrossFolders | Get the queues from all the folders in which the current user has the Queues.View permission, except the ones in the excluded folder.
[**queue_definitions_post**](QueueDefinitionsApi.md#queue_definitions_post) | **POST** /odata/QueueDefinitions | Creates a new queue.
[**queue_definitions_put_by_id**](QueueDefinitionsApi.md#queue_definitions_put_by_id) | **PUT** /odata/QueueDefinitions({key}) | Edits a queue.
[**queue_definitions_share_to_folders**](QueueDefinitionsApi.md#queue_definitions_share_to_folders) | **POST** /odata/QueueDefinitions/UiPath.Server.Configuration.OData.ShareToFolders | Makes the queue visible in the specified folders.


# **queue_definitions_delete_by_id**
> queue_definitions_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Deletes a queue based on its key.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.Delete.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Deletes a queue based on its key.
    api_instance.queue_definitions_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_delete_by_id: %s\n" % e)
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

# **queue_definitions_export_by_id**
> ExportModel queue_definitions_export_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Requests a CSV export of filtered items.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.View and Transactions.View.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
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
    # Requests a CSV export of filtered items.
    api_response = api_instance.queue_definitions_export_by_id(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_export_by_id: %s\n" % e)
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

[**ExportModel**](ExportModel.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_get**
> ODataValueOfIEnumerableOfQueueDefinitionDto queue_definitions_get(mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets the list of queue definitions.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
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
    # Gets the list of queue definitions.
    api_response = api_instance.queue_definitions_get(mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfQueueDefinitionDto**](ODataValueOfIEnumerableOfQueueDefinitionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_get_by_id**
> QueueDefinitionDto queue_definitions_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a single queue definition based on its Id.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a single queue definition based on its Id.
    api_response = api_instance.queue_definitions_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**QueueDefinitionDto**](QueueDefinitionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_get_folders_for_queue_by_id**
> AccessibleFoldersDto queue_definitions_get_folders_for_queue_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get all accesible folders where the queue is shared, and the total count of folders where it is shared (including unaccessible folders).

OAuth required scopes: OR.Queues or OR.Queues.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
id = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get all accesible folders where the queue is shared, and the total count of folders where it is shared (including unaccessible folders).
    api_response = api_instance.queue_definitions_get_folders_for_queue_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_get_folders_for_queue_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**AccessibleFoldersDto**](AccessibleFoldersDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_get_json_schema_definition_by_id_and_jsonschematype**
> file queue_definitions_get_json_schema_definition_by_id_and_jsonschematype(key, json_schema_type, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a given queue item JSON schema as a .json file, based on queue definition id.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.Edit.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
json_schema_type = 'json_schema_type_example' # str | Possible values: QueueSchemaType
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a given queue item JSON schema as a .json file, based on queue definition id.
    api_response = api_instance.queue_definitions_get_json_schema_definition_by_id_and_jsonschematype(key, json_schema_type, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_get_json_schema_definition_by_id_and_jsonschematype: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **json_schema_type** | **str**| Possible values: QueueSchemaType | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**file**](file.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_get_queues_across_folders**
> ODataValueOfIEnumerableOfQueueDefinitionDto queue_definitions_get_queues_across_folders(exclude_folder_id=exclude_folder_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get the queues from all the folders in which the current user has the Queues.View permission, except the ones in the excluded folder.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
exclude_folder_id = 789 # int |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get the queues from all the folders in which the current user has the Queues.View permission, except the ones in the excluded folder.
    api_response = api_instance.queue_definitions_get_queues_across_folders(exclude_folder_id=exclude_folder_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_get_queues_across_folders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude_folder_id** | **int**|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfQueueDefinitionDto**](ODataValueOfIEnumerableOfQueueDefinitionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_post**
> QueueDefinitionDto queue_definitions_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a new queue.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.Create.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.QueueDefinitionDto() # QueueDefinitionDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a new queue.
    api_response = api_instance.queue_definitions_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QueueDefinitionDto**](QueueDefinitionDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**QueueDefinitionDto**](QueueDefinitionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_put_by_id**
> queue_definitions_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Edits a queue.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Required permissions: Queues.Edit.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.QueueDefinitionDto() # QueueDefinitionDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Edits a queue.
    api_instance.queue_definitions_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**QueueDefinitionDto**](QueueDefinitionDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_definitions_share_to_folders**
> queue_definitions_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Makes the queue visible in the specified folders.

OAuth required scopes: OR.Queues or OR.Queues.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.QueueDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.QueueFoldersShareDto() # QueueFoldersShareDto | Object containing the ids of the queue definitions and the ids of the folders where they should be shared. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Makes the queue visible in the specified folders.
    api_instance.queue_definitions_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling QueueDefinitionsApi->queue_definitions_share_to_folders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QueueFoldersShareDto**](QueueFoldersShareDto.md)| Object containing the ids of the queue definitions and the ids of the folders where they should be shared. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

