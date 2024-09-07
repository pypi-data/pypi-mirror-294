# uipath_orchestrator_rest.UsersApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**users_assign_roles_by_id**](UsersApi.md#users_assign_roles_by_id) | **POST** /odata/Users({key})/UiPath.Server.Configuration.OData.AssignRoles | 
[**users_change_culture**](UsersApi.md#users_change_culture) | **POST** /odata/Users/UiPath.Server.Configuration.OData.ChangeCulture | Changes the culture for the current user
[**users_change_user_culture_by_id**](UsersApi.md#users_change_user_culture_by_id) | **POST** /odata/Users({key})/UiPath.Server.Configuration.OData.ChangeUserCulture | Changes the culture for the specified user
[**users_delete_by_id**](UsersApi.md#users_delete_by_id) | **DELETE** /odata/Users({key}) | Deletes a user.
[**users_get**](UsersApi.md#users_get) | **GET** /odata/Users | Gets users.
[**users_get_by_id**](UsersApi.md#users_get_by_id) | **GET** /odata/Users({key}) | Gets a user based on its id.
[**users_get_current_permissions**](UsersApi.md#users_get_current_permissions) | **GET** /odata/Users/UiPath.Server.Configuration.OData.GetCurrentPermissions | Returns a user permission collection containing data about the current user and all the permissions it has.
[**users_get_current_user**](UsersApi.md#users_get_current_user) | **GET** /odata/Users/UiPath.Server.Configuration.OData.GetCurrentUser | Returns details about the user currently logged into Orchestrator.
[**users_patch_by_id**](UsersApi.md#users_patch_by_id) | **PATCH** /odata/Users({key}) | Partially updates a user.  Cannot update roles or organization units via this endpoint.
[**users_post**](UsersApi.md#users_post) | **POST** /odata/Users | Creates a new user.
[**users_put_by_id**](UsersApi.md#users_put_by_id) | **PUT** /odata/Users({key}) | Edits a user.
[**users_set_active_by_id**](UsersApi.md#users_set_active_by_id) | **POST** /odata/Users({key})/UiPath.Server.Configuration.OData.SetActive | Activate or deactivate a user
[**users_toggle_organization_unit_by_id**](UsersApi.md#users_toggle_organization_unit_by_id) | **POST** /odata/Users({key})/UiPath.Server.Configuration.OData.ToggleOrganizationUnit | Associates/dissociates the given user with/from an organization unit based on toggle parameter.
[**users_toggle_role_by_id**](UsersApi.md#users_toggle_role_by_id) | **POST** /odata/Users({key})/UiPath.Server.Configuration.OData.ToggleRole | Associates/dissociates the given user with/from a role based on toggle parameter.
[**users_validate_by_userids**](UsersApi.md#users_validate_by_userids) | **GET** /odata/Users/UiPath.Server.Configuration.OData.Validate(userIds&#x3D;[{userIds}]) | Validates if the robots for the given users are busy


# **users_assign_roles_by_id**
> users_assign_roles_by_id(key, body=body)



OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Edit or Users.Create.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.UserAssignRolesRequest() # UserAssignRolesRequest |  (optional)

try:
    api_instance.users_assign_roles_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_assign_roles_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**UserAssignRolesRequest**](UserAssignRolesRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_change_culture**
> users_change_culture(body=body)

Changes the culture for the current user

OAuth required scopes: OR.Users or OR.Users.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.UserChangeCultureRequest() # UserChangeCultureRequest |  (optional)

try:
    # Changes the culture for the current user
    api_instance.users_change_culture(body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_change_culture: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserChangeCultureRequest**](UserChangeCultureRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_change_user_culture_by_id**
> users_change_user_culture_by_id(key, body=body)

Changes the culture for the specified user

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Edit.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.UserChangeCultureRequest() # UserChangeCultureRequest |  (optional)

try:
    # Changes the culture for the specified user
    api_instance.users_change_user_culture_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_change_user_culture_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**UserChangeCultureRequest**](UserChangeCultureRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_delete_by_id**
> users_delete_by_id(key)

Deletes a user.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Delete.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Deletes a user.
    api_instance.users_delete_by_id(key)
except ApiException as e:
    print("Exception when calling UsersApi->users_delete_by_id: %s\n" % e)
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

# **users_get**
> ODataValueOfIEnumerableOfUserDto users_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets users.

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: Users.View.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets users.
    api_response = api_instance.users_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfUserDto**](ODataValueOfIEnumerableOfUserDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_get_by_id**
> UserDto users_get_by_id(key, expand=expand, select=select)

Gets a user based on its id.

OAuth required scopes: OR.Users or OR.Users.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a user based on its id.
    api_response = api_instance.users_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**UserDto**](UserDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_get_current_permissions**
> UserPermissionsCollection users_get_current_permissions(expand=expand, select=select)

Returns a user permission collection containing data about the current user and all the permissions it has.

OAuth required scopes: OR.Users or OR.Users.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Returns a user permission collection containing data about the current user and all the permissions it has.
    api_response = api_instance.users_get_current_permissions(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_get_current_permissions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**UserPermissionsCollection**](UserPermissionsCollection.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_get_current_user**
> UserDto users_get_current_user(expand=expand, select=select)

Returns details about the user currently logged into Orchestrator.

OAuth required scopes: OR.Users or OR.Users.Read.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Returns details about the user currently logged into Orchestrator.
    api_response = api_instance.users_get_current_user(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_get_current_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**UserDto**](UserDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_patch_by_id**
> users_patch_by_id(key, body=body)

Partially updates a user.  Cannot update roles or organization units via this endpoint.

OAuth required scopes: OR.Users or OR.Users.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.UserDto() # UserDto |  (optional)

try:
    # Partially updates a user.  Cannot update roles or organization units via this endpoint.
    api_instance.users_patch_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_patch_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**UserDto**](UserDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_post**
> UserDto users_post(body=body)

Creates a new user.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Create.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.UserDto() # UserDto |  (optional)

try:
    # Creates a new user.
    api_response = api_instance.users_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserDto**](UserDto.md)|  | [optional] 

### Return type

[**UserDto**](UserDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_put_by_id**
> users_put_by_id(key, body=body)

Edits a user.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Edit or Robots.Create or Robots.Edit or Robots.Delete.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.UserDto() # UserDto |  (optional)

try:
    # Edits a user.
    api_instance.users_put_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**UserDto**](UserDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_set_active_by_id**
> users_set_active_by_id(key, body=body)

Activate or deactivate a user

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Edit.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.UsersSetActiveRequest() # UsersSetActiveRequest |  (optional)

try:
    # Activate or deactivate a user
    api_instance.users_set_active_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_set_active_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**UsersSetActiveRequest**](UsersSetActiveRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_toggle_organization_unit_by_id**
> users_toggle_organization_unit_by_id(key, body=body)

Associates/dissociates the given user with/from an organization unit based on toggle parameter.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Edit.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.UsersToggleOrganizationUnitRequest() # UsersToggleOrganizationUnitRequest | <para />Toggle - States whether to associate or to dissociate the organization unit with/from the user.              <para />OrganizationUnitId - The id of the organization unit to be associated/dissociated. (optional)

try:
    # Associates/dissociates the given user with/from an organization unit based on toggle parameter.
    api_instance.users_toggle_organization_unit_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_toggle_organization_unit_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**UsersToggleOrganizationUnitRequest**](UsersToggleOrganizationUnitRequest.md)| &lt;para /&gt;Toggle - States whether to associate or to dissociate the organization unit with/from the user.              &lt;para /&gt;OrganizationUnitId - The id of the organization unit to be associated/dissociated. | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_toggle_role_by_id**
> users_toggle_role_by_id(key, body=body)

Associates/dissociates the given user with/from a role based on toggle parameter.

OAuth required scopes: OR.Users or OR.Users.Write.  Required permissions: Users.Edit.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.UsersToggleRoleRequest() # UsersToggleRoleRequest | <para />Toggle - States whether to associate or to dissociate the role with/from the user.              <para />Role - The name of the role to be associated/dissociated. (optional)

try:
    # Associates/dissociates the given user with/from a role based on toggle parameter.
    api_instance.users_toggle_role_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling UsersApi->users_toggle_role_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**UsersToggleRoleRequest**](UsersToggleRoleRequest.md)| &lt;para /&gt;Toggle - States whether to associate or to dissociate the role with/from the user.              &lt;para /&gt;Role - The name of the role to be associated/dissociated. | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_validate_by_userids**
> ODataValueOfIDictionaryOfInt64Boolean users_validate_by_userids(user_ids, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Validates if the robots for the given users are busy

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: Users.View.

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
api_instance = uipath_orchestrator_rest.UsersApi(uipath_orchestrator_rest.ApiClient(configuration))
user_ids = [56] # list[int] | The Id of the users to check
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Validates if the robots for the given users are busy
    api_response = api_instance.users_validate_by_userids(user_ids, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_validate_by_userids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_ids** | [**list[int]**](int.md)| The Id of the users to check | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIDictionaryOfInt64Boolean**](ODataValueOfIDictionaryOfInt64Boolean.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

