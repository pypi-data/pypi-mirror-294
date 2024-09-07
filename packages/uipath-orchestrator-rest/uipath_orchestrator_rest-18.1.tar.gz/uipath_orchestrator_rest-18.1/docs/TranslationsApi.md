# uipath_orchestrator_rest.TranslationsApi

All URIs are relative to *https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**translations_get_translations**](TranslationsApi.md#translations_get_translations) | **GET** /api/Translations/GetTranslations | Returns a json with translation resources


# **translations_get_translations**
> dict(str, str) translations_get_translations(lang=lang)

Returns a json with translation resources

### Example
```python
from __future__ import print_function
import time
import uipath_orchestrator_rest
from uipath_orchestrator_rest.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = uipath_orchestrator_rest.TranslationsApi()
lang = 'lang_example' # str |  (optional)

try:
    # Returns a json with translation resources
    api_response = api_instance.translations_get_translations(lang=lang)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TranslationsApi->translations_get_translations: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lang** | **str**|  | [optional] 

### Return type

**dict(str, str)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

