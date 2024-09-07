# uipath_orchestrator_rest.FoldersApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**folders_assign_domain_user**](FoldersApi.md#folders_assign_domain_user) | **POST** /odata/Folders/UiPath.Server.Configuration.OData.AssignDomainUser | Assigns a directory user or group to a set of folders with an optional set of roles per folder.
[**folders_assign_machines**](FoldersApi.md#folders_assign_machines) | **POST** /odata/Folders/UiPath.Server.Configuration.OData.AssignMachines | Assigns one or more machines to a set of folders.
[**folders_assign_users**](FoldersApi.md#folders_assign_users) | **POST** /odata/Folders/UiPath.Server.Configuration.OData.AssignUsers | Assigns one or more users to a set of folders with an optional set of roles per folder.
[**folders_delete_by_id**](FoldersApi.md#folders_delete_by_id) | **DELETE** /odata/Folders({key}) | Deletes a folder. Succeeds only if no entities or user associations  exist in this folder or any of its descendants.
[**folders_delete_by_key**](FoldersApi.md#folders_delete_by_key) | **DELETE** /api/Folders/DeleteByKey | Deletes a folder. Succeeds only if no entities or user associations  exist in this folder or any of its descendants.
[**folders_get**](FoldersApi.md#folders_get) | **GET** /odata/Folders | Gets folders.
[**folders_get_all_roles_for_user_by_username_and_skip_and_take**](FoldersApi.md#folders_get_all_roles_for_user_by_username_and_skip_and_take) | **GET** /odata/Folders/UiPath.Server.Configuration.OData.GetAllRolesForUser(username&#x3D;{username},skip&#x3D;{skip},take&#x3D;{take}) | Returns a page of the user-folder assignments for the input user, including the roles for each folder.  The response also includes the folders assigned to the directory groups of the user.  The distinction between the folders assigned directly to the user and the ones assigned to one of his groups  can be made via the User field of the response.  LIMITATION: If URI parameters contain special characters (eg. \\, /), use instead api/FoldersNavigation/GetAllRolesForUser endpoint.
[**folders_get_by_id**](FoldersApi.md#folders_get_by_id) | **GET** /odata/Folders({key}) | Gets a single folder, based on its Id.
[**folders_get_by_key_by_identifier**](FoldersApi.md#folders_get_by_key_by_identifier) | **GET** /odata/Folders/UiPath.Server.Configuration.OData.GetByKey(identifier&#x3D;{identifier}) | Gets a single folder, based on its Key.
[**folders_get_machines_for_folder_by_key**](FoldersApi.md#folders_get_machines_for_folder_by_key) | **GET** /odata/Folders/UiPath.Server.Configuration.OData.GetMachinesForFolder(key&#x3D;{key}) | Returns the machines assigned to a folder.
[**folders_get_move_folder_machines_changes**](FoldersApi.md#folders_get_move_folder_machines_changes) | **GET** /odata/Folders/UiPath.Server.Configuration.OData.GetMoveFolderMachinesChanges | Gets the machine changes when moving a folder
[**folders_get_subfolders_with_assigned_machine**](FoldersApi.md#folders_get_subfolders_with_assigned_machine) | **GET** /odata/Folders/UiPath.Server.Configuration.OData.GetSubfoldersWithAssignedMachine | Gets direct machine assignments for all subfolders of the specific folder
[**folders_get_users_for_folder_by_key_and_includeinherited**](FoldersApi.md#folders_get_users_for_folder_by_key_and_includeinherited) | **GET** /odata/Folders/UiPath.Server.Configuration.OData.GetUsersForFolder(key&#x3D;{key},includeInherited&#x3D;{includeInherited}) | Returns the users who have access to a folder and optionally the fine-grained roles each one  has on that folder.
[**folders_move_folder_by_folderid**](FoldersApi.md#folders_move_folder_by_folderid) | **PUT** /odata/Folders({folderId})/UiPath.Server.Configuration.OData.MoveFolder | Move a folder.
[**folders_patch_name_description**](FoldersApi.md#folders_patch_name_description) | **PATCH** /api/Folders/PatchNameDescription | Edits a folder.
[**folders_post**](FoldersApi.md#folders_post) | **POST** /odata/Folders | Creates a new folder.
[**folders_put_by_id**](FoldersApi.md#folders_put_by_id) | **PUT** /odata/Folders({key}) | Edits a folder.
[**folders_remove_machines_from_folder_by_id**](FoldersApi.md#folders_remove_machines_from_folder_by_id) | **POST** /odata/Folders({key})/UiPath.Server.Configuration.OData.RemoveMachinesFromFolder | Remove user assignment from a folder.
[**folders_remove_user_from_folder_by_id**](FoldersApi.md#folders_remove_user_from_folder_by_id) | **POST** /odata/Folders({key})/UiPath.Server.Configuration.OData.RemoveUserFromFolder | Remove user assignment from a folder.
[**folders_toggle_folder_machine_inherit**](FoldersApi.md#folders_toggle_folder_machine_inherit) | **POST** /odata/Folders/UiPath.Server.Configuration.OData.ToggleFolderMachineInherit | Toggle machine propagation for a folder to all subfolders.
[**folders_update_machines_to_folder_associations**](FoldersApi.md#folders_update_machines_to_folder_associations) | **POST** /odata/Folders/UiPath.Server.Configuration.OData.UpdateMachinesToFolderAssociations | Add and remove machine associations to a folder


# **folders_assign_domain_user**
> folders_assign_domain_user(body=body)

Assigns a directory user or group to a set of folders with an optional set of roles per folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Assigns domain user to any folder or only if user has SubFolders.Edit permission on all folders provided).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.FolderAssignDomainUserRequest() # FolderAssignDomainUserRequest |  (optional)

try:
    # Assigns a directory user or group to a set of folders with an optional set of roles per folder.
    api_instance.folders_assign_domain_user(body=body)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_assign_domain_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FolderAssignDomainUserRequest**](FolderAssignDomainUserRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_assign_machines**
> folders_assign_machines(body=body)

Assigns one or more machines to a set of folders.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Assigns machines to any folder or only if user has SubFolders.Edit permission on all folders provided).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.FolderAssignMachinesRequest() # FolderAssignMachinesRequest |  (optional)

try:
    # Assigns one or more machines to a set of folders.
    api_instance.folders_assign_machines(body=body)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_assign_machines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FolderAssignMachinesRequest**](FolderAssignMachinesRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_assign_users**
> folders_assign_users(body=body)

Assigns one or more users to a set of folders with an optional set of roles per folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Assigns users to any folder or if the user has SubFolders.Edit permission on all folders provided).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.FolderAssignUsersRequest() # FolderAssignUsersRequest |  (optional)

try:
    # Assigns one or more users to a set of folders with an optional set of roles per folder.
    api_instance.folders_assign_users(body=body)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_assign_users: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FolderAssignUsersRequest**](FolderAssignUsersRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_delete_by_id**
> folders_delete_by_id(key)

Deletes a folder. Succeeds only if no entities or user associations  exist in this folder or any of its descendants.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Delete or SubFolders.Delete - Deletes any folder or only if user has SubFolders.Delete permission on the provided folder).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Deletes a folder. Succeeds only if no entities or user associations  exist in this folder or any of its descendants.
    api_instance.folders_delete_by_id(key)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_delete_by_id: %s\n" % e)
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

# **folders_delete_by_key**
> folders_delete_by_key(key=key)

Deletes a folder. Succeeds only if no entities or user associations  exist in this folder or any of its descendants.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Delete or SubFolders.Delete - Deletes any folder or only if user has SubFolders.Delete permission on the provided folder).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str |  (optional)

try:
    # Deletes a folder. Succeeds only if no entities or user associations  exist in this folder or any of its descendants.
    api_instance.folders_delete_by_key(key=key)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_delete_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | [**str**](.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get**
> ODataValueOfIEnumerableOfFolderDto folders_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets folders.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (Units.View or SubFolders.View - Gets all folders or only the folders where user has SubFolders.View permission).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets folders.
    api_response = api_instance.folders_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfFolderDto**](ODataValueOfIEnumerableOfFolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get_all_roles_for_user_by_username_and_skip_and_take**
> UserRoleAssignmentsDto folders_get_all_roles_for_user_by_username_and_skip_and_take(username, skip, take, type=type, search_text=search_text, expand=expand, select=select)

Returns a page of the user-folder assignments for the input user, including the roles for each folder.  The response also includes the folders assigned to the directory groups of the user.  The distinction between the folders assigned directly to the user and the ones assigned to one of his groups  can be made via the User field of the response.  LIMITATION: If URI parameters contain special characters (eg. \\, /), use instead api/FoldersNavigation/GetAllRolesForUser endpoint.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (Units.View or SubFolders.View - Gets roles from all folders or only from folders where user has SubFolders.View permission).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
username = 'username_example' # str | User name
skip = 56 # int | 
take = 56 # int | 
type = 'User' # str |  (optional) (default to User)
search_text = 'search_text_example' # str |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Returns a page of the user-folder assignments for the input user, including the roles for each folder.  The response also includes the folders assigned to the directory groups of the user.  The distinction between the folders assigned directly to the user and the ones assigned to one of his groups  can be made via the User field of the response.  LIMITATION: If URI parameters contain special characters (eg. \\, /), use instead api/FoldersNavigation/GetAllRolesForUser endpoint.
    api_response = api_instance.folders_get_all_roles_for_user_by_username_and_skip_and_take(username, skip, take, type=type, search_text=search_text, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get_all_roles_for_user_by_username_and_skip_and_take: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**| User name | 
 **skip** | **int**|  | 
 **take** | **int**|  | 
 **type** | **str**|  | [optional] [default to User]
 **search_text** | **str**|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**UserRoleAssignmentsDto**](UserRoleAssignmentsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get_by_id**
> FolderDto folders_get_by_id(key, expand=expand, select=select)

Gets a single folder, based on its Id.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (Units.View or SubFolders.View - Gets any folder or only the folder if user has SubFolders.View permission on it or the user is assigned to the folder.).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a single folder, based on its Id.
    api_response = api_instance.folders_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**FolderDto**](FolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get_by_key_by_identifier**
> FolderDto folders_get_by_key_by_identifier(identifier, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets a single folder, based on its Key.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (Units.View or SubFolders.View - Gets any folder or only the folder if user has SubFolders.View permission on it or the user is assigned to the folder.).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
identifier = 'identifier_example' # str | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets a single folder, based on its Key.
    api_response = api_instance.folders_get_by_key_by_identifier(identifier, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get_by_key_by_identifier: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**str**](.md)|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**FolderDto**](FolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get_machines_for_folder_by_key**
> ODataValueOfIEnumerableOfMachineFolderDto folders_get_machines_for_folder_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Returns the machines assigned to a folder.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (Units.View or SubFolders.View - Gets machines for any folder or only if user has SubFolders.View permission on folder).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns the machines assigned to a folder.
    api_response = api_instance.folders_get_machines_for_folder_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get_machines_for_folder_by_key: %s\n" % e)
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

### Return type

[**ODataValueOfIEnumerableOfMachineFolderDto**](ODataValueOfIEnumerableOfMachineFolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get_move_folder_machines_changes**
> ODataValueOfIEnumerableOfMoveFolderMachineChange folders_get_move_folder_machines_changes(folder_id=folder_id, target_parent_id=target_parent_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Gets the machine changes when moving a folder

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (SubFolders.Delete - Deletes folder only if user has SubFolders.Delete permission on it) and (Units.Create or SubFolders.Create - Creates root or subfolder or only subfolder if user has SubFolders.Create permission on parent) and (Units.Edit or SubFolders.Edit - Edits any folder or only if user has SubFolders.Edit permission on it).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
folder_id = 789 # int | Id of the folder to be moved (optional)
target_parent_id = 789 # int | Id of the target parent (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets the machine changes when moving a folder
    api_response = api_instance.folders_get_move_folder_machines_changes(folder_id=folder_id, target_parent_id=target_parent_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get_move_folder_machines_changes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **folder_id** | **int**| Id of the folder to be moved | [optional] 
 **target_parent_id** | **int**| Id of the target parent | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfMoveFolderMachineChange**](ODataValueOfIEnumerableOfMoveFolderMachineChange.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get_subfolders_with_assigned_machine**
> ODataValueOfIEnumerableOfFolderDto folders_get_subfolders_with_assigned_machine(root_folder_id=root_folder_id, machine_id=machine_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets direct machine assignments for all subfolders of the specific folder

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (Units.View or SubFolders.View - Gets the subfolders in which the machines is directly assigned for any folder or for subfolders only).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
root_folder_id = 789 # int |  (optional)
machine_id = 789 # int |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets direct machine assignments for all subfolders of the specific folder
    api_response = api_instance.folders_get_subfolders_with_assigned_machine(root_folder_id=root_folder_id, machine_id=machine_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get_subfolders_with_assigned_machine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **root_folder_id** | **int**|  | [optional] 
 **machine_id** | **int**|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfFolderDto**](ODataValueOfIEnumerableOfFolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_get_users_for_folder_by_key_and_includeinherited**
> ODataValueOfIEnumerableOfUserRolesDto folders_get_users_for_folder_by_key_and_includeinherited(key, include_inherited, include_alerts_enabled=include_alerts_enabled, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Returns the users who have access to a folder and optionally the fine-grained roles each one  has on that folder.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: (Units.View or SubFolders.View or Assets.Create or Assets.Edit - Gets users for any folder or if the user has SubFolders.View/Assets.Create/Assets.Edit permission on the provided folder).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
include_inherited = true # bool | If true, the response will include users inherited from ancestors
include_alerts_enabled = false # bool | If true, the response will include alert preferences for each user (optional) (default to false)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns the users who have access to a folder and optionally the fine-grained roles each one  has on that folder.
    api_response = api_instance.folders_get_users_for_folder_by_key_and_includeinherited(key, include_inherited, include_alerts_enabled=include_alerts_enabled, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_get_users_for_folder_by_key_and_includeinherited: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **include_inherited** | **bool**| If true, the response will include users inherited from ancestors | 
 **include_alerts_enabled** | **bool**| If true, the response will include alert preferences for each user | [optional] [default to false]
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfUserRolesDto**](ODataValueOfIEnumerableOfUserRolesDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_move_folder_by_folderid**
> folders_move_folder_by_folderid(folder_id, target_parent_id=target_parent_id)

Move a folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Delete or SubFolders.Delete - Move any folder or to folder only if user has SubFolders.Delete permission on it) and (Units.Create or SubFolders.Create - Move to any target folder or to folder if user has SubFolders.Create permission on target) and (Units.Edit or SubFolders.Edit - Move to any target folder or to folder if user has SubFolders.Edit permission on target).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
folder_id = 789 # int | Id of the folder to be moved
target_parent_id = 789 # int | Id of the target parent (optional)

try:
    # Move a folder.
    api_instance.folders_move_folder_by_folderid(folder_id, target_parent_id=target_parent_id)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_move_folder_by_folderid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **folder_id** | **int**| Id of the folder to be moved | 
 **target_parent_id** | **int**| Id of the target parent | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_patch_name_description**
> FolderDto folders_patch_name_description(body=body, key=key)

Edits a folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Edits any folder or edits only if user has SubFolders.Edit permission on the provided folder).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.FolderUpdateNameDescriptionRequest() # FolderUpdateNameDescriptionRequest |  (optional)
key = 'key_example' # str |  (optional)

try:
    # Edits a folder.
    api_response = api_instance.folders_patch_name_description(body=body, key=key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_patch_name_description: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FolderUpdateNameDescriptionRequest**](FolderUpdateNameDescriptionRequest.md)|  | [optional] 
 **key** | [**str**](.md)|  | [optional] 

### Return type

[**FolderDto**](FolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_post**
> FolderDto folders_post(body=body)

Creates a new folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Create or SubFolders.Create - Creates root or subfolder or only subfolder if user has SubFolders.Create permission on parent).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.FolderDto() # FolderDto |  (optional)

try:
    # Creates a new folder.
    api_response = api_instance.folders_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FolderDto**](FolderDto.md)|  | [optional] 

### Return type

[**FolderDto**](FolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_put_by_id**
> FolderDto folders_put_by_id(key, body=body)

Edits a folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Edits any folder or edits only if user has SubFolders.Edit permission on the provided folder).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.FolderDto() # FolderDto |  (optional)

try:
    # Edits a folder.
    api_response = api_instance.folders_put_by_id(key, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**FolderDto**](FolderDto.md)|  | [optional] 

### Return type

[**FolderDto**](FolderDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_remove_machines_from_folder_by_id**
> folders_remove_machines_from_folder_by_id(key, body=body)

Remove user assignment from a folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Removes machines from any folder or only if caller has SubFolders.Edit permission the folder provided).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.RemoveMachinesFromFolderRequest() # RemoveMachinesFromFolderRequest | The Ids of the machines to remove from the folder (optional)

try:
    # Remove user assignment from a folder.
    api_instance.folders_remove_machines_from_folder_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_remove_machines_from_folder_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**RemoveMachinesFromFolderRequest**](RemoveMachinesFromFolderRequest.md)| The Ids of the machines to remove from the folder | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_remove_user_from_folder_by_id**
> folders_remove_user_from_folder_by_id(key, body=body)

Remove user assignment from a folder.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Remove user from any folder or only if caller has SubFolders.Edit permission on provided folder).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.RemoveUserFromFolderRequest() # RemoveUserFromFolderRequest | userId - The Id of the user to remove from the folder (optional)

try:
    # Remove user assignment from a folder.
    api_instance.folders_remove_user_from_folder_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_remove_user_from_folder_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**RemoveUserFromFolderRequest**](RemoveUserFromFolderRequest.md)| userId - The Id of the user to remove from the folder | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_toggle_folder_machine_inherit**
> folders_toggle_folder_machine_inherit(body=body)

Toggle machine propagation for a folder to all subfolders.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Propagate machine to subfolders only if Units.Edit permission is provided or only if SubFolders.Edit permission on all folders provided).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.FolderMachineInheritDto() # FolderMachineInheritDto |  (optional)

try:
    # Toggle machine propagation for a folder to all subfolders.
    api_instance.folders_toggle_folder_machine_inherit(body=body)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_toggle_folder_machine_inherit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FolderMachineInheritDto**](FolderMachineInheritDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folders_update_machines_to_folder_associations**
> folders_update_machines_to_folder_associations(body=body)

Add and remove machine associations to a folder

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: (Units.Edit or SubFolders.Edit - Update machines to any folder associations or only if user has SubFolders.Edit permission on all folders provided).

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
api_instance = uipath_orchestrator_rest.FoldersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.UpdateMachinesToFolderAssociationsRequest() # UpdateMachinesToFolderAssociationsRequest |  (optional)

try:
    # Add and remove machine associations to a folder
    api_instance.folders_update_machines_to_folder_associations(body=body)
except ApiException as e:
    print("Exception when calling FoldersApi->folders_update_machines_to_folder_associations: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateMachinesToFolderAssociationsRequest**](UpdateMachinesToFolderAssociationsRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

