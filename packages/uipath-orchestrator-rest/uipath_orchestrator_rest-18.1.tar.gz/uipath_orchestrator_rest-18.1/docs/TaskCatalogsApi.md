# uipath_orchestrator_rest.TaskCatalogsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**task_catalogs_create_task_catalog**](TaskCatalogsApi.md#task_catalogs_create_task_catalog) | **POST** /odata/TaskCatalogs/UiPath.Server.Configuration.OData.CreateTaskCatalog | Creates a new Task Catalog.
[**task_catalogs_delete_by_id**](TaskCatalogsApi.md#task_catalogs_delete_by_id) | **DELETE** /odata/TaskCatalogs({key}) | Deletes Task Catalog.
[**task_catalogs_get**](TaskCatalogsApi.md#task_catalogs_get) | **GET** /odata/TaskCatalogs | Gets Task Catalog objects with the given OData queries.
[**task_catalogs_get_by_id**](TaskCatalogsApi.md#task_catalogs_get_by_id) | **GET** /odata/TaskCatalogs({key}) | Gets a Task Catalog item by Id.
[**task_catalogs_get_folders_for_task_catalog_by_id**](TaskCatalogsApi.md#task_catalogs_get_folders_for_task_catalog_by_id) | **GET** /odata/TaskCatalogs/UiPath.Server.Configuration.OData.GetFoldersForTaskCatalog(id&#x3D;{id}) | Get all accessible folders where the task catalog is shared, and the total count of folders where it is shared (including unaccessible folders).
[**task_catalogs_get_task_catalog_extended_details_by_taskcatalogid**](TaskCatalogsApi.md#task_catalogs_get_task_catalog_extended_details_by_taskcatalogid) | **GET** /odata/TaskCatalogs/UiPath.Server.Configuration.OData.GetTaskCatalogExtendedDetails(taskCatalogId&#x3D;{taskCatalogId}) | Validates task catalog deletion request.
[**task_catalogs_get_task_catalogs_from_folders_with_permissions**](TaskCatalogsApi.md#task_catalogs_get_task_catalogs_from_folders_with_permissions) | **GET** /odata/TaskCatalogs/UiPath.Server.Configuration.OData.GetTaskCatalogsFromFoldersWithPermissions | Gets Task Catalogs across folders having given permission with the given OData queries .
[**task_catalogs_share_to_folders**](TaskCatalogsApi.md#task_catalogs_share_to_folders) | **POST** /odata/TaskCatalogs/UiPath.Server.Configuration.OData.ShareToFolders | Makes the task catalogs visible in the specified folders.
[**task_catalogs_update_task_catalog_by_id**](TaskCatalogsApi.md#task_catalogs_update_task_catalog_by_id) | **POST** /odata/TaskCatalogs({key})/UiPath.Server.Configuration.OData.UpdateTaskCatalog | Updates Task Catalog.


# **task_catalogs_create_task_catalog**
> TaskCatalogDto task_catalogs_create_task_catalog(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates a new Task Catalog.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: TaskCatalogs.Create.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskCatalogRequest() # TaskCatalogRequest | The task catalog to be created. (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates a new Task Catalog.
    api_response = api_instance.task_catalogs_create_task_catalog(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_create_task_catalog: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskCatalogRequest**](TaskCatalogRequest.md)| The task catalog to be created. | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TaskCatalogDto**](TaskCatalogDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_delete_by_id**
> task_catalogs_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Deletes Task Catalog.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: TaskCatalogs.Delete.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Id of the catalog to be deleted
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Deletes Task Catalog.
    api_instance.task_catalogs_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Id of the catalog to be deleted | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_get**
> ODataValueOfIEnumerableOfTaskCatalogDto task_catalogs_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets Task Catalog objects with the given OData queries.

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Required permissions: TaskCatalogs.View.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets Task Catalog objects with the given OData queries.
    api_response = api_instance.task_catalogs_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_get: %s\n" % e)
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
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfTaskCatalogDto**](ODataValueOfIEnumerableOfTaskCatalogDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_get_by_id**
> TaskCatalogDto task_catalogs_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a Task Catalog item by Id.

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Required permissions: TaskCatalogs.View.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | id of the object
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a Task Catalog item by Id.
    api_response = api_instance.task_catalogs_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| id of the object | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TaskCatalogDto**](TaskCatalogDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_get_folders_for_task_catalog_by_id**
> AccessibleFoldersDto task_catalogs_get_folders_for_task_catalog_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get all accessible folders where the task catalog is shared, and the total count of folders where it is shared (including unaccessible folders).

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
id = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get all accessible folders where the task catalog is shared, and the total count of folders where it is shared (including unaccessible folders).
    api_response = api_instance.task_catalogs_get_folders_for_task_catalog_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_get_folders_for_task_catalog_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**AccessibleFoldersDto**](AccessibleFoldersDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_get_task_catalog_extended_details_by_taskcatalogid**
> TaskCatalogExtendedDetailsDto task_catalogs_get_task_catalog_extended_details_by_taskcatalogid(task_catalog_id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Validates task catalog deletion request.

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
task_catalog_id = 789 # int | Id of task catalog
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Validates task catalog deletion request.
    api_response = api_instance.task_catalogs_get_task_catalog_extended_details_by_taskcatalogid(task_catalog_id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_get_task_catalog_extended_details_by_taskcatalogid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_catalog_id** | **int**| Id of task catalog | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**TaskCatalogExtendedDetailsDto**](TaskCatalogExtendedDetailsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_get_task_catalogs_from_folders_with_permissions**
> ODataValueOfIEnumerableOfTaskCatalogDto task_catalogs_get_task_catalogs_from_folders_with_permissions(mandatory_permissions=mandatory_permissions, exclude_folder_id=exclude_folder_id, distinct_by_select=distinct_by_select, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets Task Catalogs across folders having given permission with the given OData queries .

OAuth required scopes: OR.Tasks or OR.Tasks.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
mandatory_permissions = ['mandatory_permissions_example'] # list[str] | These represent the additional permissions over TaskCatalog.Read required in the folders the data is retrieved from; all permissions in this set must be met (optional)
exclude_folder_id = 789 # int | The task catalogs beloging to this folder will be excluded. (optional)
distinct_by_select = true # bool | Return distinct attributes from task catalog for select query. Select param must have exactly 1 value if this is enabled (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets Task Catalogs across folders having given permission with the given OData queries .
    api_response = api_instance.task_catalogs_get_task_catalogs_from_folders_with_permissions(mandatory_permissions=mandatory_permissions, exclude_folder_id=exclude_folder_id, distinct_by_select=distinct_by_select, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_get_task_catalogs_from_folders_with_permissions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mandatory_permissions** | [**list[str]**](str.md)| These represent the additional permissions over TaskCatalog.Read required in the folders the data is retrieved from; all permissions in this set must be met | [optional] 
 **exclude_folder_id** | **int**| The task catalogs beloging to this folder will be excluded. | [optional] 
 **distinct_by_select** | **bool**| Return distinct attributes from task catalog for select query. Select param must have exactly 1 value if this is enabled | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfTaskCatalogDto**](ODataValueOfIEnumerableOfTaskCatalogDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_share_to_folders**
> task_catalogs_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Makes the task catalogs visible in the specified folders.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TaskCatalogFoldersShareDto() # TaskCatalogFoldersShareDto | Object containing the ids of the task catalogs and the ids of the folders where it should be shared. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Makes the task catalogs visible in the specified folders.
    api_instance.task_catalogs_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_share_to_folders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskCatalogFoldersShareDto**](TaskCatalogFoldersShareDto.md)| Object containing the ids of the task catalogs and the ids of the folders where it should be shared. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_catalogs_update_task_catalog_by_id**
> task_catalogs_update_task_catalog_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Updates Task Catalog.

OAuth required scopes: OR.Tasks or OR.Tasks.Write.  Required permissions: TaskCatalogs.Edit.

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
api_instance = uipath_orchestrator_rest.TaskCatalogsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Key of the object
body = uipath_orchestrator_rest.TaskCatalogRequest() # TaskCatalogRequest | TaskCatalog to be updated (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Updates Task Catalog.
    api_instance.task_catalogs_update_task_catalog_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TaskCatalogsApi->task_catalogs_update_task_catalog_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Key of the object | 
 **body** | [**TaskCatalogRequest**](TaskCatalogRequest.md)| TaskCatalog to be updated | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

