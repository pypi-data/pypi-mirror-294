# uipath_orchestrator_rest.JobTriggersApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**job_triggers_deliver_payload_by_inboxid**](JobTriggersApi.md#job_triggers_deliver_payload_by_inboxid) | **POST** /api/JobTriggers/DeliverPayload/{inboxId} | Deliver payload for trigger inboxId.
[**job_triggers_get**](JobTriggersApi.md#job_triggers_get) | **GET** /odata/JobTriggers | Gets JobTriggers.
[**job_triggers_get_payload_by_inboxid**](JobTriggersApi.md#job_triggers_get_payload_by_inboxid) | **GET** /api/JobTriggers/GetPayload/{inboxId} | Get payload for trigger inboxId.
[**job_triggers_get_with_wait_events_by_jobid**](JobTriggersApi.md#job_triggers_get_with_wait_events_by_jobid) | **GET** /odata/JobTriggers/UiPath.Server.Configuration.OData.GetWithWaitEvents(jobId&#x3D;{jobId}) | Gets Trigger option for a job instance along with wait event details    .


# **job_triggers_deliver_payload_by_inboxid**
> job_triggers_deliver_payload_by_inboxid(inbox_id, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Deliver payload for trigger inboxId.

OAuth required scopes: OR.Jobs or OR.Jobs.Write.  Required permissions: Jobs.Edit.

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
api_instance = uipath_orchestrator_rest.JobTriggersApi(uipath_orchestrator_rest.ApiClient(configuration))
inbox_id = 'inbox_id_example' # str | 
body = 'body_example' # str |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Deliver payload for trigger inboxId.
    api_instance.job_triggers_deliver_payload_by_inboxid(inbox_id, body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling JobTriggersApi->job_triggers_deliver_payload_by_inboxid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **inbox_id** | [**str**](.md)|  | 
 **body** | **str**|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **job_triggers_get**
> ODataValueOfIEnumerableOfJobTriggerDto job_triggers_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets JobTriggers.

OAuth required scopes: OR.Jobs or OR.Jobs.Read.  Required permissions: Jobs.View.

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
api_instance = uipath_orchestrator_rest.JobTriggersApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets JobTriggers.
    api_response = api_instance.job_triggers_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobTriggersApi->job_triggers_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfJobTriggerDto**](ODataValueOfIEnumerableOfJobTriggerDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **job_triggers_get_payload_by_inboxid**
> str job_triggers_get_payload_by_inboxid(inbox_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get payload for trigger inboxId.

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.JobTriggersApi()
inbox_id = 'inbox_id_example' # str | 
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get payload for trigger inboxId.
    api_response = api_instance.job_triggers_get_payload_by_inboxid(inbox_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobTriggersApi->job_triggers_get_payload_by_inboxid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **inbox_id** | [**str**](.md)|  | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **job_triggers_get_with_wait_events_by_jobid**
> ODataValueOfIEnumerableOfJobTriggerWithWaitEventsDto job_triggers_get_with_wait_events_by_jobid(job_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Gets Trigger option for a job instance along with wait event details    .

OAuth required scopes: OR.Jobs or OR.Jobs.Read.  Required permissions: Jobs.View.

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
api_instance = uipath_orchestrator_rest.JobTriggersApi(uipath_orchestrator_rest.ApiClient(configuration))
job_id = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Gets Trigger option for a job instance along with wait event details    .
    api_response = api_instance.job_triggers_get_with_wait_events_by_jobid(job_id, expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobTriggersApi->job_triggers_get_with_wait_events_by_jobid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **top** | **int**| Limits the number of items returned from a collection. The maximum value is 1000. | [optional] 
 **skip** | **int**| Excludes the specified number of items of the queried collection from the result. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfJobTriggerWithWaitEventsDto**](ODataValueOfIEnumerableOfJobTriggerWithWaitEventsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

