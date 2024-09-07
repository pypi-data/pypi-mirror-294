# uipath_orchestrator_rest.ProcessesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**processes_delete_by_id**](ProcessesApi.md#processes_delete_by_id) | **DELETE** /odata/Processes({key}) | Deletes a package.
[**processes_download_package_by_key**](ProcessesApi.md#processes_download_package_by_key) | **GET** /odata/Processes/UiPath.Server.Configuration.OData.DownloadPackage(key&#x3D;{key}) | Downloads the .nupkg file of a Package.
[**processes_get**](ProcessesApi.md#processes_get) | **GET** /odata/Processes | Gets the processes.
[**processes_get_arguments_by_key**](ProcessesApi.md#processes_get_arguments_by_key) | **GET** /odata/Processes/UiPath.Server.Configuration.OData.GetArguments(key&#x3D;{key}) | Get process parameters
[**processes_get_process_versions_by_processid**](ProcessesApi.md#processes_get_process_versions_by_processid) | **GET** /odata/Processes/UiPath.Server.Configuration.OData.GetProcessVersions(processId&#x3D;{processId}) | Returns a collection of all available versions of a given process. Allows odata query options.
[**processes_set_arguments**](ProcessesApi.md#processes_set_arguments) | **POST** /odata/Processes/UiPath.Server.Configuration.OData.SetArguments | Saves process arguments
[**processes_upload_package**](ProcessesApi.md#processes_upload_package) | **POST** /odata/Processes/UiPath.Server.Configuration.OData.UploadPackage | Uploads a new package or a new version of an existing package. The content of the package is sent as a .nupkg file embedded in the HTTP request.


# **processes_delete_by_id**
> processes_delete_by_id(key, feed_id=feed_id)

Deletes a package.

OAuth required scopes: OR.Execution or OR.Execution.Write.  Required permissions: (Packages.Delete - Deletes a package in a Tenant Feed) and (FolderPackages.Delete - Deletes a package in a Folder Feed).

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
api_instance = uipath_orchestrator_rest.ProcessesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
feed_id = 'feed_id_example' # str |  (optional)

try:
    # Deletes a package.
    api_instance.processes_delete_by_id(key, feed_id=feed_id)
except ApiException as e:
    print("Exception when calling ProcessesApi->processes_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **feed_id** | [**str**](.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **processes_download_package_by_key**
> file processes_download_package_by_key(key, feed_id=feed_id)

Downloads the .nupkg file of a Package.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: (Packages.View - Downloads a package from a Tenant Feed) and (FolderPackages.View - Downloads a package from a Folder Feed).

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
api_instance = uipath_orchestrator_rest.ProcessesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
feed_id = 'feed_id_example' # str |  (optional)

try:
    # Downloads the .nupkg file of a Package.
    api_response = api_instance.processes_download_package_by_key(key, feed_id=feed_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessesApi->processes_download_package_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **feed_id** | [**str**](.md)|  | [optional] 

### Return type

[**file**](file.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **processes_get**
> ODataValueOfIEnumerableOfProcessDto processes_get(search_term=search_term, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets the processes.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: (Packages.View - Lists packages in a Tenant Feed) and (FolderPackages.View - Lists packages in a Folder Feed).

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
api_instance = uipath_orchestrator_rest.ProcessesApi(uipath_orchestrator_rest.ApiClient(configuration))
search_term = '' # str |  (optional) (default to )
feed_id = 'feed_id_example' # str |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets the processes.
    api_response = api_instance.processes_get(search_term=search_term, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessesApi->processes_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_term** | **str**|  | [optional] [default to ]
 **feed_id** | [**str**](.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfProcessDto**](ODataValueOfIEnumerableOfProcessDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **processes_get_arguments_by_key**
> ArgumentMetadata processes_get_arguments_by_key(key, expand=expand, select=select)

Get process parameters

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: Packages.View.

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
api_instance = uipath_orchestrator_rest.ProcessesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Get process parameters
    api_response = api_instance.processes_get_arguments_by_key(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessesApi->processes_get_arguments_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ArgumentMetadata**](ArgumentMetadata.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **processes_get_process_versions_by_processid**
> ODataValueOfIEnumerableOfProcessDto processes_get_process_versions_by_processid(process_id, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Returns a collection of all available versions of a given process. Allows odata query options.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: (Packages.View - Lists versions of a package in a Tenant Feed) and (FolderPackages.View - Lists versions of a package in a Folder Feed).

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
api_instance = uipath_orchestrator_rest.ProcessesApi(uipath_orchestrator_rest.ApiClient(configuration))
process_id = 'process_id_example' # str | The Id of the process for which the versions are fetched.
feed_id = 'feed_id_example' # str |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns a collection of all available versions of a given process. Allows odata query options.
    api_response = api_instance.processes_get_process_versions_by_processid(process_id, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessesApi->processes_get_process_versions_by_processid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **process_id** | **str**| The Id of the process for which the versions are fetched. | 
 **feed_id** | [**str**](.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfProcessDto**](ODataValueOfIEnumerableOfProcessDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **processes_set_arguments**
> processes_set_arguments(body=body)

Saves process arguments

OAuth required scopes: OR.Execution or OR.Execution.Write.  Required permissions: Packages.Edit.

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
api_instance = uipath_orchestrator_rest.ProcessesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.ProcessesSetArgumentsRequest() # ProcessesSetArgumentsRequest |  (optional)

try:
    # Saves process arguments
    api_instance.processes_set_arguments(body=body)
except ApiException as e:
    print("Exception when calling ProcessesApi->processes_set_arguments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProcessesSetArgumentsRequest**](ProcessesSetArgumentsRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **processes_upload_package**
> ODataValueOfIEnumerableOfBulkItemDtoOfString processes_upload_package(file, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count, file1=file1, file2=file2, file3=file3, file4=file4, file5=file5, file6=file6, file7=file7, file8=file8, file9=file9)

Uploads a new package or a new version of an existing package. The content of the package is sent as a .nupkg file embedded in the HTTP request.

OAuth required scopes: OR.Execution or OR.Execution.Write.  Required permissions: (Packages.Create - Uploads a package in a Tenant Feed) and (FolderPackages.Create - Uploads a package in a Folder Feed).

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
api_instance = uipath_orchestrator_rest.ProcessesApi(uipath_orchestrator_rest.ApiClient(configuration))
file = '/path/to/file.txt' # file | 
feed_id = 'feed_id_example' # str |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
file1 = '/path/to/file.txt' # file |  (optional)
file2 = '/path/to/file.txt' # file |  (optional)
file3 = '/path/to/file.txt' # file |  (optional)
file4 = '/path/to/file.txt' # file |  (optional)
file5 = '/path/to/file.txt' # file |  (optional)
file6 = '/path/to/file.txt' # file |  (optional)
file7 = '/path/to/file.txt' # file |  (optional)
file8 = '/path/to/file.txt' # file |  (optional)
file9 = '/path/to/file.txt' # file |  (optional)

try:
    # Uploads a new package or a new version of an existing package. The content of the package is sent as a .nupkg file embedded in the HTTP request.
    api_response = api_instance.processes_upload_package(file, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count, file1=file1, file2=file2, file3=file3, file4=file4, file5=file5, file6=file6, file7=file7, file8=file8, file9=file9)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessesApi->processes_upload_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 
 **feed_id** | [**str**](.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **file1** | **file**|  | [optional] 
 **file2** | **file**|  | [optional] 
 **file3** | **file**|  | [optional] 
 **file4** | **file**|  | [optional] 
 **file5** | **file**|  | [optional] 
 **file6** | **file**|  | [optional] 
 **file7** | **file**|  | [optional] 
 **file8** | **file**|  | [optional] 
 **file9** | **file**|  | [optional] 

### Return type

[**ODataValueOfIEnumerableOfBulkItemDtoOfString**](ODataValueOfIEnumerableOfBulkItemDtoOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

