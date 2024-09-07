# uipath_orchestrator_rest.PackageFeedsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**package_feeds_get_folder_feed**](PackageFeedsApi.md#package_feeds_get_folder_feed) | **GET** /api/PackageFeeds/GetFolderFeed | Returns the feed id for a user assigned folder having specific feed


# **package_feeds_get_folder_feed**
> str package_feeds_get_folder_feed(folder_id=folder_id)

Returns the feed id for a user assigned folder having specific feed

OAuth required scopes: OR.Execution or OR.Execution.Read.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.PackageFeedsApi(uipath_orchestrator_rest.ApiClient(configuration))
folder_id = 789 # int |  (optional)

try:
    # Returns the feed id for a user assigned folder having specific feed
    api_response = api_instance.package_feeds_get_folder_feed(folder_id=folder_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackageFeedsApi->package_feeds_get_folder_feed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **folder_id** | **int**|  | [optional] 

### Return type

**str**

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

