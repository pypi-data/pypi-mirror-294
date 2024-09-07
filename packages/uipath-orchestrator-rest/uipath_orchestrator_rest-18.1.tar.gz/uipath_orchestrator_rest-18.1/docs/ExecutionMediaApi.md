# uipath_orchestrator_rest.ExecutionMediaApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**execution_media_delete_media_by_job_id**](ExecutionMediaApi.md#execution_media_delete_media_by_job_id) | **POST** /odata/ExecutionMedia/UiPath.Server.Configuration.OData.DeleteMediaByJobId | Deletes the execution media for the given job key.
[**execution_media_download_media_by_job_id**](ExecutionMediaApi.md#execution_media_download_media_by_job_id) | **GET** /odata/ExecutionMedia/UiPath.Server.Configuration.OData.DownloadMediaByJobId(jobId&#x3D;{jobId}) | Downloads execution media by job id
[**execution_media_get**](ExecutionMediaApi.md#execution_media_get) | **GET** /odata/ExecutionMedia | 
[**execution_media_get_by_id**](ExecutionMediaApi.md#execution_media_get_by_id) | **GET** /odata/ExecutionMedia({key}) | Get by id


# **execution_media_delete_media_by_job_id**
> execution_media_delete_media_by_job_id(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Deletes the execution media for the given job key.

OAuth required scopes: OR.Monitoring or OR.Monitoring.Write.  Required permissions: ExecutionMedia.Delete.

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
api_instance = uipath_orchestrator_rest.ExecutionMediaApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.ExecutionMediaDeleteMediaByJobIdRequest() # ExecutionMediaDeleteMediaByJobIdRequest |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Deletes the execution media for the given job key.
    api_instance.execution_media_delete_media_by_job_id(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling ExecutionMediaApi->execution_media_delete_media_by_job_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ExecutionMediaDeleteMediaByJobIdRequest**](ExecutionMediaDeleteMediaByJobIdRequest.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execution_media_download_media_by_job_id**
> file execution_media_download_media_by_job_id(job_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Downloads execution media by job id

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: ExecutionMedia.View.

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
api_instance = uipath_orchestrator_rest.ExecutionMediaApi(uipath_orchestrator_rest.ApiClient(configuration))
job_id = 789 # int | 
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Downloads execution media by job id
    api_response = api_instance.execution_media_download_media_by_job_id(job_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExecutionMediaApi->execution_media_download_media_by_job_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **int**|  | 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**file**](file.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execution_media_get**
> ODataValueOfIEnumerableOfExecutionMediaDto execution_media_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)



OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: ExecutionMedia.View.

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
api_instance = uipath_orchestrator_rest.ExecutionMediaApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    api_response = api_instance.execution_media_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExecutionMediaApi->execution_media_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfExecutionMediaDto**](ODataValueOfIEnumerableOfExecutionMediaDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execution_media_get_by_id**
> ExecutionMediaDto execution_media_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get by id

OAuth required scopes: OR.Monitoring or OR.Monitoring.Read.  Required permissions: ExecutionMedia.View.

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
api_instance = uipath_orchestrator_rest.ExecutionMediaApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 789 # int | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get by id
    api_response = api_instance.execution_media_get_by_id(key, expand=expand, select=select, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExecutionMediaApi->execution_media_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **int**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**ExecutionMediaDto**](ExecutionMediaDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

