# uipath_orchestrator_rest.DirectoryServiceApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**directory_service_get_directory_permissions**](DirectoryServiceApi.md#directory_service_get_directory_permissions) | **GET** /api/DirectoryService/GetDirectoryPermissions | Gets directory permissions
[**directory_service_get_domains**](DirectoryServiceApi.md#directory_service_get_domains) | **GET** /api/DirectoryService/GetDomains | Gets domains
[**directory_service_search_for_users_and_groups**](DirectoryServiceApi.md#directory_service_search_for_users_and_groups) | **GET** /api/DirectoryService/SearchForUsersAndGroups | Search users and groups


# **directory_service_get_directory_permissions**
> list[DirectoryPermissionDto] directory_service_get_directory_permissions(username=username, domain=domain)

Gets directory permissions

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: Users.View.

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
api_instance = uipath_orchestrator_rest.DirectoryServiceApi(uipath_orchestrator_rest.ApiClient(configuration))
username = 'username_example' # str |  (optional)
domain = 'domain_example' # str |  (optional)

try:
    # Gets directory permissions
    api_response = api_instance.directory_service_get_directory_permissions(username=username, domain=domain)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryServiceApi->directory_service_get_directory_permissions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | [optional] 
 **domain** | **str**|  | [optional] 

### Return type

[**list[DirectoryPermissionDto]**](DirectoryPermissionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **directory_service_get_domains**
> list[DomainDto] directory_service_get_domains()

Gets domains

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: (Users.View or Units.Edit or SubFolders.Edit).

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
api_instance = uipath_orchestrator_rest.DirectoryServiceApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Gets domains
    api_response = api_instance.directory_service_get_domains()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryServiceApi->directory_service_get_domains: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[DomainDto]**](DomainDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **directory_service_search_for_users_and_groups**
> list[DirectoryObjectDto] directory_service_search_for_users_and_groups(search_context=search_context, domain=domain, prefix=prefix)

Search users and groups

OAuth required scopes: OR.Users or OR.Users.Read.  Required permissions: (Users.View or Units.Edit or SubFolders.Edit).

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
api_instance = uipath_orchestrator_rest.DirectoryServiceApi(uipath_orchestrator_rest.ApiClient(configuration))
search_context = 'search_context_example' # str |  (optional)
domain = 'domain_example' # str |  (optional)
prefix = 'prefix_example' # str |  (optional)

try:
    # Search users and groups
    api_response = api_instance.directory_service_search_for_users_and_groups(search_context=search_context, domain=domain, prefix=prefix)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectoryServiceApi->directory_service_search_for_users_and_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_context** | **str**|  | [optional] 
 **domain** | **str**|  | [optional] 
 **prefix** | **str**|  | [optional] 

### Return type

[**list[DirectoryObjectDto]**](DirectoryObjectDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

