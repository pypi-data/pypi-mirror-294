# uipath_orchestrator_rest.AlertsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**alerts_get**](AlertsApi.md#alerts_get) | **GET** /odata/Alerts | Gets alerts.
[**alerts_get_unread_count**](AlertsApi.md#alerts_get_unread_count) | **GET** /odata/Alerts/UiPath.Server.Configuration.OData.GetUnreadCount | Returns the total number of alerts, per tenant, that haven&#39;t been read by the current user.
[**alerts_mark_as_read**](AlertsApi.md#alerts_mark_as_read) | **POST** /odata/Alerts/UiPath.Server.Configuration.OData.MarkAsRead | Marks alerts as read and returns the remaining number of unread notifications.
[**alerts_raise_process_alert**](AlertsApi.md#alerts_raise_process_alert) | **POST** /odata/Alerts/UiPath.Server.Configuration.OData.RaiseProcessAlert | Creates a Process Alert


# **alerts_get**
> ODataValueOfIEnumerableOfAlertDto alerts_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets alerts.

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: Alerts.View. DEPRECATED:  Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.AlertsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets alerts.
    api_response = api_instance.alerts_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertsApi->alerts_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfAlertDto**](ODataValueOfIEnumerableOfAlertDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **alerts_get_unread_count**
> ODataValueOfInt64 alerts_get_unread_count(expand=expand, select=select)

Returns the total number of alerts, per tenant, that haven't been read by the current user.

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: Alerts.View. DEPRECATED:  Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.AlertsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Returns the total number of alerts, per tenant, that haven't been read by the current user.
    api_response = api_instance.alerts_get_unread_count(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertsApi->alerts_get_unread_count: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **alerts_mark_as_read**
> ODataValueOfInt64 alerts_mark_as_read(body=body, expand=expand, select=select)

Marks alerts as read and returns the remaining number of unread notifications.

OAuth required scopes: OR.Monitoring or OR.Monitoring.Write.  Required permissions: Alerts.View. DEPRECATED:  Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.AlertsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.AlertsMarkAsReadRequest() # AlertsMarkAsReadRequest | Collection containing the unique identifiers of the notifications that will be marked as read (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Marks alerts as read and returns the remaining number of unread notifications.
    api_response = api_instance.alerts_mark_as_read(body=body, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertsApi->alerts_mark_as_read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AlertsMarkAsReadRequest**](AlertsMarkAsReadRequest.md)| Collection containing the unique identifiers of the notifications that will be marked as read | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfInt64**](ODataValueOfInt64.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **alerts_raise_process_alert**
> alerts_raise_process_alert(body=body)

Creates a Process Alert

OAuth required scopes: OR.Monitoring or OR.Monitoring.Write.  Required permissions: Alerts.Create. DEPRECATED:  Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.AlertsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.RaiseProcessAlertRequest() # RaiseProcessAlertRequest |  (optional)

try:
    # Creates a Process Alert
    api_instance.alerts_raise_process_alert(body=body)
except ApiException as e:
    print("Exception when calling AlertsApi->alerts_raise_process_alert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RaiseProcessAlertRequest**](RaiseProcessAlertRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

