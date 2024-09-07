# uipath_orchestrator_rest.MaintenanceApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**maintenance_end**](MaintenanceApi.md#maintenance_end) | **POST** /api/Maintenance/End | Ends a maintenance window
[**maintenance_get**](MaintenanceApi.md#maintenance_get) | **GET** /api/Maintenance/Get | Gets the host admin logs.
[**maintenance_start**](MaintenanceApi.md#maintenance_start) | **POST** /api/Maintenance/Start | Starts a maintenance window


# **maintenance_end**
> maintenance_end(tenant_id=tenant_id)

Ends a maintenance window

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
api_instance = uipath_orchestrator_rest.MaintenanceApi(uipath_orchestrator_rest.ApiClient(configuration))
tenant_id = 56 # int |  (optional)

try:
    # Ends a maintenance window
    api_instance.maintenance_end(tenant_id=tenant_id)
except ApiException as e:
    print("Exception when calling MaintenanceApi->maintenance_end: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant_id** | **int**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **maintenance_get**
> MaintenanceSetting maintenance_get(tenant_id=tenant_id)

Gets the host admin logs.

OAuth required scopes: OR.Administration or OR.Administration.Read.  Host only. Required permissions: Audit.View.

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
api_instance = uipath_orchestrator_rest.MaintenanceApi(uipath_orchestrator_rest.ApiClient(configuration))
tenant_id = 56 # int |  (optional)

try:
    # Gets the host admin logs.
    api_response = api_instance.maintenance_get(tenant_id=tenant_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MaintenanceApi->maintenance_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant_id** | **int**|  | [optional] 

### Return type

[**MaintenanceSetting**](MaintenanceSetting.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **maintenance_start**
> maintenance_start(phase=phase, force=force, kill_jobs=kill_jobs, tenant_id=tenant_id)

Starts a maintenance window

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
api_instance = uipath_orchestrator_rest.MaintenanceApi(uipath_orchestrator_rest.ApiClient(configuration))
phase = 'phase_example' # str | Phase - UiPath.Orchestrator.DataContracts.MaintenanceState.Draining or UiPath.Orchestrator.DataContracts.MaintenanceState.Suspended (optional)
force = false # bool | Whether to ignore errors during transition (optional) (default to false)
kill_jobs = false # bool | Whether to force-kill running jobs when transitioning to UiPath.Orchestrator.DataContracts.MaintenanceState.Suspended (optional) (default to false)
tenant_id = 56 # int | If tenant id is set, maintenance will start only for this tenant (optional)

try:
    # Starts a maintenance window
    api_instance.maintenance_start(phase=phase, force=force, kill_jobs=kill_jobs, tenant_id=tenant_id)
except ApiException as e:
    print("Exception when calling MaintenanceApi->maintenance_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **phase** | **str**| Phase - UiPath.Orchestrator.DataContracts.MaintenanceState.Draining or UiPath.Orchestrator.DataContracts.MaintenanceState.Suspended | [optional] 
 **force** | **bool**| Whether to ignore errors during transition | [optional] [default to false]
 **kill_jobs** | **bool**| Whether to force-kill running jobs when transitioning to UiPath.Orchestrator.DataContracts.MaintenanceState.Suspended | [optional] [default to false]
 **tenant_id** | **int**| If tenant id is set, maintenance will start only for this tenant | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

