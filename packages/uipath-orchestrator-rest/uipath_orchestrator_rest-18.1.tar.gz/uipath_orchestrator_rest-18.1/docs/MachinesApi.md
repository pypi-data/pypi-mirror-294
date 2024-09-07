# uipath_orchestrator_rest.MachinesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**machines_delete_bulk**](MachinesApi.md#machines_delete_bulk) | **POST** /odata/Machines/UiPath.Server.Configuration.OData.DeleteBulk | Deletes multiple machines based on their keys.
[**machines_delete_by_id**](MachinesApi.md#machines_delete_by_id) | **DELETE** /odata/Machines({key}) | Deletes a machine based on its key.
[**machines_get**](MachinesApi.md#machines_get) | **GET** /odata/Machines | Gets machines.
[**machines_get_assigned_machines_by_folderid**](MachinesApi.md#machines_get_assigned_machines_by_folderid) | **GET** /odata/Machines/UiPath.Server.Configuration.OData.GetAssignedMachines(folderId&#x3D;{folderId}) | Gets machines assigned to folder and robot
[**machines_get_by_id**](MachinesApi.md#machines_get_by_id) | **GET** /odata/Machines({key}) | Gets a single machine based on its id.
[**machines_get_runtimes_for_folder_by_folderid**](MachinesApi.md#machines_get_runtimes_for_folder_by_folderid) | **GET** /odata/Machines/UiPath.Server.Configuration.OData.GetRuntimesForFolder(folderId&#x3D;{folderId}) | Gets runtimes for the specified folder
[**machines_patch_by_id**](MachinesApi.md#machines_patch_by_id) | **PATCH** /odata/Machines({key}) | Partially updates a machine.
[**machines_post**](MachinesApi.md#machines_post) | **POST** /odata/Machines | Creates a new machine.
[**machines_put_by_id**](MachinesApi.md#machines_put_by_id) | **PUT** /odata/Machines({key}) | Edits a machine based on its key.


# **machines_delete_bulk**
> machines_delete_bulk(body=body)

Deletes multiple machines based on their keys.

OAuth required scopes: OR.Machines or OR.Machines.Write.  Required permissions: Machines.Delete.

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.MachineDeleteBulkRequest() # MachineDeleteBulkRequest |  (optional)

try:
    # Deletes multiple machines based on their keys.
    api_instance.machines_delete_bulk(body=body)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_delete_bulk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MachineDeleteBulkRequest**](MachineDeleteBulkRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **machines_delete_by_id**
> machines_delete_by_id(key)

Deletes a machine based on its key.

OAuth required scopes: OR.Machines or OR.Machines.Write.  Required permissions: Machines.Delete.

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Deletes a machine based on its key.
    api_instance.machines_delete_by_id(key)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_delete_by_id: %s\n" % e)
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

# **machines_get**
> ODataValueOfIEnumerableOfExtendedMachineDto machines_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets machines.

OAuth required scopes: OR.Machines or OR.Machines.Read.  Required permissions: Machines.View.

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets machines.
    api_response = api_instance.machines_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfExtendedMachineDto**](ODataValueOfIEnumerableOfExtendedMachineDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **machines_get_assigned_machines_by_folderid**
> ODataValueOfIEnumerableOfMachineDto machines_get_assigned_machines_by_folderid(folder_id, robot_id=robot_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets machines assigned to folder and robot

OAuth required scopes: OR.Machines or OR.Machines.Read.  Required permissions: (Machines.View or Jobs.Create).

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
folder_id = 789 # int | 
robot_id = 789 # int |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets machines assigned to folder and robot
    api_response = api_instance.machines_get_assigned_machines_by_folderid(folder_id, robot_id=robot_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_get_assigned_machines_by_folderid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **folder_id** | **int**|  | 
 **robot_id** | **int**|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfMachineDto**](ODataValueOfIEnumerableOfMachineDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **machines_get_by_id**
> MachineDto machines_get_by_id(key, expand=expand, select=select)

Gets a single machine based on its id.

OAuth required scopes: OR.Machines or OR.Machines.Read.  Required permissions: Machines.View.

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a single machine based on its id.
    api_response = api_instance.machines_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**MachineDto**](MachineDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **machines_get_runtimes_for_folder_by_folderid**
> ODataValueOfIEnumerableOfMachineRuntimeDto machines_get_runtimes_for_folder_by_folderid(folder_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Gets runtimes for the specified folder

OAuth required scopes: OR.Machines or OR.Machines.Read.  Required permissions: (Machines.View or Jobs.Create).

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
folder_id = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets runtimes for the specified folder
    api_response = api_instance.machines_get_runtimes_for_folder_by_folderid(folder_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_get_runtimes_for_folder_by_folderid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **folder_id** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfMachineRuntimeDto**](ODataValueOfIEnumerableOfMachineRuntimeDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **machines_patch_by_id**
> machines_patch_by_id(key, body=body)

Partially updates a machine.

OAuth required scopes: OR.Machines or OR.Machines.Write.  Required permissions: Machines.Edit.

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.MachineDto() # MachineDto |  (optional)

try:
    # Partially updates a machine.
    api_instance.machines_patch_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_patch_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**MachineDto**](MachineDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **machines_post**
> MachineDto machines_post(body=body)

Creates a new machine.

OAuth required scopes: OR.Machines or OR.Machines.Write.  Required permissions: Machines.Create.

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.MachineDto() # MachineDto |  (optional)

try:
    # Creates a new machine.
    api_response = api_instance.machines_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MachineDto**](MachineDto.md)|  | [optional] 

### Return type

[**MachineDto**](MachineDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **machines_put_by_id**
> MachineDto machines_put_by_id(key, body=body)

Edits a machine based on its key.

OAuth required scopes: OR.Machines or OR.Machines.Write.  Required permissions: Machines.Edit.

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
api_instance = uipath_orchestrator_rest.MachinesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.MachineDto() # MachineDto |  (optional)

try:
    # Edits a machine based on its key.
    api_response = api_instance.machines_put_by_id(key, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachinesApi->machines_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**MachineDto**](MachineDto.md)|  | [optional] 

### Return type

[**MachineDto**](MachineDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

