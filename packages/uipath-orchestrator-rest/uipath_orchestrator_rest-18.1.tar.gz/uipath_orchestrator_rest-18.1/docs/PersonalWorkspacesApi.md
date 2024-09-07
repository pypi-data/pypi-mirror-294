# uipath_orchestrator_rest.PersonalWorkspacesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**personal_workspaces_convert_to_folder_by_id**](PersonalWorkspacesApi.md#personal_workspaces_convert_to_folder_by_id) | **POST** /odata/PersonalWorkspaces({key})/UiPath.Server.Configuration.OData.ConvertToFolder | Converts a Personal Workspace to a standard Folder.
[**personal_workspaces_get**](PersonalWorkspacesApi.md#personal_workspaces_get) | **GET** /odata/PersonalWorkspaces | Gets Personal Workspaces.
[**personal_workspaces_get_personal_workspace**](PersonalWorkspacesApi.md#personal_workspaces_get_personal_workspace) | **GET** /odata/PersonalWorkspaces/UiPath.Server.Configuration.OData.GetPersonalWorkspace | Gets Personal Workspace for current User
[**personal_workspaces_start_exploring_by_id**](PersonalWorkspacesApi.md#personal_workspaces_start_exploring_by_id) | **POST** /odata/PersonalWorkspaces({key})/UiPath.Server.Configuration.OData.StartExploring | Assigns the current User to explore a Personal Workspace.
[**personal_workspaces_stop_exploring_by_id**](PersonalWorkspacesApi.md#personal_workspaces_stop_exploring_by_id) | **POST** /odata/PersonalWorkspaces({key})/UiPath.Server.Configuration.OData.StopExploring | Unassigns the current User from exploring a Personal Workspace.


# **personal_workspaces_convert_to_folder_by_id**
> personal_workspaces_convert_to_folder_by_id(key, body=body)

Converts a Personal Workspace to a standard Folder.

OAuth authentication is not supported.  Required permissions: Units.Edit.

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
api_instance = uipath_orchestrator_rest.PersonalWorkspacesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.PersonalWorkspacesConvertToFolderRequest() # PersonalWorkspacesConvertToFolderRequest |  (optional)

try:
    # Converts a Personal Workspace to a standard Folder.
    api_instance.personal_workspaces_convert_to_folder_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling PersonalWorkspacesApi->personal_workspaces_convert_to_folder_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**PersonalWorkspacesConvertToFolderRequest**](PersonalWorkspacesConvertToFolderRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **personal_workspaces_get**
> ODataValueOfIEnumerableOfPersonalWorkspaceDto personal_workspaces_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets Personal Workspaces.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: Units.View.

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
api_instance = uipath_orchestrator_rest.PersonalWorkspacesApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets Personal Workspaces.
    api_response = api_instance.personal_workspaces_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonalWorkspacesApi->personal_workspaces_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfPersonalWorkspaceDto**](ODataValueOfIEnumerableOfPersonalWorkspaceDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **personal_workspaces_get_personal_workspace**
> PersonalWorkspaceDto personal_workspaces_get_personal_workspace(expand=expand, select=select)

Gets Personal Workspace for current User

OAuth authentication is not supported.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.PersonalWorkspacesApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets Personal Workspace for current User
    api_response = api_instance.personal_workspaces_get_personal_workspace(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonalWorkspacesApi->personal_workspaces_get_personal_workspace: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**PersonalWorkspaceDto**](PersonalWorkspaceDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **personal_workspaces_start_exploring_by_id**
> personal_workspaces_start_exploring_by_id(key)

Assigns the current User to explore a Personal Workspace.

OAuth authentication is not supported.  Required permissions: Units.Edit and Users.View and Roles.View.

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
api_instance = uipath_orchestrator_rest.PersonalWorkspacesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Assigns the current User to explore a Personal Workspace.
    api_instance.personal_workspaces_start_exploring_by_id(key)
except ApiException as e:
    print("Exception when calling PersonalWorkspacesApi->personal_workspaces_start_exploring_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **personal_workspaces_stop_exploring_by_id**
> personal_workspaces_stop_exploring_by_id(key)

Unassigns the current User from exploring a Personal Workspace.

OAuth authentication is not supported.  Required permissions: Units.Edit and Users.View and Roles.View.

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
api_instance = uipath_orchestrator_rest.PersonalWorkspacesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Unassigns the current User from exploring a Personal Workspace.
    api_instance.personal_workspaces_stop_exploring_by_id(key)
except ApiException as e:
    print("Exception when calling PersonalWorkspacesApi->personal_workspaces_stop_exploring_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

