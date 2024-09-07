# QueueItemDataDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the queue into which the item will be added. | [optional] 
**priority** | **str** | Sets the processing importance for a given item. | [optional] 
**specific_content** | **dict(str, object)** | A collection of key value pairs containing custom data configured in the Add Queue Item activity, in UiPath Studio. | [optional] 
**defer_date** | **datetime** | The earliest date and time at which the item is available for processing. If empty the item can be processed as soon as possible. | [optional] 
**due_date** | **datetime** | The latest date and time at which the item should be processed. If empty the item can be processed at any given time. | [optional] 
**risk_sla_date** | **datetime** | The RiskSla date at time which is considered as risk zone for the item to be processed. | [optional] 
**reference** | **str** | An optional, user-specified value for queue item identification. | [optional] 
**progress** | **str** | String field which is used to keep track of the business flow progress. | [optional] 
**source** | **str** | The Source type of the item. | [optional] 
**parent_operation_id** | **str** | Operation id which started the job. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


