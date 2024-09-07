# uipath_orchestrator_rest.RolesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**roles_delete_by_id**](RolesApi.md#roles_delete_by_id) | **DELETE** /odata/Roles({key}) | Deletes a role.
[**roles_get**](RolesApi.md#roles_get) | **GET** /odata/Roles | Gets roles.
[**roles_get_by_id**](RolesApi.md#roles_get_by_id) | **GET** /odata/Roles({key}) | Gets role based on its id.
[**roles_get_user_ids_for_role_by_key**](RolesApi.md#roles_get_user_ids_for_role_by_key) | **GET** /odata/Roles/UiPath.Server.Configuration.OData.GetUserIdsForRole(key&#x3D;{key}) | Returns a collection of all the ids of the users associated to a role based on role Id.
[**roles_get_users_for_role_by_key**](RolesApi.md#roles_get_users_for_role_by_key) | **GET** /odata/Roles/UiPath.Server.Configuration.OData.GetUsersForRole(key&#x3D;{key}) | Returns a collection of all users and, if no other sorting is provided, will place first those associated to a role.Allows odata query options.
[**roles_post**](RolesApi.md#roles_post) | **POST** /odata/Roles | Creates a new role - Creating mixed roles will not be supported in 21.10
[**roles_put_by_id**](RolesApi.md#roles_put_by_id) | **PUT** /odata/Roles({key}) | Edits a role.
[**roles_set_users_by_id**](RolesApi.md#roles_set_users_by_id) | **POST** /odata/Roles({key})/UiPath.Server.Configuration.OData.SetUsers | Associates a group of users with and dissociates another group of users from the given role.


# **roles_delete_by_id**
> roles_delete_by_id(key)

Deletes a role.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Roles.Delete.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | 

try:
    # Deletes a role.
    api_instance.roles_delete_by_id(key)
except ApiException as e:
    print("Exception when calling RolesApi->roles_delete_by_id: %s\n" % e)
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

# **roles_get**
> ODataValueOfIEnumerableOfRoleDto roles_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets roles.

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: Roles.View or Units.Edit or SubFolders.Edit.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets roles.
    api_response = api_instance.roles_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RolesApi->roles_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfRoleDto**](ODataValueOfIEnumerableOfRoleDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **roles_get_by_id**
> RoleDto roles_get_by_id(key, expand=expand, select=select)

Gets role based on its id.

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: Roles.View.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets role based on its id.
    api_response = api_instance.roles_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RolesApi->roles_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**RoleDto**](RoleDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **roles_get_user_ids_for_role_by_key**
> ODataValueOfIEnumerableOfInt64 roles_get_user_ids_for_role_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Returns a collection of all the ids of the users associated to a role based on role Id.

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: Roles.View or Users.View.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | The Id of the role for which the robot ids are fetched.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns a collection of all the ids of the users associated to a role based on role Id.
    api_response = api_instance.roles_get_user_ids_for_role_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RolesApi->roles_get_user_ids_for_role_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Id of the role for which the robot ids are fetched. | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfInt64**](ODataValueOfIEnumerableOfInt64.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **roles_get_users_for_role_by_key**
> ODataValueOfIEnumerableOfUserDto roles_get_users_for_role_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Returns a collection of all users and, if no other sorting is provided, will place first those associated to a role.Allows odata query options.

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: Roles.View and Users.View.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | The Id of the role for which the associated users are placed first.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns a collection of all users and, if no other sorting is provided, will place first those associated to a role.Allows odata query options.
    api_response = api_instance.roles_get_users_for_role_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RolesApi->roles_get_users_for_role_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Id of the role for which the associated users are placed first. | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfUserDto**](ODataValueOfIEnumerableOfUserDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **roles_post**
> RoleDto roles_post(body=body)

Creates a new role - Creating mixed roles will not be supported in 21.10

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Roles.Create.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.RoleDto() # RoleDto |  (optional)

try:
    # Creates a new role - Creating mixed roles will not be supported in 21.10
    api_response = api_instance.roles_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RolesApi->roles_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RoleDto**](RoleDto.md)|  | [optional] 

### Return type

[**RoleDto**](RoleDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **roles_put_by_id**
> roles_put_by_id(key, body=body)

Edits a role.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Roles.Edit.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | 
body = uipath_orchestrator_rest.RoleDto() # RoleDto |  (optional)

try:
    # Edits a role.
    api_instance.roles_put_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling RolesApi->roles_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**RoleDto**](RoleDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **roles_set_users_by_id**
> roles_set_users_by_id(key, body=body)

Associates a group of users with and dissociates another group of users from the given role.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Roles.Edit and Users.View.

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
api_instance = uipath_orchestrator_rest.RolesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | The role id.
body = uipath_orchestrator_rest.SetUsersRequest() # SetUsersRequest | <para />addedUserIds - The id of the users to be associated with the role.              <para />removedUserIds - The id of the users to be dissociated from the role. (optional)

try:
    # Associates a group of users with and dissociates another group of users from the given role.
    api_instance.roles_set_users_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling RolesApi->roles_set_users_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The role id. | 
 **body** | [**SetUsersRequest**](SetUsersRequest.md)| &lt;para /&gt;addedUserIds - The id of the users to be associated with the role.              &lt;para /&gt;removedUserIds - The id of the users to be dissociated from the role. | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

