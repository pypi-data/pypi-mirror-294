# uipath_orchestrator_rest.AssetsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**assets_delete_by_id**](AssetsApi.md#assets_delete_by_id) | **DELETE** /odata/Assets({key}) | Delete an asset
[**assets_get**](AssetsApi.md#assets_get) | **GET** /odata/Assets | Get Assets
[**assets_get_assets_across_folders**](AssetsApi.md#assets_get_assets_across_folders) | **GET** /odata/Assets/UiPath.Server.Configuration.OData.GetAssetsAcrossFolders | Get the assets from all the folders in which the current user has the Assets.View permission, except the one specified.
[**assets_get_by_id**](AssetsApi.md#assets_get_by_id) | **GET** /odata/Assets({key}) | Gets a single asset based on its id
[**assets_get_filtered**](AssetsApi.md#assets_get_filtered) | **GET** /odata/Assets/UiPath.Server.Configuration.OData.GetFiltered | Get Filtered Assets
[**assets_get_folders_for_asset_by_id**](AssetsApi.md#assets_get_folders_for_asset_by_id) | **GET** /odata/Assets/UiPath.Server.Configuration.OData.GetFoldersForAsset(id&#x3D;{id}) | Get all accesible folders where the asset is shared, and the total count of folders where it is shared (including unaccessible folders).
[**assets_get_robot_asset_by_name_for_robot_key**](AssetsApi.md#assets_get_robot_asset_by_name_for_robot_key) | **POST** /odata/Assets/UiPath.Server.Configuration.OData.GetRobotAssetByNameForRobotKey | Returns the named asset associated to the given robot key.
[**assets_get_robot_asset_by_robot_id**](AssetsApi.md#assets_get_robot_asset_by_robot_id) | **GET** /odata/Assets/UiPath.Server.Configuration.OData.GetRobotAssetByRobotId(robotId&#x3D;{robotId},assetName&#x3D;{assetName}) | Returns the named asset associated to the given robot Id.
[**assets_get_robot_asset_by_robotid_and_assetname**](AssetsApi.md#assets_get_robot_asset_by_robotid_and_assetname) | **GET** /odata/Assets/UiPath.Server.Configuration.OData.GetRobotAsset(robotId&#x3D;{robotId},assetName&#x3D;{assetName}) | Returns the named asset associated to the given robot key.
[**assets_post**](AssetsApi.md#assets_post) | **POST** /odata/Assets | Creates an asset
[**assets_put_by_id**](AssetsApi.md#assets_put_by_id) | **PUT** /odata/Assets({key}) | Edit an asset
[**assets_set_robot_asset_by_robot_key**](AssetsApi.md#assets_set_robot_asset_by_robot_key) | **POST** /odata/Assets/UiPath.Server.Configuration.OData.SetRobotAssetByRobotKey | Set the asset value associated to the given robot key.
[**assets_share_to_folders**](AssetsApi.md#assets_share_to_folders) | **POST** /odata/Assets/UiPath.Server.Configuration.OData.ShareToFolders | Adds the assets to the folders specified in &#39;ToAddFolderIds&#39;. Removes the assets from the folders specified in &#39;ToRemoveFolderIds&#39;.


# **assets_delete_by_id**
> assets_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Delete an asset

OAuth required scopes: OR.Assets or OR.Assets.Write.  Required permissions: Assets.Delete.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Delete an asset
    api_instance.assets_delete_by_id(key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_delete_by_id: %s\n" % e)
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

# **assets_get**
> ODataValueOfIEnumerableOfAssetDto assets_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get Assets

OAuth required scopes: OR.Assets or OR.Assets.Read.  Required permissions: Assets.View. DEPRECATED:  Replaced by GetFiltered. Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get Assets
    api_response = api_instance.assets_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfAssetDto**](ODataValueOfIEnumerableOfAssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_get_assets_across_folders**
> ODataValueOfIEnumerableOfAssetDto assets_get_assets_across_folders(exclude_folder_id=exclude_folder_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get the assets from all the folders in which the current user has the Assets.View permission, except the one specified.

OAuth required scopes: OR.Assets or OR.Assets.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
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
    # Get the assets from all the folders in which the current user has the Assets.View permission, except the one specified.
    api_response = api_instance.assets_get_assets_across_folders(exclude_folder_id=exclude_folder_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get_assets_across_folders: %s\n" % e)
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

[**ODataValueOfIEnumerableOfAssetDto**](ODataValueOfIEnumerableOfAssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_get_by_id**
> AssetDto assets_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets a single asset based on its id

OAuth required scopes: OR.Assets or OR.Assets.Read.  Required permissions: Assets.View.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets a single asset based on its id
    api_response = api_instance.assets_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**AssetDto**](AssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_get_filtered**
> ODataValueOfIEnumerableOfAssetDto assets_get_filtered(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get Filtered Assets

OAuth required scopes: OR.Assets or OR.Assets.Read.  Required permissions: Assets.View.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get Filtered Assets
    api_response = api_instance.assets_get_filtered(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get_filtered: %s\n" % e)
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

[**ODataValueOfIEnumerableOfAssetDto**](ODataValueOfIEnumerableOfAssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_get_folders_for_asset_by_id**
> AccessibleFoldersDto assets_get_folders_for_asset_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get all accesible folders where the asset is shared, and the total count of folders where it is shared (including unaccessible folders).

OAuth required scopes: OR.Assets or OR.Assets.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
id = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get all accesible folders where the asset is shared, and the total count of folders where it is shared (including unaccessible folders).
    api_response = api_instance.assets_get_folders_for_asset_by_id(id, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get_folders_for_asset_by_id: %s\n" % e)
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

# **assets_get_robot_asset_by_name_for_robot_key**
> RobotAssetDto assets_get_robot_asset_by_name_for_robot_key(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns the named asset associated to the given robot key.

OAuth required scopes: OR.Assets or OR.Assets.Write.  Required permissions: Assets.View.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.AssetsGetRobotByNameAndKeyRequest() # AssetsGetRobotByNameAndKeyRequest |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns the named asset associated to the given robot key.
    api_response = api_instance.assets_get_robot_asset_by_name_for_robot_key(body=body, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get_robot_asset_by_name_for_robot_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AssetsGetRobotByNameAndKeyRequest**](AssetsGetRobotByNameAndKeyRequest.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**RobotAssetDto**](RobotAssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_get_robot_asset_by_robot_id**
> RobotAssetDto assets_get_robot_asset_by_robot_id(robot_id, asset_name, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns the named asset associated to the given robot Id.

OAuth required scopes: OR.Assets or OR.Assets.Read.  Required permissions: Assets.View.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
robot_id = 789 # int | The Id of the robot for which the asset is being fetched.
asset_name = 'asset_name_example' # str | The name of the asset being fetched.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns the named asset associated to the given robot Id.
    api_response = api_instance.assets_get_robot_asset_by_robot_id(robot_id, asset_name, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get_robot_asset_by_robot_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **robot_id** | **int**| The Id of the robot for which the asset is being fetched. | 
 **asset_name** | **str**| The name of the asset being fetched. | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**RobotAssetDto**](RobotAssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_get_robot_asset_by_robotid_and_assetname**
> RobotAssetDto assets_get_robot_asset_by_robotid_and_assetname(robot_id, asset_name, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns the named asset associated to the given robot key.

OAuth required scopes: OR.Assets or OR.Assets.Read.  Required permissions: Assets.View. DEPRECATED:  Use the GetRobotAssetByNameForRobotKey endpoint. Kept for backwards compatibility. Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
robot_id = 'robot_id_example' # str | The key of the robot for which the asset is being fetched.
asset_name = 'asset_name_example' # str | The name of the asset being fetched.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns the named asset associated to the given robot key.
    api_response = api_instance.assets_get_robot_asset_by_robotid_and_assetname(robot_id, asset_name, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_get_robot_asset_by_robotid_and_assetname: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **robot_id** | **str**| The key of the robot for which the asset is being fetched. | 
 **asset_name** | **str**| The name of the asset being fetched. | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**RobotAssetDto**](RobotAssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_post**
> AssetDto assets_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Creates an asset

OAuth required scopes: OR.Assets or OR.Assets.Write.  Required permissions: Assets.Create.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.AssetDto() # AssetDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Creates an asset
    api_response = api_instance.assets_post(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AssetDto**](AssetDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**AssetDto**](AssetDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_put_by_id**
> assets_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Edit an asset

OAuth required scopes: OR.Assets or OR.Assets.Write.  Required permissions: Assets.Edit.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.AssetDto() # AssetDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Edit an asset
    api_instance.assets_put_by_id(key, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**AssetDto**](AssetDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_set_robot_asset_by_robot_key**
> assets_set_robot_asset_by_robot_key(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Set the asset value associated to the given robot key.

OAuth required scopes: OR.Assets or OR.Assets.Write.  Required permissions: Assets.Edit.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.AssetsSetRobotAssetsByKeyRequest() # AssetsSetRobotAssetsByKeyRequest |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Set the asset value associated to the given robot key.
    api_instance.assets_set_robot_asset_by_robot_key(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_set_robot_asset_by_robot_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AssetsSetRobotAssetsByKeyRequest**](AssetsSetRobotAssetsByKeyRequest.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assets_share_to_folders**
> assets_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Adds the assets to the folders specified in 'ToAddFolderIds'. Removes the assets from the folders specified in 'ToRemoveFolderIds'.

OAuth required scopes: OR.Assets or OR.Assets.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.AssetsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.AssetFoldersShareDto() # AssetFoldersShareDto | Object containing the ids of the assets, the ids of the folders where they should be shared and the ids of the folders from which they should be removed. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Adds the assets to the folders specified in 'ToAddFolderIds'. Removes the assets from the folders specified in 'ToRemoveFolderIds'.
    api_instance.assets_share_to_folders(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling AssetsApi->assets_share_to_folders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AssetFoldersShareDto**](AssetFoldersShareDto.md)| Object containing the ids of the assets, the ids of the folders where they should be shared and the ids of the folders from which they should be removed. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

