# QueueItemEventDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queue_item_id** | **int** | The Id of a Queue Item that the current item is connected to. | [optional] 
**timestamp** | **datetime** | The Date and Time when the event occured. | [optional] 
**action** | **str** | The Action that caused the event. | [optional] 
**data** | **str** | The Data associated to the event. | [optional] 
**user_id** | **int** | The Id of the User that caused the event. | [optional] 
**user_name** | **str** | The Name of the User that caused the event. | [optional] 
**status** | **str** | Processing Status when event snapshot was taken. | [optional] 
**review_status** | **str** | Review Status when event snapshot was taken. | [optional] 
**reviewer_user_id** | **int** | Reviewer User Id when event snapshot was taken. | [optional] 
**reviewer_user_name** | **str** | Reviewer User Name when event snapshot was taken. | [optional] 
**external_client_id** | **str** | The External client identifier that caused the event. Example: OAuth 3rd party app identifier that called Orchestrator. | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


