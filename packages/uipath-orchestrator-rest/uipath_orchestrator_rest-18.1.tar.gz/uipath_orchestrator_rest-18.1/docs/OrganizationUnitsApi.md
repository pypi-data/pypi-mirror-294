# uipath_orchestrator_rest.OrganizationUnitsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**organization_units_delete_by_id**](OrganizationUnitsApi.md#organization_units_delete_by_id) | **DELETE** /odata/OrganizationUnits({key}) | Deletes an organization unit.
[**organization_units_get**](OrganizationUnitsApi.md#organization_units_get) | **GET** /odata/OrganizationUnits | Gets the organization units.
[**organization_units_get_by_id**](OrganizationUnitsApi.md#organization_units_get_by_id) | **GET** /odata/OrganizationUnits({key}) | Gets an organization unit.
[**organization_units_get_user_ids_for_unit_by_key**](OrganizationUnitsApi.md#organization_units_get_user_ids_for_unit_by_key) | **GET** /odata/OrganizationUnits/UiPath.Server.Configuration.OData.GetUserIdsForUnit(key&#x3D;{key}) | Returns a collection of all the ids of the users associated to an unit based on unit Id.
[**organization_units_get_users_for_unit_by_key**](OrganizationUnitsApi.md#organization_units_get_users_for_unit_by_key) | **GET** /odata/OrganizationUnits/UiPath.Server.Configuration.OData.GetUsersForUnit(key&#x3D;{key}) | Returns a collection of all non robot users and, if no other sorting is provided, will place first those associated to an unit. Allows odata query options.
[**organization_units_post**](OrganizationUnitsApi.md#organization_units_post) | **POST** /odata/OrganizationUnits | Creates an organization unit.
[**organization_units_put_by_id**](OrganizationUnitsApi.md#organization_units_put_by_id) | **PUT** /odata/OrganizationUnits({key}) | Edits an organization unit.
[**organization_units_set_users_by_id**](OrganizationUnitsApi.md#organization_units_set_users_by_id) | **POST** /odata/OrganizationUnits({key})/UiPath.Server.Configuration.OData.SetUsers | Associates a group of users with and dissociates another group of users from the given unit.


# **organization_units_delete_by_id**
> organization_units_delete_by_id(key)

Deletes an organization unit.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: Units.Delete. DEPRECATED:  Kept for backwards compatibility. Use Delete from FoldersController  instead Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Deletes an organization unit.
    api_instance.organization_units_delete_by_id(key)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_delete_by_id: %s\n" % e)
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

# **organization_units_get**
> ODataValueOfIEnumerableOfOrganizationUnitDto organization_units_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets the organization units.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: Units.View. DEPRECATED:  Kept for backwards compatibility. Use Get from FoldersController  instead Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets the organization units.
    api_response = api_instance.organization_units_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfOrganizationUnitDto**](ODataValueOfIEnumerableOfOrganizationUnitDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organization_units_get_by_id**
> OrganizationUnitDto organization_units_get_by_id(key, expand=expand, select=select)

Gets an organization unit.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: Units.View. DEPRECATED:  Kept for backwards compatibility. Use Get from FoldersController  instead Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets an organization unit.
    api_response = api_instance.organization_units_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**OrganizationUnitDto**](OrganizationUnitDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organization_units_get_user_ids_for_unit_by_key**
> ODataValueOfIEnumerableOfInt64 organization_units_get_user_ids_for_unit_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Returns a collection of all the ids of the users associated to an unit based on unit Id.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: Units.View and Users.View. DEPRECATED:  Kept for backwards compatibility. Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Id of the unit for which the robot ids are fetched.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns a collection of all the ids of the users associated to an unit based on unit Id.
    api_response = api_instance.organization_units_get_user_ids_for_unit_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_get_user_ids_for_unit_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Id of the unit for which the robot ids are fetched. | 
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

# **organization_units_get_users_for_unit_by_key**
> ODataValueOfIEnumerableOfUserDto organization_units_get_users_for_unit_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Returns a collection of all non robot users and, if no other sorting is provided, will place first those associated to an unit. Allows odata query options.

OAuth required scopes: OR.Folders or OR.Folders.Read.  Required permissions: Units.View and Users.View. DEPRECATED:  Kept for backwards compatibility. Use GetUsersForFolder from FoldersController  instead Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Id of the unit for which the associated users are placed first.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns a collection of all non robot users and, if no other sorting is provided, will place first those associated to an unit. Allows odata query options.
    api_response = api_instance.organization_units_get_users_for_unit_by_key(key, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_get_users_for_unit_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Id of the unit for which the associated users are placed first. | 
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

# **organization_units_post**
> OrganizationUnitDto organization_units_post(body=body)

Creates an organization unit.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: Units.Create. DEPRECATED:  Kept for backwards compatibility. Use Post from FoldersController  instead Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.OrganizationUnitDto() # OrganizationUnitDto |  (optional)

try:
    # Creates an organization unit.
    api_response = api_instance.organization_units_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrganizationUnitDto**](OrganizationUnitDto.md)|  | [optional] 

### Return type

[**OrganizationUnitDto**](OrganizationUnitDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organization_units_put_by_id**
> OrganizationUnitDto organization_units_put_by_id(key, body=body)

Edits an organization unit.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: Units.Edit. DEPRECATED:  Kept for backwards compatibility. Use Put from FoldersController  instead Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | 
body = uipath_orchestrator_rest.OrganizationUnitDto() # OrganizationUnitDto |  (optional)

try:
    # Edits an organization unit.
    api_response = api_instance.organization_units_put_by_id(key, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**OrganizationUnitDto**](OrganizationUnitDto.md)|  | [optional] 

### Return type

[**OrganizationUnitDto**](OrganizationUnitDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organization_units_set_users_by_id**
> organization_units_set_users_by_id(key, body=body)

Associates a group of users with and dissociates another group of users from the given unit.

OAuth required scopes: OR.Folders or OR.Folders.Write.  Required permissions: Users.Edit. DEPRECATED:  Kept for backwards compatibility. Use AssignUsers from FoldersController  instead Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.OrganizationUnitsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | The unit id.
body = uipath_orchestrator_rest.SetUsersRequest() # SetUsersRequest | <para />addedUserIds - The id of the users to be associated with the unit.              <para />removedUserIds - The id of the users to be dissociated from the unit. (optional)

try:
    # Associates a group of users with and dissociates another group of users from the given unit.
    api_instance.organization_units_set_users_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling OrganizationUnitsApi->organization_units_set_users_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The unit id. | 
 **body** | [**SetUsersRequest**](SetUsersRequest.md)| &lt;para /&gt;addedUserIds - The id of the users to be associated with the unit.              &lt;para /&gt;removedUserIds - The id of the users to be dissociated from the unit. | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

