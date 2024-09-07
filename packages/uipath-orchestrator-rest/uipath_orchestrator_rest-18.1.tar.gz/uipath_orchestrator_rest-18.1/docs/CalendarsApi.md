# uipath_orchestrator_rest.CalendarsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**calendars_calendar_exists**](CalendarsApi.md#calendars_calendar_exists) | **POST** /odata/Calendars/UiPath.Server.Configuration.OData.CalendarExists | Validate calendar name, and check if it already exists.
[**calendars_delete_by_id**](CalendarsApi.md#calendars_delete_by_id) | **DELETE** /odata/Calendars({key}) | Deletes a calendar.
[**calendars_get**](CalendarsApi.md#calendars_get) | **GET** /odata/Calendars | Gets calendars for current tenant.
[**calendars_get_by_id**](CalendarsApi.md#calendars_get_by_id) | **GET** /odata/Calendars({key}) | Gets calendar based on its id.
[**calendars_post**](CalendarsApi.md#calendars_post) | **POST** /odata/Calendars | Creates a new calendar.
[**calendars_put_by_id**](CalendarsApi.md#calendars_put_by_id) | **PUT** /odata/Calendars({key}) | Edits a calendar.


# **calendars_calendar_exists**
> ODataValueOfBoolean calendars_calendar_exists(body=body, expand=expand, select=select)

Validate calendar name, and check if it already exists.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: (Settings.Edit).

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
api_instance = uipath_orchestrator_rest.CalendarsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.CalendarExistsRequest() # CalendarExistsRequest |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Validate calendar name, and check if it already exists.
    api_response = api_instance.calendars_calendar_exists(body=body, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CalendarsApi->calendars_calendar_exists: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CalendarExistsRequest**](CalendarExistsRequest.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfBoolean**](ODataValueOfBoolean.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **calendars_delete_by_id**
> calendars_delete_by_id(key)

Deletes a calendar.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: (Settings.Delete).

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
api_instance = uipath_orchestrator_rest.CalendarsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 

try:
    # Deletes a calendar.
    api_instance.calendars_delete_by_id(key)
except ApiException as e:
    print("Exception when calling CalendarsApi->calendars_delete_by_id: %s\n" % e)
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

# **calendars_get**
> ODataValueOfIEnumerableOfExtendedCalendarDto calendars_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets calendars for current tenant.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.CalendarsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. The allowed functions are: allfunctions. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. The allowed properties are: Name, Id. (optional)
top = 56 # int | Limits the number of items returned from a collection. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets calendars for current tenant.
    api_response = api_instance.calendars_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CalendarsApi->calendars_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. The allowed functions are: allfunctions. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. The allowed properties are: Name, Id. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfExtendedCalendarDto**](ODataValueOfIEnumerableOfExtendedCalendarDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **calendars_get_by_id**
> ExtendedCalendarDto calendars_get_by_id(key, expand=expand, select=select)

Gets calendar based on its id.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.CalendarsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets calendar based on its id.
    api_response = api_instance.calendars_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CalendarsApi->calendars_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ExtendedCalendarDto**](ExtendedCalendarDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **calendars_post**
> ExtendedCalendarDto calendars_post(body=body)

Creates a new calendar.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: (Settings.Create).

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
api_instance = uipath_orchestrator_rest.CalendarsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.ExtendedCalendarDto() # ExtendedCalendarDto |  (optional)

try:
    # Creates a new calendar.
    api_response = api_instance.calendars_post(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CalendarsApi->calendars_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ExtendedCalendarDto**](ExtendedCalendarDto.md)|  | [optional] 

### Return type

[**ExtendedCalendarDto**](ExtendedCalendarDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **calendars_put_by_id**
> ExtendedCalendarDto calendars_put_by_id(key, body=body)

Edits a calendar.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: (Settings.Edit).

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
api_instance = uipath_orchestrator_rest.CalendarsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
body = uipath_orchestrator_rest.ExtendedCalendarDto() # ExtendedCalendarDto |  (optional)

try:
    # Edits a calendar.
    api_response = api_instance.calendars_put_by_id(key, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CalendarsApi->calendars_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **body** | [**ExtendedCalendarDto**](ExtendedCalendarDto.md)|  | [optional] 

### Return type

[**ExtendedCalendarDto**](ExtendedCalendarDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

