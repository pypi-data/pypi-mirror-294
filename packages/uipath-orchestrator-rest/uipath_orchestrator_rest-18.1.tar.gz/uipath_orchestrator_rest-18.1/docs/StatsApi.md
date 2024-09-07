# uipath_orchestrator_rest.StatsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**stats_get_consumption_license_stats**](StatsApi.md#stats_get_consumption_license_stats) | **GET** /api/Stats/GetConsumptionLicenseStats | Gets the consumption licensing usage statistics
[**stats_get_count_stats**](StatsApi.md#stats_get_count_stats) | **GET** /api/Stats/GetCountStats | Gets the total number of various entities registered in Orchestrator
[**stats_get_jobs_stats**](StatsApi.md#stats_get_jobs_stats) | **GET** /api/Stats/GetJobsStats | Gets the total number of jobs aggregated by Job State
[**stats_get_license_stats**](StatsApi.md#stats_get_license_stats) | **GET** /api/Stats/GetLicenseStats | Gets the licensing usage statistics
[**stats_get_sessions_stats**](StatsApi.md#stats_get_sessions_stats) | **GET** /api/Stats/GetSessionsStats | Gets the total number of robots aggregated by Robot State


# **stats_get_consumption_license_stats**
> list[ConsumptionLicenseStatsModel] stats_get_consumption_license_stats(tenant_id=tenant_id, days=days)

Gets the consumption licensing usage statistics

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: License.View.

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
api_instance = uipath_orchestrator_rest.StatsApi(uipath_orchestrator_rest.ApiClient(configuration))
tenant_id = 56 # int | The Tenant's Id - can be used when authenticated as Host (optional)
days = 56 # int | Number of reported license usage days (optional)

try:
    # Gets the consumption licensing usage statistics
    api_response = api_instance.stats_get_consumption_license_stats(tenant_id=tenant_id, days=days)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatsApi->stats_get_consumption_license_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant_id** | **int**| The Tenant&#39;s Id - can be used when authenticated as Host | [optional] 
 **days** | **int**| Number of reported license usage days | [optional] 

### Return type

[**list[ConsumptionLicenseStatsModel]**](ConsumptionLicenseStatsModel.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stats_get_count_stats**
> list[CountStats] stats_get_count_stats()

Gets the total number of various entities registered in Orchestrator

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Requires authentication.  Returns the name and the total number of entities registered in Orchestrator for a set of entities.  All the counted entity types can be seen in the result below.       [             {               \"title\": \"Processes\",               \"count\": 1             },             {               \"title\": \"Assets\",               \"count\": 0             },             {               \"title\": \"Queues\",               \"count\": 0             },             {               \"title\": \"Schedules\",               \"count\": 0             }       ]

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
api_instance = uipath_orchestrator_rest.StatsApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Gets the total number of various entities registered in Orchestrator
    api_response = api_instance.stats_get_count_stats()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatsApi->stats_get_count_stats: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CountStats]**](CountStats.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stats_get_jobs_stats**
> list[CountStats] stats_get_jobs_stats()

Gets the total number of jobs aggregated by Job State

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: Jobs.View.  Returns the total number of Successful, Faulted and Canceled jobs respectively.  Example of returned result:      [            {              \"title\": \"Successful\",              \"count\": 0            },            {              \"title\": \"Faulted\",              \"count\": 0            },            {              \"title\": \"Canceled\",              \"count\": 0            }      ]

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
api_instance = uipath_orchestrator_rest.StatsApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Gets the total number of jobs aggregated by Job State
    api_response = api_instance.stats_get_jobs_stats()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatsApi->stats_get_jobs_stats: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CountStats]**](CountStats.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stats_get_license_stats**
> list[LicenseStatsModel] stats_get_license_stats(tenant_id=tenant_id, days=days)

Gets the licensing usage statistics

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: License.View.

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
api_instance = uipath_orchestrator_rest.StatsApi(uipath_orchestrator_rest.ApiClient(configuration))
tenant_id = 56 # int | The Tenant's Id - can be used when authenticated as Host (optional)
days = 56 # int | Number of reported license usage days (optional)

try:
    # Gets the licensing usage statistics
    api_response = api_instance.stats_get_license_stats(tenant_id=tenant_id, days=days)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatsApi->stats_get_license_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant_id** | **int**| The Tenant&#39;s Id - can be used when authenticated as Host | [optional] 
 **days** | **int**| Number of reported license usage days | [optional] 

### Return type

[**list[LicenseStatsModel]**](LicenseStatsModel.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stats_get_sessions_stats**
> list[CountStats] stats_get_sessions_stats()

Gets the total number of robots aggregated by Robot State

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: Robots.View.  Returns the total number of Available, Busy, Disconnected and Unresponsive robots respectively.  Example of returned result:      [            {              \"title\": \"Available\",              \"count\": 1            },            {              \"title\": \"Busy\",              \"count\": 0            },            {              \"title\": \"Disconnected\",              \"count\": 1            },            {              \"title\": \"Unresponsive\",              \"count\": 0            }      ]

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
api_instance = uipath_orchestrator_rest.StatsApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Gets the total number of robots aggregated by Robot State
    api_response = api_instance.stats_get_sessions_stats()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatsApi->stats_get_sessions_stats: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CountStats]**](CountStats.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

