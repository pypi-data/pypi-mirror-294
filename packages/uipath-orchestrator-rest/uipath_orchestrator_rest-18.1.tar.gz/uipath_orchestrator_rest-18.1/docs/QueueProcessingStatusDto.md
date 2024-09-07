# QueueProcessingStatusDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items_to_process** | **int** | The total number of items in the queue with the status New. | [optional] 
**items_in_progress** | **int** | The total number of items in the queue with the status InProgress. | [optional] 
**queue_definition_id** | **int** | The Id of the queue for which the report is done. | [optional] 
**queue_definition_key** | **str** | The Key of the queue for which the report is done. | [optional] 
**queue_definition_name** | **str** | The name of the queue for which the report is done. | [optional] 
**queue_definition_description** | **str** | The description of the queue for which the report is done. | [optional] 
**queue_definition_accept_automatically_retry** | **bool** | States whether the queue accepts automatic item retry or not. | [optional] 
**queue_definition_max_number_of_retries** | **int** | The maximum number of retries allowed for any item of the queue. | [optional] 
**queue_definition_enforce_unique_reference** | **bool** | States whether Item Reference field should be unique per Queue. Deleted and retried items are not checked against this rule. | [optional] 
**processing_mean_time** | **float** | The average time spent processing a successful item. | [optional] 
**successful_transactions_no** | **int** | The total number of successfully processed items. | [optional] 
**application_exceptions_no** | **int** | The total number of application exceptions thrown while processing queue items. | [optional] 
**business_exceptions_no** | **int** | The total number of business exceptions thrown while processing queue items. | [optional] 
**successful_transactions_processing_time** | **float** | The total number of seconds spent processing successful queue items. | [optional] 
**application_exceptions_processing_time** | **float** | The total number of seconds spent processing queue items that failed with application exception. | [optional] 
**business_exceptions_processing_time** | **float** | The total number of seconds spent processing queue items that failed with business exception. | [optional] 
**total_number_of_transactions** | **int** | The total number of item processing transactions, both failed and successful. | [optional] 
**last_processed** | **datetime** | The date and time of the last item processing. | [optional] 
**release_name** | **str** | The name of the process associated with the queue. | [optional] 
**release_id** | **int** | The ProcessId Queue is associated with. | [optional] 
**is_process_in_current_folder** | **bool** | Flag to determine if the release is in the current folder | [optional] 
**specific_data_json_schema_exists** | **bool** | Optional JSON schema enforced onto the specific data field is set. | [optional] 
**output_data_json_schema_exists** | **bool** | Optional JSON schema enforced onto the output data field is set. | [optional] 
**analytics_data_json_schema_exists** | **bool** | Optional JSON schema enforced onto the analytics data field is set. | [optional] 
**process_schedule_id** | **int** | The Id of the process schedule associated with the queue. | [optional] 
**queue_folders_count** | **int** | The number of folders where the queue definition is shared. | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


