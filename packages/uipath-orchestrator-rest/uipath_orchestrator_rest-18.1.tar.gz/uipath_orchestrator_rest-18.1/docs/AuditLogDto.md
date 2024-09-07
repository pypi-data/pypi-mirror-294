# AuditLogDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_name** | **str** | The name of the Orchestrator service that performed a given action in the system. | [optional] 
**method_name** | **str** | The name of the service method that performed a given action in the system. | [optional] 
**parameters** | **str** | JSON representation of the method parameters and their values for the given action. | [optional] 
**execution_time** | **datetime** | The date and time when the action was performed. | [optional] 
**action** | **str** | The action performed (create, update, delete etc) | [optional] 
**component** | **str** | The component for which the action was performed | [optional] 
**display_name** | **str** | The display name of the resource acted on, usually Name | [optional] 
**entity_id** | **int** | The Id of the resource acted on | [optional] 
**operation_text** | **str** | User friendly description of the change, e.g. \&quot;User X created robot Y\&quot; | [optional] 
**user_name** | **str** | UserName that sent the request | [optional] 
**user_type** | **str** | The type of user that sent the request | [optional] 
**entities** | [**list[AuditLogEntityDto]**](AuditLogEntityDto.md) | Audit entity details collection | [optional] 
**external_client_id** | **str** | External client identifier. Example: OAuth 3rd party app identifier that called Orchestrator. | [optional] 
**user_id** | **int** |  | [optional] 
**user_is_deleted** | **bool** | Marks whether the users that did the action was deleted in the meantime | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


