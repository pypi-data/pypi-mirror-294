# uipath_orchestrator_rest.GenericTasksApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generic_tasks_complete_task**](GenericTasksApi.md#generic_tasks_complete_task) | **POST** /tasks/GenericTasks/CompleteTask | Complete the task by saving task data and action taken
[**generic_tasks_create_task**](GenericTasksApi.md#generic_tasks_create_task) | **POST** /tasks/GenericTasks/CreateTask | Creates a new Generic Task.
[**generic_tasks_get_task_data_by_id**](GenericTasksApi.md#generic_tasks_get_task_data_by_id) | **GET** /tasks/GenericTasks/GetTaskDataById | Returns task data dto
[**generic_tasks_save_and_reassign_task**](GenericTasksApi.md#generic_tasks_save_and_reassign_task) | **POST** /tasks/GenericTasks/SaveAndReassignTask | Save changes done by the current user and Reassign Task to another user
[**generic_tasks_save_task_data**](GenericTasksApi.md#generic_tasks_save_task_data) | **PUT** /tasks/GenericTasks/SaveTaskData | Save Task data
[**generic_tasks_save_task_tags**](GenericTasksApi.md#generic_tasks_save_task_tags) | **PUT** /tasks/GenericTasks/SaveTaskTags | Save tags for a task


# **generic_tasks_complete_task**
> generic_tasks_complete_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Complete the task by saving task data and action taken

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: Tasks.Edit.

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
api_instance = uipath_orchestrator_rest.GenericTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskCompletionRequest() # TaskCompletionRequest | TaskCompletionRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Complete the task by saving task data and action taken
    api_instance.generic_tasks_complete_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling GenericTasksApi->generic_tasks_complete_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskCompletionRequest**](TaskCompletionRequest.md)| TaskCompletionRequest | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generic_tasks_create_task**
> TaskDataDto generic_tasks_create_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a new Generic Task.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: Tasks.Create.

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
api_instance = uipath_orchestrator_rest.GenericTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskCreateRequest() # TaskCreateRequest | The task to be created. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a new Generic Task.
    api_response = api_instance.generic_tasks_create_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GenericTasksApi->generic_tasks_create_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskCreateRequest**](TaskCreateRequest.md)| The task to be created. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TaskDataDto**](TaskDataDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generic_tasks_get_task_data_by_id**
> TaskDataDto generic_tasks_get_task_data_by_id(task_id=task_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns task data dto

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Required permissions: Tasks.View.

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
api_instance = uipath_orchestrator_rest.GenericTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
task_id = 789 # int | Task id (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns task data dto
    api_response = api_instance.generic_tasks_get_task_data_by_id(task_id=task_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GenericTasksApi->generic_tasks_get_task_data_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **int**| Task id | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TaskDataDto**](TaskDataDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generic_tasks_save_and_reassign_task**
> generic_tasks_save_and_reassign_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Save changes done by the current user and Reassign Task to another user

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: Tasks.Edit.

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
api_instance = uipath_orchestrator_rest.GenericTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskSaveAndReassignmentRequest() # TaskSaveAndReassignmentRequest | TaskSaveAndReassignmentRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Save changes done by the current user and Reassign Task to another user
    api_instance.generic_tasks_save_and_reassign_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling GenericTasksApi->generic_tasks_save_and_reassign_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskSaveAndReassignmentRequest**](TaskSaveAndReassignmentRequest.md)| TaskSaveAndReassignmentRequest | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generic_tasks_save_task_data**
> generic_tasks_save_task_data(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Save Task data

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: Tasks.Edit.

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
api_instance = uipath_orchestrator_rest.GenericTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskDataSaveRequest() # TaskDataSaveRequest | TaskDataSaveRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Save Task data
    api_instance.generic_tasks_save_task_data(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling GenericTasksApi->generic_tasks_save_task_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskDataSaveRequest**](TaskDataSaveRequest.md)| TaskDataSaveRequest | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generic_tasks_save_task_tags**
> generic_tasks_save_task_tags(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Save tags for a task

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: Tasks.Edit.

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
api_instance = uipath_orchestrator_rest.GenericTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskTagsSaveRequest() # TaskTagsSaveRequest | TaskTagsSaveRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Save tags for a task
    api_instance.generic_tasks_save_task_tags(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling GenericTasksApi->generic_tasks_save_task_tags: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskTagsSaveRequest**](TaskTagsSaveRequest.md)| TaskTagsSaveRequest | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

