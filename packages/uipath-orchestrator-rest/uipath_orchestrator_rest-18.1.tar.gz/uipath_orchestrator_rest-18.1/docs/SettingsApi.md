# uipath_orchestrator_rest.SettingsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**settings_activate_license_offline**](SettingsApi.md#settings_activate_license_offline) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.ActivateLicenseOffline | Uploads a new offline license activation.  The content of the license is sent as a file embedded in the HTTP request.
[**settings_activate_license_online**](SettingsApi.md#settings_activate_license_online) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.ActivateLicenseOnline | Activate the license for a specific tenant
[**settings_deactivate_license_online**](SettingsApi.md#settings_deactivate_license_online) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.DeactivateLicenseOnline | Deactivate the license for a specific tenant
[**settings_delete_bulk**](SettingsApi.md#settings_delete_bulk) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.DeleteBulk | Deletes values for the specified settings in the Tenant scope.
[**settings_delete_license**](SettingsApi.md#settings_delete_license) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.DeleteLicense | Removes the license
[**settings_get**](SettingsApi.md#settings_get) | **GET** /odata/Settings | Gets the settings.
[**settings_get_activity_settings**](SettingsApi.md#settings_get_activity_settings) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetActivitySettings | Returns Orchestrator settings used by activities
[**settings_get_authentication_settings**](SettingsApi.md#settings_get_authentication_settings) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetAuthenticationSettings | Gets the authentication settings
[**settings_get_by_id**](SettingsApi.md#settings_get_by_id) | **GET** /odata/Settings({key}) | Gets a settings value based on its key.
[**settings_get_calendar**](SettingsApi.md#settings_get_calendar) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetCalendar | Gets custom calendar, with excluded dates in UTC, for current tenant
[**settings_get_connection_string**](SettingsApi.md#settings_get_connection_string) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetConnectionString | Gets the connection string
[**settings_get_deactivate_license_offline**](SettingsApi.md#settings_get_deactivate_license_offline) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.GetDeactivateLicenseOffline | Deactivate the license offline for a specific tenant
[**settings_get_execution_settings_configuration_by_scope**](SettingsApi.md#settings_get_execution_settings_configuration_by_scope) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetExecutionSettingsConfiguration(scope&#x3D;{scope}) | Gets the execution settings configuration (display name, value type, etc.).  If scope is 0 (Global), the default values will be the initial ones. If scope is 1 (Robot), then  the default values will be the actual values set globally.  e.g., Resolution width  Assume it was set globally to 720.  Then within the config returned by this function, the default value for this setting will be:  - 0 for scope &#x3D; 0 and  - 720 for scope &#x3D; 1.
[**settings_get_languages**](SettingsApi.md#settings_get_languages) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetLanguages | Gets supported languages
[**settings_get_license**](SettingsApi.md#settings_get_license) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetLicense | Retrieves the current license information.
[**settings_get_license_offline**](SettingsApi.md#settings_get_license_offline) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.GetLicenseOffline | Create the offline activation request for a specific tenant
[**settings_get_secure_store_configuration_by_storetypename**](SettingsApi.md#settings_get_secure_store_configuration_by_storetypename) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetSecureStoreConfiguration(storeTypeName&#x3D;{storeTypeName}) | Gets the configuration format for a Secure store
[**settings_get_timezones**](SettingsApi.md#settings_get_timezones) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetTimezones | Gets timezones.
[**settings_get_update_settings**](SettingsApi.md#settings_get_update_settings) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetUpdateSettings | Gets the update settings
[**settings_get_web_settings**](SettingsApi.md#settings_get_web_settings) | **GET** /odata/Settings/UiPath.Server.Configuration.OData.GetWebSettings | Returns a collection of key value pairs representing settings used by Orchestrator web client.
[**settings_put_by_id**](SettingsApi.md#settings_put_by_id) | **PUT** /odata/Settings({key}) | Edits a setting.
[**settings_set_calendar**](SettingsApi.md#settings_set_calendar) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.SetCalendar | Sets custom calendar, with excluded dates in UTC, for current tenant
[**settings_update_bulk**](SettingsApi.md#settings_update_bulk) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.UpdateBulk | Updates the current settings.
[**settings_update_license_online**](SettingsApi.md#settings_update_license_online) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.UpdateLicenseOnline | Update the license for a specific tenant
[**settings_update_user_setting**](SettingsApi.md#settings_update_user_setting) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.UpdateUserSetting | Edits a user setting.
[**settings_upload_license**](SettingsApi.md#settings_upload_license) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.UploadLicense | Uploads a new license file that was previously generated with Regutil. The content of the license is sent as a file embedded in the HTTP request.
[**settings_verify_smtp_setting**](SettingsApi.md#settings_verify_smtp_setting) | **POST** /odata/Settings/UiPath.Server.Configuration.OData.VerifySmtpSetting | Verify whether the given SMTP settings are correct or not by sending an email to a recipient.


# **settings_activate_license_offline**
> settings_activate_license_offline(file)

Uploads a new offline license activation.  The content of the license is sent as a file embedded in the HTTP request.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Create or License.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
file = '/path/to/file.txt' # file | 

try:
    # Uploads a new offline license activation.  The content of the license is sent as a file embedded in the HTTP request.
    api_instance.settings_activate_license_offline(file)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_activate_license_offline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_activate_license_online**
> settings_activate_license_online(body=body)

Activate the license for a specific tenant

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Create or License.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.LicenseRequest() # LicenseRequest |  (optional)

try:
    # Activate the license for a specific tenant
    api_instance.settings_activate_license_online(body=body)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_activate_license_online: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LicenseRequest**](LicenseRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_deactivate_license_online**
> settings_deactivate_license_online()

Deactivate the license for a specific tenant

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Delete.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Deactivate the license for a specific tenant
    api_instance.settings_deactivate_license_online()
except ApiException as e:
    print("Exception when calling SettingsApi->settings_deactivate_license_online: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_delete_bulk**
> settings_delete_bulk(body=body)

Deletes values for the specified settings in the Tenant scope.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Delete.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.SettingsDeleteBulkRequest() # SettingsDeleteBulkRequest | Settings - The collection of settings to be deleted. (optional)

try:
    # Deletes values for the specified settings in the Tenant scope.
    api_instance.settings_delete_bulk(body=body)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_delete_bulk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SettingsDeleteBulkRequest**](SettingsDeleteBulkRequest.md)| Settings - The collection of settings to be deleted. | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_delete_license**
> settings_delete_license()

Removes the license

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Delete.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Removes the license
    api_instance.settings_delete_license()
except ApiException as e:
    print("Exception when calling SettingsApi->settings_delete_license: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get**
> ODataValueOfIEnumerableOfSettingsDto settings_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)

Gets the settings.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
top = 56 # int | Limits the number of items returned from a collection. The maximum value is 1000. (optional)
skip = 56 # int | Excludes the specified number of items of the queried collection from the result. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets the settings.
    api_response = api_instance.settings_get(expand=expand, filter=filter, select=select, orderby=orderby, top=top, skip=skip, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get: %s\n" % e)
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

[**ODataValueOfIEnumerableOfSettingsDto**](ODataValueOfIEnumerableOfSettingsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_activity_settings**
> ActivitySettingsDto settings_get_activity_settings(expand=expand, select=select)

Returns Orchestrator settings used by activities

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Returns Orchestrator settings used by activities
    api_response = api_instance.settings_get_activity_settings(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_activity_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ActivitySettingsDto**](ActivitySettingsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_authentication_settings**
> ResponseDictionaryDto settings_get_authentication_settings(expand=expand, select=select)

Gets the authentication settings

OAuth required scopes: OR.Settings or OR.Settings.Read.

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.SettingsApi()
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets the authentication settings
    api_response = api_instance.settings_get_authentication_settings(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_authentication_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ResponseDictionaryDto**](ResponseDictionaryDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_by_id**
> ODataValueOfString settings_get_by_id(key, expand=expand, select=select)

Gets a settings value based on its key.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets a settings value based on its key.
    api_response = api_instance.settings_get_by_id(key, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfString**](ODataValueOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_calendar**
> CalendarDto settings_get_calendar(expand=expand, select=select)

Gets custom calendar, with excluded dates in UTC, for current tenant

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View. DEPRECATED:  This API is deprecated. Please do not use it any longer. Use /odata/Calendars instead. Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets custom calendar, with excluded dates in UTC, for current tenant
    api_response = api_instance.settings_get_calendar(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_calendar: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**CalendarDto**](CalendarDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_connection_string**
> ODataValueOfString settings_get_connection_string(expand=expand, select=select)

Gets the connection string

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets the connection string
    api_response = api_instance.settings_get_connection_string(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_connection_string: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfString**](ODataValueOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_deactivate_license_offline**
> ODataValueOfString settings_get_deactivate_license_offline(expand=expand, select=select)

Deactivate the license offline for a specific tenant

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Delete.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Deactivate the license offline for a specific tenant
    api_response = api_instance.settings_get_deactivate_license_offline(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_deactivate_license_offline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfString**](ODataValueOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_execution_settings_configuration_by_scope**
> ExecutionSettingsConfiguration settings_get_execution_settings_configuration_by_scope(scope, expand=expand, select=select)

Gets the execution settings configuration (display name, value type, etc.).  If scope is 0 (Global), the default values will be the initial ones. If scope is 1 (Robot), then  the default values will be the actual values set globally.  e.g., Resolution width  Assume it was set globally to 720.  Then within the config returned by this function, the default value for this setting will be:  - 0 for scope = 0 and  - 720 for scope = 1.

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.Edit or Robots.Create or Robots.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
scope = 56 # int | Scope of the configuration; 0 for Global, 1 for Robot
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets the execution settings configuration (display name, value type, etc.).  If scope is 0 (Global), the default values will be the initial ones. If scope is 1 (Robot), then  the default values will be the actual values set globally.  e.g., Resolution width  Assume it was set globally to 720.  Then within the config returned by this function, the default value for this setting will be:  - 0 for scope = 0 and  - 720 for scope = 1.
    api_response = api_instance.settings_get_execution_settings_configuration_by_scope(scope, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_execution_settings_configuration_by_scope: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **int**| Scope of the configuration; 0 for Global, 1 for Robot | 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ExecutionSettingsConfiguration**](ExecutionSettingsConfiguration.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_languages**
> ListResultDtoOfLanguageInfo settings_get_languages(expand=expand, select=select)

Gets supported languages

OAuth required scopes: OR.Settings or OR.Settings.Read.

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.SettingsApi()
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets supported languages
    api_response = api_instance.settings_get_languages(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_languages: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ListResultDtoOfLanguageInfo**](ListResultDtoOfLanguageInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_license**
> LicenseDto settings_get_license(expand=expand, select=select)

Retrieves the current license information.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Retrieves the current license information.
    api_response = api_instance.settings_get_license(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_license: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**LicenseDto**](LicenseDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_license_offline**
> ODataValueOfString settings_get_license_offline(body=body, expand=expand, select=select)

Create the offline activation request for a specific tenant

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Create or License.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.LicenseRequest() # LicenseRequest |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Create the offline activation request for a specific tenant
    api_response = api_instance.settings_get_license_offline(body=body, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_license_offline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LicenseRequest**](LicenseRequest.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ODataValueOfString**](ODataValueOfString.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_secure_store_configuration_by_storetypename**
> ODataValueOfIEnumerableOfConfigurationEntry settings_get_secure_store_configuration_by_storetypename(store_type_name, proxy_id=proxy_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)

Gets the configuration format for a Secure store

OAuth required scopes: OR.Settings or OR.Settings.Read.  Required permissions: Settings.View.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
store_type_name = 'store_type_name_example' # str | name of the secure store type
proxy_id = 789 # int | id of the hosted credential store (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
filter = 'filter_example' # str | Restricts the set of items returned. The maximum number of expressions is 100. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)
orderby = 'orderby_example' # str | Specifies the order in which items are returned. The maximum number of expressions is 5. (optional)
count = true # bool | Indicates whether the total count of items within a collection are returned in the result. (optional)

try:
    # Gets the configuration format for a Secure store
    api_response = api_instance.settings_get_secure_store_configuration_by_storetypename(store_type_name, proxy_id=proxy_id, expand=expand, filter=filter, select=select, orderby=orderby, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_secure_store_configuration_by_storetypename: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **store_type_name** | **str**| name of the secure store type | 
 **proxy_id** | **int**| id of the hosted credential store | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **filter** | **str**| Restricts the set of items returned. The maximum number of expressions is 100. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 
 **orderby** | **str**| Specifies the order in which items are returned. The maximum number of expressions is 5. | [optional] 
 **count** | **bool**| Indicates whether the total count of items within a collection are returned in the result. | [optional] 

### Return type

[**ODataValueOfIEnumerableOfConfigurationEntry**](ODataValueOfIEnumerableOfConfigurationEntry.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_timezones**
> ListResultDtoOfNameValueDto settings_get_timezones(expand=expand, select=select)

Gets timezones.

OAuth required scopes: OR.Settings or OR.Settings.Read.

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.SettingsApi()
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets timezones.
    api_response = api_instance.settings_get_timezones(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_timezones: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ListResultDtoOfNameValueDto**](ListResultDtoOfNameValueDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_update_settings**
> UpdateSettingsDto settings_get_update_settings(expand=expand, select=select)

Gets the update settings

OAuth required scopes: OR.Settings or OR.Settings.Read.

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.SettingsApi()
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Gets the update settings
    api_response = api_instance.settings_get_update_settings(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_update_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**UpdateSettingsDto**](UpdateSettingsDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_get_web_settings**
> ResponseDictionaryDto settings_get_web_settings(expand=expand, select=select)

Returns a collection of key value pairs representing settings used by Orchestrator web client.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Returns a collection of key value pairs representing settings used by Orchestrator web client.
    api_response = api_instance.settings_get_web_settings(expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_get_web_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**ResponseDictionaryDto**](ResponseDictionaryDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_put_by_id**
> SettingsDto settings_put_by_id(key, body=body)

Edits a setting.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
key = 'key_example' # str | 
body = uipath_orchestrator_rest.SettingsDto() # SettingsDto |  (optional)

try:
    # Edits a setting.
    api_response = api_instance.settings_put_by_id(key, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_put_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **body** | [**SettingsDto**](SettingsDto.md)|  | [optional] 

### Return type

[**SettingsDto**](SettingsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_set_calendar**
> settings_set_calendar(body=body)

Sets custom calendar, with excluded dates in UTC, for current tenant

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Edit. DEPRECATED:  This API is deprecated. Please do not use it any longer. Use /odata/Calendars instead. Please refer to https://docs.uipath.com/orchestrator/reference

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.CalendarDto() # CalendarDto |  (optional)

try:
    # Sets custom calendar, with excluded dates in UTC, for current tenant
    api_instance.settings_set_calendar(body=body)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_set_calendar: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CalendarDto**](CalendarDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_update_bulk**
> settings_update_bulk(body=body)

Updates the current settings.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.SettingsUpdateBulkRequest() # SettingsUpdateBulkRequest | Settings - The collection of settings to be updated. (optional)

try:
    # Updates the current settings.
    api_instance.settings_update_bulk(body=body)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_update_bulk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SettingsUpdateBulkRequest**](SettingsUpdateBulkRequest.md)| Settings - The collection of settings to be updated. | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_update_license_online**
> settings_update_license_online()

Update the license for a specific tenant

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))

try:
    # Update the license for a specific tenant
    api_instance.settings_update_license_online()
except ApiException as e:
    print("Exception when calling SettingsApi->settings_update_license_online: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_update_user_setting**
> SettingsDto settings_update_user_setting(body=body, expand=expand, select=select)

Edits a user setting.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Requires authentication.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.UpdateUserSettingRequest() # UpdateUserSettingRequest |  (optional)
expand = 'expand_example' # str | Indicates the related entities to be represented inline. The maximum depth is 2. (optional)
select = 'select_example' # str | Limits the properties returned in the result. (optional)

try:
    # Edits a user setting.
    api_response = api_instance.settings_update_user_setting(body=body, expand=expand, select=select)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_update_user_setting: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateUserSettingRequest**](UpdateUserSettingRequest.md)|  | [optional] 
 **expand** | **str**| Indicates the related entities to be represented inline. The maximum depth is 2. | [optional] 
 **select** | **str**| Limits the properties returned in the result. | [optional] 

### Return type

[**SettingsDto**](SettingsDto.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_upload_license**
> settings_upload_license(file)

Uploads a new license file that was previously generated with Regutil. The content of the license is sent as a file embedded in the HTTP request.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: License.Create or License.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
file = '/path/to/file.txt' # file | 

try:
    # Uploads a new license file that was previously generated with Regutil. The content of the license is sent as a file embedded in the HTTP request.
    api_instance.settings_upload_license(file)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_upload_license: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **settings_verify_smtp_setting**
> settings_verify_smtp_setting(body=body)

Verify whether the given SMTP settings are correct or not by sending an email to a recipient.

OAuth required scopes: OR.Settings or OR.Settings.Write.  Required permissions: Settings.Edit.

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
api_instance = uipath_orchestrator_rest.SettingsApi(uipath_orchestrator_rest.ApiClient(configuration))
body = uipath_orchestrator_rest.VerifySmtpSettingRequest() # VerifySmtpSettingRequest | SMTP setting parameters (optional)

try:
    # Verify whether the given SMTP settings are correct or not by sending an email to a recipient.
    api_instance.settings_verify_smtp_setting(body=body)
except ApiException as e:
    print("Exception when calling SettingsApi->settings_verify_smtp_setting: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**VerifySmtpSettingRequest**](VerifySmtpSettingRequest.md)| SMTP setting parameters | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json;odata.metadata=minimal;odata.streaming=true, application/json;odata.metadata=minimal;odata.streaming=false, application/json;odata.metadata=minimal, application/json;odata.metadata=full;odata.streaming=true, application/json;odata.metadata=full;odata.streaming=false, application/json;odata.metadata=full, application/json;odata.metadata=none;odata.streaming=true, application/json;odata.metadata=none;odata.streaming=false, application/json;odata.metadata=none, application/json;odata.streaming=true, application/json;odata.streaming=false, application/json, application/json-patch+json, application/*+json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

