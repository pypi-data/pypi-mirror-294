# uipath_orchestrator_rest.AppTasksApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_tasks_complete_app_task**](AppTasksApi.md#app_tasks_complete_app_task) | **POST** /tasks/AppTasks/CompleteAppTask | Complete the task by saving app task data and action taken
[**app_tasks_create_app_task**](AppTasksApi.md#app_tasks_create_app_task) | **POST** /tasks/AppTasks/CreateAppTask | Creates a new App Task.
[**app_tasks_get_app_task_by_id**](AppTasksApi.md#app_tasks_get_app_task_by_id) | **GET** /tasks/AppTasks/GetAppTaskById | Returns dto to render app task
[**app_tasks_save_and_reassign_app_tasks**](AppTasksApi.md#app_tasks_save_and_reassign_app_tasks) | **POST** /tasks/AppTasks/SaveAndReassignAppTasks | Save changes done by the current user and Reassign Task to another user
[**app_tasks_save_app_tasks_data**](AppTasksApi.md#app_tasks_save_app_tasks_data) | **PUT** /tasks/AppTasks/SaveAppTasksData | Save task data


# **app_tasks_complete_app_task**
> app_tasks_complete_app_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Complete the task by saving app task data and action taken

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
api_instance = uipath_orchestrator_rest.AppTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskCompletionRequest() # TaskCompletionRequest | TaskCompletionRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Complete the task by saving app task data and action taken
    api_instance.app_tasks_complete_app_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling AppTasksApi->app_tasks_complete_app_task: %s\n" % e)
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

# **app_tasks_create_app_task**
> AppTasksDataDto app_tasks_create_app_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a new App Task.

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
api_instance = uipath_orchestrator_rest.AppTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.AppTasksCreateRequest() # AppTasksCreateRequest | The app task to be created. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a new App Task.
    api_response = api_instance.app_tasks_create_app_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppTasksApi->app_tasks_create_app_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AppTasksCreateRequest**](AppTasksCreateRequest.md)| The app task to be created. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**AppTasksDataDto**](AppTasksDataDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_tasks_get_app_task_by_id**
> AppTasksDataDto app_tasks_get_app_task_by_id(task_id=task_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns dto to render app task

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
api_instance = uipath_orchestrator_rest.AppTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
task_id = 789 # int | Task id (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns dto to render app task
    api_response = api_instance.app_tasks_get_app_task_by_id(task_id=task_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppTasksApi->app_tasks_get_app_task_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **int**| Task id | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**AppTasksDataDto**](AppTasksDataDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_tasks_save_and_reassign_app_tasks**
> app_tasks_save_and_reassign_app_tasks(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

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
api_instance = uipath_orchestrator_rest.AppTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskSaveAndReassignmentRequest() # TaskSaveAndReassignmentRequest | TaskSaveAndReassignmentRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Save changes done by the current user and Reassign Task to another user
    api_instance.app_tasks_save_and_reassign_app_tasks(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling AppTasksApi->app_tasks_save_and_reassign_app_tasks: %s\n" % e)
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

# **app_tasks_save_app_tasks_data**
> app_tasks_save_app_tasks_data(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Save task data

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
api_instance = uipath_orchestrator_rest.AppTasksApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskDataSaveRequest() # TaskDataSaveRequest | TaskDataSaveRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Save task data
    api_instance.app_tasks_save_app_tasks_data(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling AppTasksApi->app_tasks_save_app_tasks_data: %s\n" % e)
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

