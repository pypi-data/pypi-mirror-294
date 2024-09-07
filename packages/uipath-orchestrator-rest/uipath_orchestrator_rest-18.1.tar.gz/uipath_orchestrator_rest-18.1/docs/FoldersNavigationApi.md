# uipath_orchestrator_rest.FoldersNavigationApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**folders_navigation_get_all_folders_for_current_user**](FoldersNavigationApi.md#folders_navigation_get_all_folders_for_current_user) | **GET** /api/FoldersNavigation/GetAllFoldersForCurrentUser | Returns the folders the current user has access to.  The response will be a list of folders; the hierarchy can be reconstructed  using the ParentId properties. From the root to the folders the user has  actually been assigned to, the folders will be marked as non-selectable  and only the paths to the assigned-to folders will be included.  From the assigned-to folders down to the leaves, the nodes will be marked as  selectable and their children lists fully populated.
[**folders_navigation_get_all_roles_for_user**](FoldersNavigationApi.md#folders_navigation_get_all_roles_for_user) | **GET** /api/FoldersNavigation/GetAllRolesForUser | Returns a page of the user-folder assignments for the input user, including the roles for each folder.  The response also includes the folders assigned to the directory groups of the user.  The distinction between the folders assigned directly to the user and the ones assigned to one of his groups  can be made via the User field of the response.
[**folders_navigation_get_folder_navigation_context_for_current_user**](FoldersNavigationApi.md#folders_navigation_get_folder_navigation_context_for_current_user) | **GET** /api/FoldersNavigation/GetFolderNavigationContextForCurrentUser | Returns a subset (paginated) of direct children for a given folder, which are accessible to the current user.  To ease a folder tree structure navigation design, the list of ancestors for the given folder is also returned.
[**folders_navigation_get_folders_for_current_user**](FoldersNavigationApi.md#folders_navigation_get_folders_for_current_user) | **GET** /api/FoldersNavigation/GetFoldersForCurrentUser | Returns a filtered subset (paginated) of the folders the current user has access to.


# **folders_navigation_get_all_folders_for_current_user**
> list[ExtendedFolderDto] folders_navigation_get_all_folders_for_current_user()

Returns the folders the current user has access to.  The response will be a list of folders; the hierarchy can be reconstructed  using the ParentId properties. From the root to the folders the user has  actually been assigned to, the folders will be marked as non-selectable  and only the paths to the assigned-to folders will be included.  From the assigned-to folders down to the leaves, the nodes will be marked as  selectable and their children lists fully populated.

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
api_instance = uipath_orchestrator_rest.FoldersNavigationApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Returns the folders the current user has access to.  The response will be a list of folders; the hierarchy can be reconstructed  using the ParentId properties. From the root to the folders the user has  actually been assigned to, the folders will be marked as non-selectable  and only the paths to the assigned-to folders will be included.  From the assigned-to folders down to the leaves, the nodes will be marked as  selectable and their children lists fully populated.
    api_response = api_instance.folders_navigation_get_all_folders_for_current_user()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersNavigationApi->folders_navigation_get_all_folders_for_current_user: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ExtendedFolderDto]**](ExtendedFolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_navigation_get_all_roles_for_user**
> UserRoleAssignmentsDto folders_navigation_get_all_roles_for_user(username=username, type=type, skip=skip, take=take, search_text=search_text)

Returns a page of the user-folder assignments for the input user, including the roles for each folder.  The response also includes the folders assigned to the directory groups of the user.  The distinction between the folders assigned directly to the user and the ones assigned to one of his groups  can be made via the User field of the response.

OAuth authentication is not supported.  Required permissions: (Units.View - Gets roles from all folders) and (SubFolders.View - Gets roles only from folders where caller has SubFolders.View permission).

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
api_instance = uipath_orchestrator_rest.FoldersNavigationApi(uipath_orchestrator_rest.ApiClient(configuration))
username = 'username_example' # str | User name (optional)
type = 'type_example' # str |  (optional)
skip = 56 # int |  (optional)
take = 56 # int |  (optional)
search_text = 'search_text_example' # str |  (optional)

try:
    # Returns a page of the user-folder assignments for the input user, including the roles for each folder.  The response also includes the folders assigned to the directory groups of the user.  The distinction between the folders assigned directly to the user and the ones assigned to one of his groups  can be made via the User field of the response.
    api_response = api_instance.folders_navigation_get_all_roles_for_user(username=username, type=type, skip=skip, take=take, search_text=search_text)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersNavigationApi->folders_navigation_get_all_roles_for_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**| User name | [optional] 
 **type** | **str**|  | [optional] 
 **skip** | **int**|  | [optional] 
 **take** | **int**|  | [optional] 
 **search_text** | **str**|  | [optional] 

### Return type

[**UserRoleAssignmentsDto**](UserRoleAssignmentsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_navigation_get_folder_navigation_context_for_current_user**
> FolderNavigationContextDto folders_navigation_get_folder_navigation_context_for_current_user(skip=skip, take=take, folder_id=folder_id)

Returns a subset (paginated) of direct children for a given folder, which are accessible to the current user.  To ease a folder tree structure navigation design, the list of ancestors for the given folder is also returned.

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
api_instance = uipath_orchestrator_rest.FoldersNavigationApi(uipath_orchestrator_rest.ApiClient(configuration))
skip = 56 # int |  (optional)
take = 56 # int |  (optional)
folder_id = 789 # int |  (optional)

try:
    # Returns a subset (paginated) of direct children for a given folder, which are accessible to the current user.  To ease a folder tree structure navigation design, the list of ancestors for the given folder is also returned.
    api_response = api_instance.folders_navigation_get_folder_navigation_context_for_current_user(skip=skip, take=take, folder_id=folder_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersNavigationApi->folders_navigation_get_folder_navigation_context_for_current_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] 
 **take** | **int**|  | [optional] 
 **folder_id** | **int**|  | [optional] 

### Return type

[**FolderNavigationContextDto**](FolderNavigationContextDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_navigation_get_folders_for_current_user**
> PageResultDtoOfPathAwareFolderDto folders_navigation_get_folders_for_current_user(skip=skip, take=take, search_text=search_text, folder_types=folder_types)

Returns a filtered subset (paginated) of the folders the current user has access to.

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
api_instance = uipath_orchestrator_rest.FoldersNavigationApi(uipath_orchestrator_rest.ApiClient(configuration))
skip = 56 # int |  (optional)
take = 56 # int |  (optional)
search_text = 'search_text_example' # str |  (optional)
folder_types = ['folder_types_example'] # list[str] |  (optional)

try:
    # Returns a filtered subset (paginated) of the folders the current user has access to.
    api_response = api_instance.folders_navigation_get_folders_for_current_user(skip=skip, take=take, search_text=search_text, folder_types=folder_types)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersNavigationApi->folders_navigation_get_folders_for_current_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] 
 **take** | **int**|  | [optional] 
 **search_text** | **str**|  | [optional] 
 **folder_types** | [**list[str]**](str.md)|  | [optional] 

### Return type

[**PageResultDtoOfPathAwareFolderDto**](PageResultDtoOfPathAwareFolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

