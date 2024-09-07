# uipath_orchestrator_rest.TaskFormsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**task_forms_bulk_complete_tasks**](TaskFormsApi.md#task_forms_bulk_complete_tasks) | **POST** /forms/TaskForms/BulkCompleteTasks | Bulk Complete the task by merging form data and action taken
[**task_forms_bulk_update_tasks**](TaskFormsApi.md#task_forms_bulk_update_tasks) | **PUT** /forms/TaskForms/BulkUpdateTasks | Bulk Update Task data by merging data.
[**task_forms_complete_task**](TaskFormsApi.md#task_forms_complete_task) | **POST** /forms/TaskForms/CompleteTask | Complete the task by saving form data and action taken
[**task_forms_create_form_task**](TaskFormsApi.md#task_forms_create_form_task) | **POST** /forms/TaskForms/CreateFormTask | Creates a new Form Task.
[**task_forms_get_task_data_by_id**](TaskFormsApi.md#task_forms_get_task_data_by_id) | **GET** /forms/TaskForms/GetTaskDataById | Returns task data dto
[**task_forms_get_task_form_by_id**](TaskFormsApi.md#task_forms_get_task_form_by_id) | **GET** /forms/TaskForms/GetTaskFormById | Returns form dto to render task form
[**task_forms_save_and_reassign_task**](TaskFormsApi.md#task_forms_save_and_reassign_task) | **POST** /forms/TaskForms/SaveAndReassignTask | Save changes done by the current user and Reassign Task to another user
[**task_forms_save_task_data**](TaskFormsApi.md#task_forms_save_task_data) | **PUT** /forms/TaskForms/SaveTaskData | Save task data


# **task_forms_bulk_complete_tasks**
> list[BulkOperationErrorResponse] task_forms_bulk_complete_tasks(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Bulk Complete the task by merging form data and action taken

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.BulkTasksCompletionRequest() # BulkTasksCompletionRequest | BulkTasksCompletionRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Bulk Complete the task by merging form data and action taken
    api_response = api_instance.task_forms_bulk_complete_tasks(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_bulk_complete_tasks: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BulkTasksCompletionRequest**](BulkTasksCompletionRequest.md)| BulkTasksCompletionRequest | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**list[BulkOperationErrorResponse]**](BulkOperationErrorResponse.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_forms_bulk_update_tasks**
> list[BulkOperationErrorResponse] task_forms_bulk_update_tasks(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Bulk Update Task data by merging data.

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.BulkTasksDataUpdateRequest() # BulkTasksDataUpdateRequest | BulkTasksDataUpdateRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Bulk Update Task data by merging data.
    api_response = api_instance.task_forms_bulk_update_tasks(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_bulk_update_tasks: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BulkTasksDataUpdateRequest**](BulkTasksDataUpdateRequest.md)| BulkTasksDataUpdateRequest | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**list[BulkOperationErrorResponse]**](BulkOperationErrorResponse.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_forms_complete_task**
> task_forms_complete_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Complete the task by saving form data and action taken

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskCompletionRequest() # TaskCompletionRequest | TaskCompletionRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Complete the task by saving form data and action taken
    api_instance.task_forms_complete_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_complete_task: %s\n" % e)
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

# **task_forms_create_form_task**
> TaskDataDto task_forms_create_form_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a new Form Task.

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.FormTaskCreateRequest() # FormTaskCreateRequest | The form task to be created. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a new Form Task.
    api_response = api_instance.task_forms_create_form_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_create_form_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FormTaskCreateRequest**](FormTaskCreateRequest.md)| The form task to be created. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TaskDataDto**](TaskDataDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_forms_get_task_data_by_id**
> TaskDataDto task_forms_get_task_data_by_id(task_id=task_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
task_id = 789 # int | Task id (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns task data dto
    api_response = api_instance.task_forms_get_task_data_by_id(task_id=task_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_get_task_data_by_id: %s\n" % e)
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

# **task_forms_get_task_form_by_id**
> TaskFormDto task_forms_get_task_form_by_id(task_id=task_id, expand_on_form_layout=expand_on_form_layout, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns form dto to render task form

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
task_id = 789 # int | Task id (optional)
expand_on_form_layout = false # bool |  (optional) (default to false)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns form dto to render task form
    api_response = api_instance.task_forms_get_task_form_by_id(task_id=task_id, expand_on_form_layout=expand_on_form_layout, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_get_task_form_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **int**| Task id | [optional] 
 **expand_on_form_layout** | **bool**|  | [optional] [default to false]
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TaskFormDto**](TaskFormDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_forms_save_and_reassign_task**
> task_forms_save_and_reassign_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskSaveAndReassignmentRequest() # TaskSaveAndReassignmentRequest | TaskSaveAndReassignmentRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Save changes done by the current user and Reassign Task to another user
    api_instance.task_forms_save_and_reassign_task(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_save_and_reassign_task: %s\n" % e)
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

# **task_forms_save_task_data**
> task_forms_save_task_data(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

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
api_instance = uipath_orchestrator_rest.TaskFormsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskDataSaveRequest() # TaskDataSaveRequest | TaskDataSaveRequest (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Save task data
    api_instance.task_forms_save_task_data(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TaskFormsApi->task_forms_save_task_data: %s\n" % e)
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

