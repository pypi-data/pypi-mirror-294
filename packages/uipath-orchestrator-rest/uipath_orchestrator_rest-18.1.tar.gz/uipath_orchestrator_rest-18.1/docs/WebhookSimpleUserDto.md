# WebhookSimpleUserDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**key** | **str** |  | [optional] 
**user_name** | **str** | The name used to login to Orchestrator. | [optional] 
**domain** | **str** | The domain from which the user is imported | [optional] 
**full_name** | **str** | The full name of the person constructed with the format Name Surname. | [optional] 
**email_address** | **str** | The e-mail address associated with the user. | [optional] 
**type** | **str** | The user type. | [optional] 
**is_active** | **bool** | States if the user is active or not. An inactive user cannot login to Orchestrator. | [optional] 
**last_login_time** | **datetime** | The date and time when the user last logged in, or null if the user never logged in. | [optional] 
**creation_time** | **datetime** | The date and time when the user was created. | [optional] 
**authentication_source** | **str** | The source which authenticated this user. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


