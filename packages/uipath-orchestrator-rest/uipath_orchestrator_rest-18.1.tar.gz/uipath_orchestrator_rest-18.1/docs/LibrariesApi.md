# uipath_orchestrator_rest.LibrariesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**libraries_delete_by_id**](LibrariesApi.md#libraries_delete_by_id) | **DELETE** /odata/Libraries({key}) | Deletes a package.
[**libraries_download_package_by_key**](LibrariesApi.md#libraries_download_package_by_key) | **GET** /odata/Libraries/UiPath.Server.Configuration.OData.DownloadPackage(key&#x3D;{key}) | Downloads the .nupkg file of a Package.
[**libraries_get**](LibrariesApi.md#libraries_get) | **GET** /odata/Libraries | Gets the library packages.
[**libraries_get_versions_by_packageid**](LibrariesApi.md#libraries_get_versions_by_packageid) | **GET** /odata/Libraries/UiPath.Server.Configuration.OData.GetVersions(packageId&#x3D;{packageId}) | Returns a collection of all available versions of a given package. Allows odata query options.
[**libraries_upload_package**](LibrariesApi.md#libraries_upload_package) | **POST** /odata/Libraries/UiPath.Server.Configuration.OData.UploadPackage | Uploads a new package or a new version of an existing package. The content of the package is sent as a .nupkg file embedded in the HTTP request.


# **libraries_delete_by_id**
> libraries_delete_by_id(key, feed_id=feed_id)

Deletes a package.

OAuth required scopes: OR.Execution or OR.Execution.Write.  Required permissions: Libraries.Delete.

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
api_instance = uipath_orchestrator_rest.LibrariesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
feed_id = 'feed_id_example' # str |  (optional)

try:
    # Deletes a package.
    api_instance.libraries_delete_by_id(key, feed_id=feed_id)
except ApiException as e:
    print("Exception when calling LibrariesApi->libraries_delete_by_id: %s\n" % e)
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

# **libraries_download_package_by_key**
> file libraries_download_package_by_key(key, feed_id=feed_id)

Downloads the .nupkg file of a Package.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: Libraries.View.

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
api_instance = uipath_orchestrator_rest.LibrariesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
feed_id = 'feed_id_example' # str |  (optional)

try:
    # Downloads the .nupkg file of a Package.
    api_response = api_instance.libraries_download_package_by_key(key, feed_id=feed_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LibrariesApi->libraries_download_package_by_key: %s\n" % e)
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

# **libraries_get**
> ODataValueOfIEnumerableOfLibraryDto libraries_get(search_term=search_term, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets the library packages.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: Libraries.View.

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
api_instance = uipath_orchestrator_rest.LibrariesApi(uipath_orchestrator_rest.ApiClient(configuration))
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
    # Gets the library packages.
    api_response = api_instance.libraries_get(search_term=search_term, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LibrariesApi->libraries_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfLibraryDto**](ODataValueOfIEnumerableOfLibraryDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **libraries_get_versions_by_packageid**
> ODataValueOfIEnumerableOfLibraryDto libraries_get_versions_by_packageid(package_id, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Returns a collection of all available versions of a given package. Allows odata query options.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: Libraries.View.

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
api_instance = uipath_orchestrator_rest.LibrariesApi(uipath_orchestrator_rest.ApiClient(configuration))
package_id = 'package_id_example' # str | The Id of the package for which the versions are fetched.
feed_id = 'feed_id_example' # str |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns a collection of all available versions of a given package. Allows odata query options.
    api_response = api_instance.libraries_get_versions_by_packageid(package_id, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LibrariesApi->libraries_get_versions_by_packageid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_id** | **str**| The Id of the package for which the versions are fetched. | 
 **feed_id** | [**str**](.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfLibraryDto**](ODataValueOfIEnumerableOfLibraryDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **libraries_upload_package**
> ODataValueOfIEnumerableOfBulkItemDtoOfString libraries_upload_package(file, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count, file1=file1, file2=file2, file3=file3, file4=file4, file5=file5, file6=file6, file7=file7, file8=file8, file9=file9)

Uploads a new package or a new version of an existing package. The content of the package is sent as a .nupkg file embedded in the HTTP request.

OAuth required scopes: OR.Execution or OR.Execution.Write.  Required permissions: Libraries.Create.

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
api_instance = uipath_orchestrator_rest.LibrariesApi(uipath_orchestrator_rest.ApiClient(configuration))
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
    api_response = api_instance.libraries_upload_package(file, feed_id=feed_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count, file1=file1, file2=file2, file3=file3, file4=file4, file5=file5, file6=file6, file7=file7, file8=file8, file9=file9)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LibrariesApi->libraries_upload_package: %s\n" % e)
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

