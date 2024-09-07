# uipath_orchestrator_rest.HostLicensesApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**host_licenses_activate_license_offline**](HostLicensesApi.md#host_licenses_activate_license_offline) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.ActivateLicenseOffline | Uploads a new offline license activation.  The content of the license is sent as a file embedded in the HTTP request.
[**host_licenses_activate_license_online**](HostLicensesApi.md#host_licenses_activate_license_online) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.ActivateLicenseOnline | Activate the license for the host
[**host_licenses_deactivate_license_online**](HostLicensesApi.md#host_licenses_deactivate_license_online) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.DeactivateLicenseOnline | Deactivate the license for the host
[**host_licenses_delete_by_id**](HostLicensesApi.md#host_licenses_delete_by_id) | **DELETE** /odata/HostLicenses({key}) | Deletes a host license based on its key.
[**host_licenses_delete_tenant_license**](HostLicensesApi.md#host_licenses_delete_tenant_license) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.DeleteTenantLicense | Deletes a tenant license based on its key.
[**host_licenses_get**](HostLicensesApi.md#host_licenses_get) | **GET** /odata/HostLicenses | Gets host licenses.
[**host_licenses_get_by_id**](HostLicensesApi.md#host_licenses_get_by_id) | **GET** /odata/HostLicenses({key}) | Gets a single host license based on its key.
[**host_licenses_get_deactivate_license_offline**](HostLicensesApi.md#host_licenses_get_deactivate_license_offline) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.GetDeactivateLicenseOffline | Deactivate the license offline for the host
[**host_licenses_get_license_offline**](HostLicensesApi.md#host_licenses_get_license_offline) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.GetLicenseOffline | Create the offline activation request for the host
[**host_licenses_get_tenant_license_by_tenantid**](HostLicensesApi.md#host_licenses_get_tenant_license_by_tenantid) | **GET** /odata/HostLicenses/UiPath.Server.Configuration.OData.GetTenantLicense(tenantId&#x3D;{tenantId}) | Gets a single tenant license based on its id.
[**host_licenses_set_tenant_license**](HostLicensesApi.md#host_licenses_set_tenant_license) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.SetTenantLicense | Sets the license for a specific tenant
[**host_licenses_update_license_online**](HostLicensesApi.md#host_licenses_update_license_online) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.UpdateLicenseOnline | Update the license for the host
[**host_licenses_upload_license**](HostLicensesApi.md#host_licenses_upload_license) | **POST** /odata/HostLicenses/UiPath.Server.Configuration.OData.UploadLicense | Uploads a new host license file that was previously generated with Regutil.  The content of the license is sent as a file embedded in the HTTP request.


# **host_licenses_activate_license_offline**
> host_licenses_activate_license_offline(file)

Uploads a new offline license activation.  The content of the license is sent as a file embedded in the HTTP request.

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
file = '/path/to/file.txt' # file | 

try:
    # Uploads a new offline license activation.  The content of the license is sent as a file embedded in the HTTP request.
    api_instance.host_licenses_activate_license_offline(file)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_activate_license_offline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_activate_license_online**
> host_licenses_activate_license_online(body=body)

Activate the license for the host

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.LicenseRequest() # LicenseRequest |  (optional)

try:
    # Activate the license for the host
    api_instance.host_licenses_activate_license_online(body=body)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_activate_license_online: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LicenseRequest**](LicenseRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_deactivate_license_online**
> host_licenses_deactivate_license_online(body=body)

Deactivate the license for the host

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.DeactivateLicenseRequest() # DeactivateLicenseRequest |  (optional)

try:
    # Deactivate the license for the host
    api_instance.host_licenses_deactivate_license_online(body=body)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_deactivate_license_online: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeactivateLicenseRequest**](DeactivateLicenseRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_delete_by_id**
> host_licenses_delete_by_id(key)

Deletes a host license based on its key.

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Deletes a host license based on its key.
    api_instance.host_licenses_delete_by_id(key)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_delete_by_id: %s\n" % e)
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

# **host_licenses_delete_tenant_license**
> host_licenses_delete_tenant_license(body=body)

Deletes a tenant license based on its key.

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.HostDeleteTenantLicenseRequest() # HostDeleteTenantLicenseRequest |  (optional)

try:
    # Deletes a tenant license based on its key.
    api_instance.host_licenses_delete_tenant_license(body=body)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_delete_tenant_license: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HostDeleteTenantLicenseRequest**](HostDeleteTenantLicenseRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_get**
> ODataValueOfIEnumerableOfHostLicenseDto host_licenses_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets host licenses.

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets host licenses.
    api_response = api_instance.host_licenses_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfHostLicenseDto**](ODataValueOfIEnumerableOfHostLicenseDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_get_by_id**
> HostLicenseDto host_licenses_get_by_id(key, expand=expand, select=select)

Gets a single host license based on its key.

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a single host license based on its key.
    api_response = api_instance.host_licenses_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**HostLicenseDto**](HostLicenseDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_get_deactivate_license_offline**
> ODataValueOfString host_licenses_get_deactivate_license_offline(body=body, expand=expand, select=select)

Deactivate the license offline for the host

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.DeactivateLicenseRequest() # DeactivateLicenseRequest |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Deactivate the license offline for the host
    api_response = api_instance.host_licenses_get_deactivate_license_offline(body=body, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_get_deactivate_license_offline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeactivateLicenseRequest**](DeactivateLicenseRequest.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfString**](ODataValueOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_get_license_offline**
> ODataValueOfString host_licenses_get_license_offline(body=body, expand=expand, select=select)

Create the offline activation request for the host

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.LicenseRequest() # LicenseRequest |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Create the offline activation request for the host
    api_response = api_instance.host_licenses_get_license_offline(body=body, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_get_license_offline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LicenseRequest**](LicenseRequest.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfString**](ODataValueOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_get_tenant_license_by_tenantid**
> LicenseDto host_licenses_get_tenant_license_by_tenantid(tenant_id, expand=expand, select=select)

Gets a single tenant license based on its id.

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
tenant_id = 56 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a single tenant license based on its id.
    api_response = api_instance.host_licenses_get_tenant_license_by_tenantid(tenant_id, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_get_tenant_license_by_tenantid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant_id** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**LicenseDto**](LicenseDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_set_tenant_license**
> host_licenses_set_tenant_license(body=body)

Sets the license for a specific tenant

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.HostSetTenantLicenseRequest() # HostSetTenantLicenseRequest |  (optional)

try:
    # Sets the license for a specific tenant
    api_instance.host_licenses_set_tenant_license(body=body)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_set_tenant_license: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HostSetTenantLicenseRequest**](HostSetTenantLicenseRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_update_license_online**
> host_licenses_update_license_online()

Update the license for the host

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Update the license for the host
    api_instance.host_licenses_update_license_online()
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_update_license_online: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **host_licenses_upload_license**
> HostLicenseDto host_licenses_upload_license(file, expand=expand, select=select)

Uploads a new host license file that was previously generated with Regutil.  The content of the license is sent as a file embedded in the HTTP request.

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
api_instance = uipath_orchestrator_rest.HostLicensesApi(uipath_orchestrator_rest.ApiClient(configuration))
file = '/path/to/file.txt' # file | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Uploads a new host license file that was previously generated with Regutil.  The content of the license is sent as a file embedded in the HTTP request.
    api_response = api_instance.host_licenses_upload_license(file, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HostLicensesApi->host_licenses_upload_license: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**HostLicenseDto**](HostLicenseDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

