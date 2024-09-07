# JobTriggerDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **int** |  | [optional] 
**trigger_type** | **str** | Resume type (job, queue, task etc) | [optional] 
**status** | **str** | Job trigger status (new, ready, fired etc) | [optional] 
**item_id** | **int** | item Id (queue item id, task id, job id etc) | [optional] 
**timer** | **datetime** | Resume timer (for time trigger) | [optional] 
**trigger_message** | **str** | Workflow provided resume trigger description/message | [optional] 
**inbox_id** | **str** |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


