# uipath_orchestrator_rest.AuditLogsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**audit_logs_export**](AuditLogsApi.md#audit_logs_export) | **POST** /odata/AuditLogs/UiPath.Server.Configuration.OData.Export | Requests a CSV export of filtered items.
[**audit_logs_get**](AuditLogsApi.md#audit_logs_get) | **GET** /odata/AuditLogs | Gets Audit logs.
[**audit_logs_get_audit_log_details_by_auditlogid**](AuditLogsApi.md#audit_logs_get_audit_log_details_by_auditlogid) | **GET** /odata/AuditLogs/UiPath.Server.Configuration.OData.GetAuditLogDetails(auditLogId&#x3D;{auditLogId}) | Returns audit log details by audit log id


# **audit_logs_export**
> ExportModel audit_logs_export(audited_service=audited_service, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Requests a CSV export of filtered items.

OAuth required scopes: OR.Audit or OR.Audit.Write.  Required permissions: Audit.View.

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
api_instance = uipath_orchestrator_rest.AuditLogsApi(uipath_orchestrator_rest.ApiClient(configuration))
audited_service = 'Orchestrator' # str |  (optional) (default to Orchestrator)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Requests a CSV export of filtered items.
    api_response = api_instance.audit_logs_export(audited_service=audited_service, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditLogsApi->audit_logs_export: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audited_service** | **str**|  | [optional] [default to Orchestrator]
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ExportModel**](ExportModel.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_logs_get**
> ODataValueOfIEnumerableOfAuditLogDto audit_logs_get(x_uipath_audited_service=x_uipath_audited_service, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets Audit logs.

OAuth required scopes: OR.Audit or OR.Audit.Read.  Required permissions: Audit.View.

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
api_instance = uipath_orchestrator_rest.AuditLogsApi(uipath_orchestrator_rest.ApiClient(configuration))
x_uipath_audited_service = 'Orchestrator' # str |  (optional) (default to Orchestrator)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets Audit logs.
    api_response = api_instance.audit_logs_get(x_uipath_audited_service=x_uipath_audited_service, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditLogsApi->audit_logs_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_uipath_audited_service** | **str**|  | [optional] [default to Orchestrator]
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfAuditLogDto**](ODataValueOfIEnumerableOfAuditLogDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_logs_get_audit_log_details_by_auditlogid**
> ODataValueOfIEnumerableOfAuditLogEntityDto audit_logs_get_audit_log_details_by_auditlogid(audit_log_id, x_uipath_audited_service=x_uipath_audited_service, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Returns audit log details by audit log id

OAuth required scopes: OR.Audit or OR.Audit.Read.  Required permissions: Audit.View.

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
api_instance = uipath_orchestrator_rest.AuditLogsApi(uipath_orchestrator_rest.ApiClient(configuration))
audit_log_id = 789 # int | 
x_uipath_audited_service = 'Orchestrator' # str |  (optional) (default to Orchestrator)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Returns audit log details by audit log id
    api_response = api_instance.audit_logs_get_audit_log_details_by_auditlogid(audit_log_id, x_uipath_audited_service=x_uipath_audited_service, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditLogsApi->audit_logs_get_audit_log_details_by_auditlogid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audit_log_id** | **int**|  | 
 **x_uipath_audited_service** | **str**|  | [optional] [default to Orchestrator]
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfAuditLogEntityDto**](ODataValueOfIEnumerableOfAuditLogEntityDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

