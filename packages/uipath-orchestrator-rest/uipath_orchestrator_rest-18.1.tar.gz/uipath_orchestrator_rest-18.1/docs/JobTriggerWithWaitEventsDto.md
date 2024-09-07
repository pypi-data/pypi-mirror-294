# JobTriggerWithWaitEventsDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Job Trigger Id | [optional] 
**job_id** | **int** | Job Id | [optional] 
**trigger_type** | **str** | Resume type (job, queue, task etc) | [optional] 
**status** | **str** | Job trigger status (new, ready, fired etc) | [optional] 
**item_id** | **int** | item Id (queue item id, task id, job id etc) | [optional] 
**timer** | **datetime** | Resume timer (for time trigger) | [optional] 
**trigger_message** | **str** | Workflow provided resume trigger description/message | [optional] 
**item_name** | **str** | Name of the Item on which wait is placed | [optional] 
**assigned_to_user_id** | **int** | Assigned to UserId | [optional] 
**name** | **str** | Assigned to User - Name | [optional] 
**surname** | **str** | Assigned to User - SurName | [optional] 
**user_name** | **str** | Assigned to User - UserName | [optional] 
**email_address** | **str** | Assigned to User - EmailAddress | [optional] 
**creation_time** | **datetime** | Creationtime of the item | [optional] 
**modified_time** | **datetime** | Modification time of the item | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


