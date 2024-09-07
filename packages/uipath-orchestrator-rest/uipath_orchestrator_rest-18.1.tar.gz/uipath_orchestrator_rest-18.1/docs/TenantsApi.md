# uipath_orchestrator_rest.TenantsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tenants_delete_by_id**](TenantsApi.md#tenants_delete_by_id) | **DELETE** /odata/Tenants({key}) | Deletes a tenant based on its id.
[**tenants_get**](TenantsApi.md#tenants_get) | **GET** /odata/Tenants | Gets tenants.
[**tenants_get_by_id**](TenantsApi.md#tenants_get_by_id) | **GET** /odata/Tenants({key}) | Gets a single tenant based on its id.
[**tenants_patch_by_id**](TenantsApi.md#tenants_patch_by_id) | **PATCH** /odata/Tenants({key}) | Partially updates a tenant
[**tenants_post**](TenantsApi.md#tenants_post) | **POST** /odata/Tenants | Creates a tenant.
[**tenants_set_active**](TenantsApi.md#tenants_set_active) | **POST** /odata/Tenants/UiPath.Server.Configuration.OData.SetActive | Toggles the active status of tenants


# **tenants_delete_by_id**
> tenants_delete_by_id(key)

Deletes a tenant based on its id.

OAuth required scopes: OR.Administration or OR.Administration.Write.  Host only. Requires authentication.

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
api_instance = uipath_orchestrator_rest.TenantsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | 

try:
    # Deletes a tenant based on its id.
    api_instance.tenants_delete_by_id(key)
except ApiException as e:
    print("Exception when calling TenantsApi->tenants_delete_by_id: %s\n" % e)
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

# **tenants_get**
> ODataValueOfIEnumerableOfTenantDto tenants_get(skip_last_login_time=skip_last_login_time, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets tenants.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Host only. Requires authentication.

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
api_instance = uipath_orchestrator_rest.TenantsApi(uipath_orchestrator_rest.ApiClient(configuration))
skip_last_login_time = false # bool | Skips computation of last login time for an improved performance (optional) (default to false)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets tenants.
    api_response = api_instance.tenants_get(skip_last_login_time=skip_last_login_time, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->tenants_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip_last_login_time** | **bool**| Skips computation of last login time for an improved performance | [optional] [default to false]
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfTenantDto**](ODataValueOfIEnumerableOfTenantDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tenants_get_by_id**
> TenantDto tenants_get_by_id(key, expand=expand, select=select)

Gets a single tenant based on its id.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Host only. Requires authentication.

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
api_instance = uipath_orchestrator_rest.TenantsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a single tenant based on its id.
    api_response = api_instance.tenants_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->tenants_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**TenantDto**](TenantDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tenants_patch_by_id**
> tenants_patch_by_id(key, body=body)

Partially updates a tenant

OAuth required scopes: OR.Administration or OR.Administration.Write.  Host only. Requires authentication.

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
api_instance = uipath_orchestrator_rest.TenantsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 56 # int | 
body = uipath_orchestrator_rest.TenantDto() # TenantDto |  (optional)

try:
    # Partially updates a tenant
    api_instance.tenants_patch_by_id(key, body=body)
except ApiException as e:
    print("Exception when calling TenantsApi->tenants_patch_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**TenantDto**](TenantDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tenants_post**
> TenantDto tenants_post(body=body)

Creates a tenant.

OAuth required scopes: OR.Administration or OR.Administration.Write.  Host only. Requires authentication.

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
api_instance = uipath_orchestrator_rest.TenantsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TenantDto() # TenantDto |  (optional)

try:
    # Creates a tenant.
    api_response = api_instance.tenants_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->tenants_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TenantDto**](TenantDto.md)|  | [optional] 

### Return type

[**TenantDto**](TenantDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tenants_set_active**
> tenants_set_active(body=body)

Toggles the active status of tenants

OAuth required scopes: OR.Administration or OR.Administration.Write.  Host only. Requires authentication.

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
api_instance = uipath_orchestrator_rest.TenantsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TenantSetActiveRequest() # TenantSetActiveRequest |  (optional)

try:
    # Toggles the active status of tenants
    api_instance.tenants_set_active(body=body)
except ApiException as e:
    print("Exception when calling TenantsApi->tenants_set_active: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TenantSetActiveRequest**](TenantSetActiveRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

