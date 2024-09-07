# uipath_orchestrator_rest.TestAutomationApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_automation_cancel_test_case_execution**](TestAutomationApi.md#test_automation_cancel_test_case_execution) | **POST** /api/TestAutomation/CancelTestCaseExecution | Cancels the specified test case execution.
[**test_automation_cancel_test_set_execution**](TestAutomationApi.md#test_automation_cancel_test_set_execution) | **POST** /api/TestAutomation/CancelTestSetExecution | Cancels the specified test set execution.
[**test_automation_create_test_set_for_release_version**](TestAutomationApi.md#test_automation_create_test_set_for_release_version) | **POST** /api/TestAutomation/CreateTestSetForReleaseVersion | This will create a test set with source type API.This endpoint it is supposed to be used by API integration.
[**test_automation_get_assertion_screenshot**](TestAutomationApi.md#test_automation_get_assertion_screenshot) | **GET** /api/TestAutomation/GetAssertionScreenshot | Get the screenshot for the specified test case assertion.
[**test_automation_get_package_info_by_test_case_unique_id**](TestAutomationApi.md#test_automation_get_package_info_by_test_case_unique_id) | **GET** /api/TestAutomation/GetPackageInfoByTestCaseUniqueId | Get the package identifier and the latest version for the specified test case.
[**test_automation_get_releases_for_package_version**](TestAutomationApi.md#test_automation_get_releases_for_package_version) | **GET** /api/TestAutomation/GetReleasesForPackageVersion | This will list all the processes filtered by package identifier and version cross-folder when no current folder is sent by header.
[**test_automation_get_test_case_execution_attachment**](TestAutomationApi.md#test_automation_get_test_case_execution_attachment) | **GET** /api/TestAutomation/GetTestCaseExecutionAttachment | Get the attachment for the specified test case execution attachment.
[**test_automation_get_test_case_execution_attachments**](TestAutomationApi.md#test_automation_get_test_case_execution_attachments) | **POST** /api/TestAutomation/GetTestCaseExecutionAttachments | This will list all test case execution attachments filtered by identifier and tags
[**test_automation_get_test_set_execution_attachment**](TestAutomationApi.md#test_automation_get_test_set_execution_attachment) | **GET** /api/TestAutomation/GetTestSetExecutionAttachment | Get the attachment for the specified test set execution attachment.
[**test_automation_get_test_set_execution_attachments**](TestAutomationApi.md#test_automation_get_test_set_execution_attachments) | **POST** /api/TestAutomation/GetTestSetExecutionAttachments | This will list all test set execution attachments filtered by identifier and tags
[**test_automation_reexecute_test_cases**](TestAutomationApi.md#test_automation_reexecute_test_cases) | **POST** /api/TestAutomation/ReexecuteTestCases | Re-execute the specified test case executions within the same test set execution.
[**test_automation_start_test_set_execution**](TestAutomationApi.md#test_automation_start_test_set_execution) | **POST** /api/TestAutomation/StartTestSetExecution | Start a test set execution.
[**test_automation_start_test_set_execution_with_options**](TestAutomationApi.md#test_automation_start_test_set_execution_with_options) | **POST** /api/TestAutomation/StartTestSetExecutionWithOptions | Start a test set execution with additional options.


# **test_automation_cancel_test_case_execution**
> test_automation_cancel_test_case_execution(test_case_execution_id=test_case_execution_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Cancels the specified test case execution.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Write.  Required permissions: TestSetExecutions.Edit.  Responses:  202 Accepted  403 If the caller doesn't have permissions to cancel a test set execution

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
test_case_execution_id = 789 # int | Id for the test case execution to be canceled (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Cancels the specified test case execution.
    api_instance.test_automation_cancel_test_case_execution(test_case_execution_id=test_case_execution_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_cancel_test_case_execution: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_case_execution_id** | **int**| Id for the test case execution to be canceled | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_cancel_test_set_execution**
> test_automation_cancel_test_set_execution(test_set_execution_id=test_set_execution_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Cancels the specified test set execution.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Write.  Required permissions: TestSetExecutions.Edit.  Responses:  202 Accepted  403 If the caller doesn't have permissions to cancel a test set execution

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
test_set_execution_id = 789 # int | Id for the test set execution to be canceled (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Cancels the specified test set execution.
    api_instance.test_automation_cancel_test_set_execution(test_set_execution_id=test_set_execution_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_cancel_test_set_execution: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_set_execution_id** | **int**| Id for the test set execution to be canceled | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_create_test_set_for_release_version**
> int test_automation_create_test_set_for_release_version(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

This will create a test set with source type API.This endpoint it is supposed to be used by API integration.

OAuth required scopes: OR.TestSets or OR.TestSets.Write.  Required permissions: TestSets.Create.  Responses:  201 Created returns test set Id  403 If the caller doesn't have permissions to create a test set

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.BuildTestSetRequestMessage() # BuildTestSetRequestMessage |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # This will create a test set with source type API.This endpoint it is supposed to be used by API integration.
    api_response = api_instance.test_automation_create_test_set_for_release_version(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_create_test_set_for_release_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BuildTestSetRequestMessage**](BuildTestSetRequestMessage.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

**int**

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_get_assertion_screenshot**
> file test_automation_get_assertion_screenshot(test_case_assertion_id=test_case_assertion_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get the screenshot for the specified test case assertion.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Read.  Required permissions: TestSetExecutions.View.  Responses:  200 OK  404 If the test case assertion is not found or the screenshot storage location is not found

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
test_case_assertion_id = 789 # int | Id of the test case assertion (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get the screenshot for the specified test case assertion.
    api_response = api_instance.test_automation_get_assertion_screenshot(test_case_assertion_id=test_case_assertion_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_get_assertion_screenshot: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_case_assertion_id** | **int**| Id of the test case assertion | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**file**](file.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_get_package_info_by_test_case_unique_id**
> TestPackageInfoDto test_automation_get_package_info_by_test_case_unique_id(test_case_unique_id=test_case_unique_id, package_identifier=package_identifier)

Get the package identifier and the latest version for the specified test case.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Requires authentication.  Responses:  200 OK  403 If the caller doesn't have permissions to retrieve packages  404 If there is no test case with the specified UniqueId

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
test_case_unique_id = 'test_case_unique_id_example' # str |  (optional)
package_identifier = 'package_identifier_example' # str |  (optional)

try:
    # Get the package identifier and the latest version for the specified test case.
    api_response = api_instance.test_automation_get_package_info_by_test_case_unique_id(test_case_unique_id=test_case_unique_id, package_identifier=package_identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_get_package_info_by_test_case_unique_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_case_unique_id** | [**str**](.md)|  | [optional] 
 **package_identifier** | **str**|  | [optional] 

### Return type

[**TestPackageInfoDto**](TestPackageInfoDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_get_releases_for_package_version**
> list[TestReleaseVersionDto] test_automation_get_releases_for_package_version(package_identifier=package_identifier, version=version, mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

This will list all the processes filtered by package identifier and version cross-folder when no current folder is sent by header.

OAuth required scopes: OR.Execution or OR.Execution.Read.  Required permissions: Processes.View.  Responses:  200 OK  404 If there is no release for the specified package identifier

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
package_identifier = 'package_identifier_example' # str |  (optional)
version = 'version_example' # str |  (optional)
mandatory_permissions = ['mandatory_permissions_example'] # list[str] | If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; all permissions in this set must be met (optional)
at_least_one_permissions = ['at_least_one_permissions_example'] # list[str] | If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; at least one permission in this set must be met (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # This will list all the processes filtered by package identifier and version cross-folder when no current folder is sent by header.
    api_response = api_instance.test_automation_get_releases_for_package_version(package_identifier=package_identifier, version=version, mandatory_permissions=mandatory_permissions, at_least_one_permissions=at_least_one_permissions, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_get_releases_for_package_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_identifier** | **str**|  | [optional] 
 **version** | **str**|  | [optional] 
 **mandatory_permissions** | [**list[str]**](str.md)| If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; all permissions in this set must be met | [optional] 
 **at_least_one_permissions** | [**list[str]**](str.md)| If in a cross-folder scenario, these represent the additional permissions              required in the folders the data is retrieved from; at least one permission in this set must be met | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**list[TestReleaseVersionDto]**](TestReleaseVersionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_get_test_case_execution_attachment**
> file test_automation_get_test_case_execution_attachment(test_case_execution_attachment_id=test_case_execution_attachment_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get the attachment for the specified test case execution attachment.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Read.  Required permissions: TestSetExecutions.View.  Responses:  200 OK  404 If the test case execution attachment is not found or the storage location is not found

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
test_case_execution_attachment_id = 789 # int | Id of the test case execution attachment (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get the attachment for the specified test case execution attachment.
    api_response = api_instance.test_automation_get_test_case_execution_attachment(test_case_execution_attachment_id=test_case_execution_attachment_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_get_test_case_execution_attachment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_case_execution_attachment_id** | **int**| Id of the test case execution attachment | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**file**](file.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_get_test_case_execution_attachments**
> list[TestCaseExecutionAttachmentDto] test_automation_get_test_case_execution_attachments(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

This will list all test case execution attachments filtered by identifier and tags

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Write.  Required permissions: TestSetExecutions.View.  Responses:  200 OK  404 If there is no test case execution for the specified identifier

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestCaseExecutionAttachmentFilterDto() # TestCaseExecutionAttachmentFilterDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # This will list all test case execution attachments filtered by identifier and tags
    api_response = api_instance.test_automation_get_test_case_execution_attachments(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_get_test_case_execution_attachments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestCaseExecutionAttachmentFilterDto**](TestCaseExecutionAttachmentFilterDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**list[TestCaseExecutionAttachmentDto]**](TestCaseExecutionAttachmentDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_get_test_set_execution_attachment**
> file test_automation_get_test_set_execution_attachment(test_set_execution_attachment_id=test_set_execution_attachment_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Get the attachment for the specified test set execution attachment.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Read.  Required permissions: TestSetExecutions.View.  Responses:  200 OK  404 If the test set execution attachment is not found or the storage location is not found

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
test_set_execution_attachment_id = 789 # int | Id of the test set execution attachment (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Get the attachment for the specified test set execution attachment.
    api_response = api_instance.test_automation_get_test_set_execution_attachment(test_set_execution_attachment_id=test_set_execution_attachment_id, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_get_test_set_execution_attachment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_set_execution_attachment_id** | **int**| Id of the test set execution attachment | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**file**](file.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_get_test_set_execution_attachments**
> list[TestSetExecutionAttachmentDto] test_automation_get_test_set_execution_attachments(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

This will list all test set execution attachments filtered by identifier and tags

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Write.  Required permissions: TestSetExecutions.View.  Responses:  200 OK  404 If there is no test set execution for the specified identifier

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestSetExecutionAttachmentFilterDto() # TestSetExecutionAttachmentFilterDto |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # This will list all test set execution attachments filtered by identifier and tags
    api_response = api_instance.test_automation_get_test_set_execution_attachments(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_get_test_set_execution_attachments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestSetExecutionAttachmentFilterDto**](TestSetExecutionAttachmentFilterDto.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**list[TestSetExecutionAttachmentDto]**](TestSetExecutionAttachmentDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_reexecute_test_cases**
> list[TestCaseExecutionDto] test_automation_reexecute_test_cases(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Re-execute the specified test case executions within the same test set execution.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Write.  Required permissions: TestSetExecutions.Create.  Responses:  200 OK  403 If the caller doesn't have permissions to execute test sets  404 If one or more test cases were not found

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.ReexecuteTestCasesOptionsDto() # ReexecuteTestCasesOptionsDto | A list of test case executions with corresponding input arguments and optional RobotId and MachineSessionId fields (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Re-execute the specified test case executions within the same test set execution.
    api_response = api_instance.test_automation_reexecute_test_cases(body=body, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_reexecute_test_cases: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReexecuteTestCasesOptionsDto**](ReexecuteTestCasesOptionsDto.md)| A list of test case executions with corresponding input arguments and optional RobotId and MachineSessionId fields | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

[**list[TestCaseExecutionDto]**](TestCaseExecutionDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_start_test_set_execution**
> int test_automation_start_test_set_execution(test_set_id=test_set_id, test_set_key=test_set_key, trigger_type=trigger_type, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Start a test set execution.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Write.  Required permissions: TestSetExecutions.Create.  Responses:  200 OK returns test set execution Id  403 If the caller doesn't have permissions to execute a test set  404 If the test set was not found

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
test_set_id = 789 # int |  (optional)
test_set_key = 'test_set_key_example' # str |  (optional)
trigger_type = 'Manual' # str | Specifies how was the execution triggered (optional) (default to Manual)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Start a test set execution.
    api_response = api_instance.test_automation_start_test_set_execution(test_set_id=test_set_id, test_set_key=test_set_key, trigger_type=trigger_type, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_start_test_set_execution: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_set_id** | **int**|  | [optional] 
 **test_set_key** | [**str**](.md)|  | [optional] 
 **trigger_type** | **str**| Specifies how was the execution triggered | [optional] [default to Manual]
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

**int**

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_automation_start_test_set_execution_with_options**
> int test_automation_start_test_set_execution_with_options(body=body, test_set_id=test_set_id, test_set_key=test_set_key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)

Start a test set execution with additional options.

OAuth required scopes: OR.TestSetExecutions or OR.TestSetExecutions.Write.  Required permissions: TestSetExecutions.Create.  Responses:  200 OK returns test set execution Id  403 If the caller doesn't have permissions to execute a test set  404 If the test set was not found

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
api_instance = uipath_orchestrator_rest.TestAutomationApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.TestSetExecutionOptionsDto() # TestSetExecutionOptionsDto | Provides options to set the BatchExecutionKey and TriggerType and override the input parameters for specific test cases (optional)
test_set_id = 789 # int |  (optional)
test_set_key = 'test_set_key_example' # str |  (optional)
x_uipath_organization_unit_id = 789 # int | Folder/OrganizationUnit Id (optional)

try:
    # Start a test set execution with additional options.
    api_response = api_instance.test_automation_start_test_set_execution_with_options(body=body, test_set_id=test_set_id, test_set_key=test_set_key, x_uipath_organization_unit_id=x_uipath_organization_unit_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestAutomationApi->test_automation_start_test_set_execution_with_options: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestSetExecutionOptionsDto**](TestSetExecutionOptionsDto.md)| Provides options to set the BatchExecutionKey and TriggerType and override the input parameters for specific test cases | [optional] 
 **test_set_id** | **int**|  | [optional] 
 **test_set_key** | [**str**](.md)|  | [optional] 
 **x_uipath_organization_unit_id** | **int**| Folder/OrganizationUnit Id | [optional] 

### Return type

**int**

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

