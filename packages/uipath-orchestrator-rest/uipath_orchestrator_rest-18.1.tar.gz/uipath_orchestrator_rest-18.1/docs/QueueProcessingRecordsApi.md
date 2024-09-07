# uipath_orchestrator_rest.QueueProcessingRecordsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**queue_processing_records_retrieve_last_days_processing_records_by_daysno_and_queuedefinitionid**](QueueProcessingRecordsApi.md#queue_processing_records_retrieve_last_days_processing_records_by_daysno_and_queuedefinitionid) | **GET** /odata/QueueProcessingRecords/UiPathODataSvc.RetrieveLastDaysProcessingRecords(daysNo&#x3D;{daysNo},queueDefinitionId&#x3D;{queueDefinitionId}) | Returns the computed processing status for a given queue in the last specified days.
[**queue_processing_records_retrieve_queues_processing_status**](QueueProcessingRecordsApi.md#queue_processing_records_retrieve_queues_processing_status) | **GET** /odata/QueueProcessingRecords/UiPathODataSvc.RetrieveQueuesProcessingStatus | Returns the processing status for all queues. Allows odata query options.


# **queue_processing_records_retrieve_last_days_processing_records_by_daysno_and_queuedefinitionid**
> ODataValueOfIEnumerableOfQueueProcessingRecordDto queue_processing_records_retrieve_last_days_processing_records_by_daysno_and_queuedefinitionid(days_no, queue_definition_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns the computed processing status for a given queue in the last specified days.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View and Transactions.View.

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
api_instance = uipath_orchestrator_rest.QueueProcessingRecordsApi(uipath_orchestrator_rest.ApiClient(configuration))
days_no = 56 # int | The number of days to go back from the present moment when calculating the report. If it is 0 the report will be computed for the last hour.
queue_definition_id = 789 # int | The Id of the queue for which the report is computed.
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns the computed processing status for a given queue in the last specified days.
    api_response = api_instance.queue_processing_records_retrieve_last_days_processing_records_by_daysno_and_queuedefinitionid(days_no, queue_definition_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueProcessingRecordsApi->queue_processing_records_retrieve_last_days_processing_records_by_daysno_and_queuedefinitionid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **days_no** | **int**| The number of days to go back from the present moment when calculating the report. If it is 0 the report will be computed for the last hour. | 
 **queue_definition_id** | **int**| The Id of the queue for which the report is computed. | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ODataValueOfIEnumerableOfQueueProcessingRecordDto**](ODataValueOfIEnumerableOfQueueProcessingRecordDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_processing_records_retrieve_queues_processing_status**
> ODataValueOfIEnumerableOfQueueProcessingStatusDto queue_processing_records_retrieve_queues_processing_status(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Returns the processing status for all queues. Allows odata query options.

OAuth required scopes: OR.Queues or OR.Queues.Read.  Required permissions: Queues.View.

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
api_instance = uipath_orchestrator_rest.QueueProcessingRecordsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Returns the processing status for all queues. Allows odata query options.
    api_response = api_instance.queue_processing_records_retrieve_queues_processing_status(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueProcessingRecordsApi->queue_processing_records_retrieve_queues_processing_status: %s\n" % e)
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

[**ODataValueOfIEnumerableOfQueueProcessingStatusDto**](ODataValueOfIEnumerableOfQueueProcessingStatusDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

