# uipath_orchestrator_rest.BucketsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**buckets_delete_by_id**](BucketsApi.md#buckets_delete_by_id) | **DELETE** /odata/Buckets({key}) | Delete a bucket
[**buckets_delete_file_by_key**](BucketsApi.md#buckets_delete_file_by_key) | **DELETE** /odata/Buckets({key})/UiPath.Server.Configuration.OData.DeleteFile | Deletes a file.
[**buckets_get**](BucketsApi.md#buckets_get) | **GET** /odata/Buckets | Gets Buckets.
[**buckets_get_buckets_across_folders**](BucketsApi.md#buckets_get_buckets_across_folders) | **GET** /odata/Buckets/UiPath.Server.Configuration.OData.GetBucketsAcrossFolders | Get the buckets from all the folders in which the current user has the Buckets.View permission, except the one specified.
[**buckets_get_by_id**](BucketsApi.md#buckets_get_by_id) | **GET** /odata/Buckets({key}) | Gets a single Bucket.
[**buckets_get_directories_by_key**](BucketsApi.md#buckets_get_directories_by_key) | **GET** /odata/Buckets({key})/UiPath.Server.Configuration.OData.GetDirectories | Gets the child directories in a directory.
[**buckets_get_file_by_key**](BucketsApi.md#buckets_get_file_by_key) | **GET** /odata/Buckets({key})/UiPath.Server.Configuration.OData.GetFile | Gets a file metadata.
[**buckets_get_files_by_key**](BucketsApi.md#buckets_get_files_by_key) | **GET** /odata/Buckets({key})/UiPath.Server.Configuration.OData.GetFiles | Gets the files in a directory.  Optionally returns all files in all child directories (recursive).
[**buckets_get_folders_for_bucket_by_id**](BucketsApi.md#buckets_get_folders_for_bucket_by_id) | **GET** /odata/Buckets/UiPath.Server.Configuration.OData.GetFoldersForBucket(id&#x3D;{id}) | Get all accessible folders where the bucket is shared, and the total count of folders where it is shared (including unaccessible folders).
[**buckets_get_read_uri_by_key**](BucketsApi.md#buckets_get_read_uri_by_key) | **GET** /odata/Buckets({key})/UiPath.Server.Configuration.OData.GetReadUri | Gets a direct download URL for BlobFile.
[**buckets_get_write_uri_by_key**](BucketsApi.md#buckets_get_write_uri_by_key) | **GET** /odata/Buckets({key})/UiPath.Server.Configuration.OData.GetWriteUri | Gets a direct upload URL for BlobFile.
[**buckets_post**](BucketsApi.md#buckets_post) | **POST** /odata/Buckets | Creates an Bucket
[**buckets_put_by_id**](BucketsApi.md#buckets_put_by_id) | **PUT** /odata/Buckets({key}) | Updates a bucket.
[**buckets_share_to_folders**](BucketsApi.md#buckets_share_to_folders) | **POST** /odata/Buckets/UiPath.Server.Configuration.OData.ShareToFolders | Adds the buckets to the folders specified in &#39;ToAddFolderIds&#39;. Removes the buckets from the folders specified in &#39;ToRemoveFolderIds&#39;.


# **buckets_delete_by_id**
> buckets_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Delete a bucket

OAuth required scopes: OR.Administration or OR.Administration.Write.  Required permissions: Buckets.Delete.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Delete a bucket
    api_instance.buckets_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_delete_file_by_key**
> buckets_delete_file_by_key(key, path=path, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Deletes a file.

OAuth required scopes: OR.Administration or OR.Administration.Write.  Required permissions: Buckets.View and BlobFiles.Delete.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Bucket Id
path = 'path_example' # str | The BlobFile full path (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Deletes a file.
    api_instance.buckets_delete_file_by_key(key, path=path, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_delete_file_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Bucket Id | 
 **path** | **str**| The BlobFile full path | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get**
> ODataValueOfIEnumerableOfBucketDto buckets_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets Buckets.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Required permissions: Buckets.View.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets Buckets.
    api_response = api_instance.buckets_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfBucketDto**](ODataValueOfIEnumerableOfBucketDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get_buckets_across_folders**
> ODataValueOfIEnumerableOfBucketDto buckets_get_buckets_across_folders(exclude_folder_id=exclude_folder_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get the buckets from all the folders in which the current user has the Buckets.View permission, except the one specified.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
exclude_folder_id = 789 # int |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get the buckets from all the folders in which the current user has the Buckets.View permission, except the one specified.
    api_response = api_instance.buckets_get_buckets_across_folders(exclude_folder_id=exclude_folder_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_buckets_across_folders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude_folder_id** | **int**|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfBucketDto**](ODataValueOfIEnumerableOfBucketDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get_by_id**
> BucketDto buckets_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a single Bucket.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Required permissions: Buckets.View.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a single Bucket.
    api_response = api_instance.buckets_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BucketDto**](BucketDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get_directories_by_key**
> ODataValueOfIEnumerableOfBlobFileDto buckets_get_directories_by_key(key, directory=directory, file_name_glob=file_name_glob, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets the child directories in a directory.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Required permissions: Buckets.View and BlobFiles.View.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Bucket Id
directory = 'directory_example' # str | The directory path (optional)
file_name_glob = 'file_name_glob_example' # str | Directory listing filter (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Number of directories to return (optional)
skip = 56 # int | Number of directories to skip (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets the child directories in a directory.
    api_response = api_instance.buckets_get_directories_by_key(key, directory=directory, file_name_glob=file_name_glob, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_directories_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Bucket Id | 
 **directory** | **str**| The directory path | [optional] 
 **file_name_glob** | **str**| Directory listing filter | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Number of directories to return | [optional] 
 **skip** | **int**| Number of directories to skip | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfBlobFileDto**](ODataValueOfIEnumerableOfBlobFileDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get_file_by_key**
> BlobFileDto buckets_get_file_by_key(key, path=path, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a file metadata.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Required permissions: Buckets.View and BlobFiles.View.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Bucket Id
path = 'path_example' # str | The BlobFile full path (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a file metadata.
    api_response = api_instance.buckets_get_file_by_key(key, path=path, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_file_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Bucket Id | 
 **path** | **str**| The BlobFile full path | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BlobFileDto**](BlobFileDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get_files_by_key**
> ODataValueOfIEnumerableOfBlobFileDto buckets_get_files_by_key(key, directory=directory, recursive=recursive, file_name_glob=file_name_glob, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets the files in a directory.  Optionally returns all files in all child directories (recursive).

OAuth required scopes: OR.Administration or OR.Administration.Read.  Required permissions: Buckets.View and BlobFiles.View.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Bucket Id
directory = 'directory_example' # str | The directory path (optional)
recursive = false # bool | Recurse subdirectories (flat view) (optional) (default to false)
file_name_glob = 'file_name_glob_example' # str | Files listing filter (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Number of files to return (optional)
skip = 56 # int | Number of files to skip (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets the files in a directory.  Optionally returns all files in all child directories (recursive).
    api_response = api_instance.buckets_get_files_by_key(key, directory=directory, recursive=recursive, file_name_glob=file_name_glob, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_files_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Bucket Id | 
 **directory** | **str**| The directory path | [optional] 
 **recursive** | **bool**| Recurse subdirectories (flat view) | [optional] [default to false]
 **file_name_glob** | **str**| Files listing filter | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Number of files to return | [optional] 
 **skip** | **int**| Number of files to skip | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfBlobFileDto**](ODataValueOfIEnumerableOfBlobFileDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get_folders_for_bucket_by_id**
> AccessibleFoldersDto buckets_get_folders_for_bucket_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get all accessible folders where the bucket is shared, and the total count of folders where it is shared (including unaccessible folders).

OAuth required scopes: OR.Administration or OR.Administration.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
id = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get all accessible folders where the bucket is shared, and the total count of folders where it is shared (including unaccessible folders).
    api_response = api_instance.buckets_get_folders_for_bucket_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_folders_for_bucket_by_id: %s\n" % e)
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

# **buckets_get_read_uri_by_key**
> BlobFileAccessDto buckets_get_read_uri_by_key(key, path=path, expiry_in_minutes=expiry_in_minutes, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a direct download URL for BlobFile.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Required permissions: Buckets.View and BlobFiles.View.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Bucket Id
path = 'path_example' # str | The BlobFile full path (optional)
expiry_in_minutes = 0 # int | URL expiration time (optional) (default to 0)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a direct download URL for BlobFile.
    api_response = api_instance.buckets_get_read_uri_by_key(key, path=path, expiry_in_minutes=expiry_in_minutes, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_read_uri_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Bucket Id | 
 **path** | **str**| The BlobFile full path | [optional] 
 **expiry_in_minutes** | **int**| URL expiration time | [optional] [default to 0]
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BlobFileAccessDto**](BlobFileAccessDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_get_write_uri_by_key**
> BlobFileAccessDto buckets_get_write_uri_by_key(key, path=path, expiry_in_minutes=expiry_in_minutes, content_type=content_type, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a direct upload URL for BlobFile.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Required permissions: Buckets.View and BlobFiles.Create.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | The Bucket Id
path = 'path_example' # str | The BlobFile full path (optional)
expiry_in_minutes = 0 # int | URL Expiration time (optional) (default to 0)
content_type = 'content_type_example' # str | ContentType for S3 access policy (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a direct upload URL for BlobFile.
    api_response = api_instance.buckets_get_write_uri_by_key(key, path=path, expiry_in_minutes=expiry_in_minutes, content_type=content_type, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_get_write_uri_by_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| The Bucket Id | 
 **path** | **str**| The BlobFile full path | [optional] 
 **expiry_in_minutes** | **int**| URL Expiration time | [optional] [default to 0]
 **content_type** | **str**| ContentType for S3 access policy | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BlobFileAccessDto**](BlobFileAccessDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_post**
> BucketDto buckets_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates an Bucket

OAuth required scopes: OR.Administration or OR.Administration.Write.  Required permissions: Buckets.Create.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.BucketDto() # BucketDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates an Bucket
    api_response = api_instance.buckets_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BucketDto**](BucketDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BucketDto**](BucketDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_put_by_id**
> BucketDto buckets_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Updates a bucket.

OAuth required scopes: OR.Administration or OR.Administration.Write.  Required permissions: Buckets.Edit.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.BucketDto() # BucketDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Updates a bucket.
    api_response = api_instance.buckets_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**BucketDto**](BucketDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**BucketDto**](BucketDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets_share_to_folders**
> buckets_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Adds the buckets to the folders specified in 'ToAddFolderIds'. Removes the buckets from the folders specified in 'ToRemoveFolderIds'.

OAuth required scopes: OR.Administration or OR.Administration.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.BucketsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.BucketFoldersShareDto() # BucketFoldersShareDto | Object containing the ids of the buckets and the ids of the folders where they should be shared. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Adds the buckets to the folders specified in 'ToAddFolderIds'. Removes the buckets from the folders specified in 'ToRemoveFolderIds'.
    api_instance.buckets_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets_share_to_folders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BucketFoldersShareDto**](BucketFoldersShareDto.md)| Object containing the ids of the buckets and the ids of the folders where they should be shared. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

