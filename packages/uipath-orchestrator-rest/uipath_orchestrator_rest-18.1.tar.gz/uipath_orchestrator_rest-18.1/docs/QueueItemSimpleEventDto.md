# QueueItemSimpleEventDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**key** | **str** | The Key of a queue item. In a retry-chain, all retries will inherit the initial queue item&#39;s Key. | [optional] 
**reference** | **str** | An optional, user-specified value for queue item identification. | [optional] 
**queue_definition_id** | **int** | The Id of the parent queue. | [optional] 
**status** | **str** | The processing state of the item. | [optional] 
**review_status** | **str** | The review state of the item - applicable only for failed items. | [optional] 
**processing_exception** | [**WrappedProcessingExceptionDto**](WrappedProcessingExceptionDto.md) |  | [optional] 
**due_date** | **datetime** | The latest date and time at which the item should be processed. If empty the item can be processed at any given time. | [optional] 
**priority** | **str** | Sets the processing importance for a given item. | [optional] 
**creation_time** | **datetime** | The date and time when the item was created. | [optional] 
**defer_date** | **datetime** | The earliest date and time at which the item is available for processing. If empty the item can be processed as soon as possible. | [optional] 
**start_processing** | **datetime** | The date and time at which the item processing started. This is null if the item was not processed. | [optional] 
**end_processing** | **datetime** | The date and time at which the item processing ended. This is null if the item was not processed. | [optional] 
**creator_job_id** | **int** | The id for the job that created the queue item | [optional] 
**creator_job_key** | **str** | The unique identifier for the job that created the queue item | [optional] 
**executor_job_id** | **int** | The id for the job that processed the queue item | [optional] 
**executor_job_key** | **str** | The unique identifier for the job that processed the queue item | [optional] 
**creator_user_id** | **int** | The id for the user that created the queue item | [optional] 
**risk_sla_date** | **datetime** | The RiskSla date at time which is considered as risk zone for the item to be processed. | [optional] 
**seconds_in_previous_attempts** | **int** | The number of seconds that the last failed processing lasted. | [optional] 
**ancestor_id** | **int** | The Id of the item being Automatically retried. | [optional] 
**ancestor_unique_key** | **str** | The Unique Key of the item being Automatically retried. | [optional] 
**retry_number** | **int** | The number of times this work item has been processed.  &lt;para /&gt;This can be higher than 0 only if MaxRetried number is set and the item processing failed at least once with ApplicationException. | [optional] 
**manual_ancestor_id** | **int** | The Id of the item being Manually retried. | [optional] 
**manual_ancestor_unique_key** | **str** | The Unique Key of the item being Manually retried. | [optional] 
**manual_retry_number** | **int** | The number of times this work item has been Manually retried. | [optional] 
**unique_key** | **str** | The Unique Key of the item | [optional] 
**progress** | **str** | String field which is used to keep track of the business flow progress. | [optional] 
**reviewer_user_id** | **int** | The UserId of the Reviewer, if any. | [optional] 
**robot** | [**WrappedRobotDto**](WrappedRobotDto.md) |  | [optional] 
**reviewer_user** | [**WebhookSimpleUserDto**](WebhookSimpleUserDto.md) |  | [optional] 
**specific_content** | **dict(str, object)** | A collection of key value pairs containing custom data configured in the Add Queue Item activity, in UiPath Studio. | [optional] 
**output** | **dict(str, object)** | A collection of key value pairs containing custom data resulted after successful processing. | [optional] 
**source** | **str** | Where the queue item was created | [optional] 
**parent_operation_id** | **str** | Operation id which added the queue item | [optional] 
**operation_id** | **str** | Operation id which processed the queue item | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


