# uipath_orchestrator_rest.TaskDefinitionsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**task_definitions_create_task_definition**](TaskDefinitionsApi.md#task_definitions_create_task_definition) | **POST** /odata/TaskDefinitions/UiPath.Server.Configuration.OData.CreateTaskDefinition | Creates a new Task Definition.
[**task_definitions_delete_by_id**](TaskDefinitionsApi.md#task_definitions_delete_by_id) | **DELETE** /odata/TaskDefinitions({key}) | Deletes Task Defintion/Version.
[**task_definitions_get**](TaskDefinitionsApi.md#task_definitions_get) | **GET** /odata/TaskDefinitions | Gets Task Definition objects with the given OData queries.
[**task_definitions_get_by_id**](TaskDefinitionsApi.md#task_definitions_get_by_id) | **GET** /odata/TaskDefinitions({key}) | Gets a Task Definition item by Id.
[**task_definitions_get_task_definition_versions_by_id**](TaskDefinitionsApi.md#task_definitions_get_task_definition_versions_by_id) | **GET** /odata/TaskDefinitions/UiPath.Server.Configuration.OData.GetTaskDefinitionVersions(id&#x3D;{id}) | Get all versions of Task Definition.
[**task_definitions_update_task_definition_by_id**](TaskDefinitionsApi.md#task_definitions_update_task_definition_by_id) | **POST** /odata/TaskDefinitions({key})/UiPath.Server.Configuration.OData.UpdateTaskDefinition | Updates Task Definition.


# **task_definitions_create_task_definition**
> TaskDefinitionDto task_definitions_create_task_definition(body=body, expand=expand, select=select)

Creates a new Task Definition.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: ActionDesign.Create.

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
api_instance = uipath_orchestrator_rest.TaskDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskDefinitionRequest() # TaskDefinitionRequest | The Task Definition to be created. (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Creates a new Task Definition.
    api_response = api_instance.task_definitions_create_task_definition(body=body, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskDefinitionsApi->task_definitions_create_task_definition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskDefinitionRequest**](TaskDefinitionRequest.md)| The Task Definition to be created. | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**TaskDefinitionDto**](TaskDefinitionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_definitions_delete_by_id**
> task_definitions_delete_by_id(key, task_definition_version=task_definition_version)

Deletes Task Defintion/Version.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: ActionDesign.Delete.

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
api_instance = uipath_orchestrator_rest.TaskDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Id of the task definition to be deleted
task_definition_version = 789 # int | Version of task definition to be deleted (optional)

try:
    # Deletes Task Defintion/Version.
    api_instance.task_definitions_delete_by_id(key, task_definition_version=task_definition_version)
except ApiException as e:
    print("Exception when calling TaskDefinitionsApi->task_definitions_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Id of the task definition to be deleted | 
 **task_definition_version** | **int**| Version of task definition to be deleted | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_definitions_get**
> ODataValueOfIEnumerableOfTaskDefinitionDto task_definitions_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets Task Definition objects with the given OData queries.

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Required permissions: ActionDesign.View.

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
api_instance = uipath_orchestrator_rest.TaskDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets Task Definition objects with the given OData queries.
    api_response = api_instance.task_definitions_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskDefinitionsApi->task_definitions_get: %s\n" % e)
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

### Return type

[**ODataValueOfIEnumerableOfTaskDefinitionDto**](ODataValueOfIEnumerableOfTaskDefinitionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_definitions_get_by_id**
> TaskDefinitionDto task_definitions_get_by_id(key, expand=expand, select=select)

Gets a Task Definition item by Id.

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Required permissions: ActionDesign.View.

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
api_instance = uipath_orchestrator_rest.TaskDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | id of the object
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a Task Definition item by Id.
    api_response = api_instance.task_definitions_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskDefinitionsApi->task_definitions_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| id of the object | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**TaskDefinitionDto**](TaskDefinitionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_definitions_get_task_definition_versions_by_id**
> TaskDefintionVersionDto task_definitions_get_task_definition_versions_by_id(id, expand=expand, select=select)

Get all versions of Task Definition.

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Required permissions: ActionDesign.View.

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
api_instance = uipath_orchestrator_rest.TaskDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
id = 789 # int | Id of the Task Definition
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Get all versions of Task Definition.
    api_response = api_instance.task_definitions_get_task_definition_versions_by_id(id, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskDefinitionsApi->task_definitions_get_task_definition_versions_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Id of the Task Definition | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**TaskDefintionVersionDto**](TaskDefintionVersionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_definitions_update_task_definition_by_id**
> task_definitions_update_task_definition_by_id(key, body=body)

Updates Task Definition.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: ActionDesign.Edit.

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
api_instance = uipath_orchestrator_rest.TaskDefinitionsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Key of the object
body = uipath_orchestrator_rest.TaskDefinitionRequest() # TaskDefinitionRequest | TaskDefinition to be updated (optional)

try:
    # Updates Task Definition.
    api_instance.task_definitions_update_task_definition_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling TaskDefinitionsApi->task_definitions_update_task_definition_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Key of the object | 
 **body** | [**TaskDefinitionRequest**](TaskDefinitionRequest.md)| TaskDefinition to be updated | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

