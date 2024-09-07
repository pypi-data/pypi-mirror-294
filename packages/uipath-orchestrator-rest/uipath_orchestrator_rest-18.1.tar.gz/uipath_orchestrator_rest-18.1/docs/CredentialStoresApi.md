# uipath_orchestrator_rest.CredentialStoresApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**credential_stores_delete_by_id**](CredentialStoresApi.md#credential_stores_delete_by_id) | **DELETE** /odata/CredentialStores({key}) | Deletes a Credential Store.
[**credential_stores_get**](CredentialStoresApi.md#credential_stores_get) | **GET** /odata/CredentialStores | Gets all Credential Stores.
[**credential_stores_get_available_credential_store_types**](CredentialStoresApi.md#credential_stores_get_available_credential_store_types) | **GET** /odata/CredentialStores/UiPath.Server.Configuration.OData.GetAvailableCredentialStoreTypes | Gets available Credential Store types.
[**credential_stores_get_by_id**](CredentialStoresApi.md#credential_stores_get_by_id) | **GET** /odata/CredentialStores({key}) | Gets a single Credential Store by its key.
[**credential_stores_get_default_store_for_resource_type_by_resourcetype**](CredentialStoresApi.md#credential_stores_get_default_store_for_resource_type_by_resourcetype) | **GET** /odata/CredentialStores/UiPath.Server.Configuration.OData.GetDefaultStoreForResourceType(resourceType&#x3D;{resourceType}) | Get the default credential store for the given resource type.
[**credential_stores_get_resources_for_credential_store_types_by_key_and_resourcetype**](CredentialStoresApi.md#credential_stores_get_resources_for_credential_store_types_by_key_and_resourcetype) | **GET** /odata/CredentialStores/UiPath.Server.Configuration.OData.GetResourcesForCredentialStoreTypes(key&#x3D;{key},resourceType&#x3D;{resourceType}) | Gets available resources robots (and later assets) for a credential store.
[**credential_stores_get_resources_for_credentials_proxy_resource_types**](CredentialStoresApi.md#credential_stores_get_resources_for_credentials_proxy_resource_types) | **GET** /odata/CredentialStores/UiPath.Server.Configuration.OData.GetResourcesForCredentialsProxyResourceTypes(key&#x3D;{key},resourceType&#x3D;{resourceType}) | Gets available resources robots (and later assets) for a credential store.
[**credential_stores_post**](CredentialStoresApi.md#credential_stores_post) | **POST** /odata/CredentialStores | Creates a new Credential Store.
[**credential_stores_put_by_id**](CredentialStoresApi.md#credential_stores_put_by_id) | **PUT** /odata/CredentialStores({key}) | Updates a Credential Store.
[**credential_stores_set_default_store_for_resource_type_by_id**](CredentialStoresApi.md#credential_stores_set_default_store_for_resource_type_by_id) | **POST** /odata/CredentialStores({key})/UiPath.Server.Configuration.OData.SetDefaultStoreForResourceType | Sets a credential store as the default for the given credential type.


# **credential_stores_delete_by_id**
> credential_stores_delete_by_id(key, force_delete=force_delete)

Deletes a Credential Store.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Delete.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
force_delete = true # bool |  (optional)

try:
    # Deletes a Credential Store.
    api_instance.credential_stores_delete_by_id(key, force_delete=force_delete)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **force_delete** | **bool**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_get**
> ODataValueOfIEnumerableOfCredentialStoreDto credential_stores_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets all Credential Stores.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View or Assets.Create or Assets.Edit or Assets.View or Robots.Create or Robots.Edit or Robots.View or Buckets.Create or Buckets.Edit.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets all Credential Stores.
    api_response = api_instance.credential_stores_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfCredentialStoreDto**](ODataValueOfIEnumerableOfCredentialStoreDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_get_available_credential_store_types**
> ODataValueOfIEnumerableOfString credential_stores_get_available_credential_store_types(proxy_id=proxy_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Gets available Credential Store types.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
proxy_id = 789 # int |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets available Credential Store types.
    api_response = api_instance.credential_stores_get_available_credential_store_types(proxy_id=proxy_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_get_available_credential_store_types: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proxy_id** | **int**|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfString**](ODataValueOfIEnumerableOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_get_by_id**
> CredentialStoreDto credential_stores_get_by_id(key, expand=expand, select=select)

Gets a single Credential Store by its key.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a single Credential Store by its key.
    api_response = api_instance.credential_stores_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**CredentialStoreDto**](CredentialStoreDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_get_default_store_for_resource_type_by_resourcetype**
> ODataValueOfInt64 credential_stores_get_default_store_for_resource_type_by_resourcetype(resource_type, expand=expand, select=select)

Get the default credential store for the given resource type.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View or Assets.Create or Assets.Edit or Assets.View or Robots.Create or Robots.Edit or Robots.View or Buckets.Create or Buckets.Edit.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
resource_type = 'resource_type_example' # str | Provides the resource type for which to retrieve the default.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Get the default credential store for the given resource type.
    api_response = api_instance.credential_stores_get_default_store_for_resource_type_by_resourcetype(resource_type, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_get_default_store_for_resource_type_by_resourcetype: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_type** | **str**| Provides the resource type for which to retrieve the default. | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfInt64**](ODataValueOfInt64.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_get_resources_for_credential_store_types_by_key_and_resourcetype**
> ODataValueOfIEnumerableOfCredentialStoreResourceDto credential_stores_get_resources_for_credential_store_types_by_key_and_resourcetype(key, resource_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets available resources robots (and later assets) for a credential store.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Provides the ID of the credential store for which to retrieve resources.
resource_type = 'resource_type_example' # str | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets available resources robots (and later assets) for a credential store.
    api_response = api_instance.credential_stores_get_resources_for_credential_store_types_by_key_and_resourcetype(key, resource_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_get_resources_for_credential_store_types_by_key_and_resourcetype: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Provides the ID of the credential store for which to retrieve resources. | 
 **resource_type** | **str**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfCredentialStoreResourceDto**](ODataValueOfIEnumerableOfCredentialStoreResourceDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_get_resources_for_credentials_proxy_resource_types**
> ODataValueOfIEnumerableOfCredentialsProxyResourceDto credential_stores_get_resources_for_credentials_proxy_resource_types(key, resource_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets available resources robots (and later assets) for a credential store.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Provides the ID of the credential store for which to retrieve resources.
resource_type = 'resource_type_example' # str | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets available resources robots (and later assets) for a credential store.
    api_response = api_instance.credential_stores_get_resources_for_credentials_proxy_resource_types(key, resource_type, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_get_resources_for_credentials_proxy_resource_types: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Provides the ID of the credential store for which to retrieve resources. | 
 **resource_type** | **str**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfCredentialsProxyResourceDto**](ODataValueOfIEnumerableOfCredentialsProxyResourceDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_post**
> CredentialStoreDto credential_stores_post(body=body)

Creates a new Credential Store.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Create.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.CredentialStoreDto() # CredentialStoreDto |  (optional)

try:
    # Creates a new Credential Store.
    api_response = api_instance.credential_stores_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CredentialStoreDto**](CredentialStoreDto.md)|  | [optional] 

### Return type

[**CredentialStoreDto**](CredentialStoreDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_put_by_id**
> credential_stores_put_by_id(key, body=body)

Updates a Credential Store.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Edit.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.CredentialStoreDto() # CredentialStoreDto |  (optional)

try:
    # Updates a Credential Store.
    api_instance.credential_stores_put_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**CredentialStoreDto**](CredentialStoreDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **credential_stores_set_default_store_for_resource_type_by_id**
> credential_stores_set_default_store_for_resource_type_by_id(key, body=body)

Sets a credential store as the default for the given credential type.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Edit.

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
api_instance = uipath_orchestrator_rest.CredentialStoresApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | Provides the ID of the credential store to set as default.
body = uipath_orchestrator_rest.CredentialSetDefaultStoreForResourceTypeRequest() # CredentialSetDefaultStoreForResourceTypeRequest | Provides the resourceType that indicates                     the resource type for which the stores becomes default. (optional)

try:
    # Sets a credential store as the default for the given credential type.
    api_instance.credential_stores_set_default_store_for_resource_type_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling CredentialStoresApi->credential_stores_set_default_store_for_resource_type_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**| Provides the ID of the credential store to set as default. | 
 **body** | [**CredentialSetDefaultStoreForResourceTypeRequest**](CredentialSetDefaultStoreForResourceTypeRequest.md)| Provides the resourceType that indicates                     the resource type for which the stores becomes default. | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

