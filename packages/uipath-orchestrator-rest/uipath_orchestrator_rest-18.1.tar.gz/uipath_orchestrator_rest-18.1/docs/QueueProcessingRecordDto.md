# QueueProcessingRecordDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queue_definition_id** | **int** | The Id of the queue for which the report is done. | [optional] 
**ui_queue_metadata** | [**QueueDefinitionDto**](QueueDefinitionDto.md) |  | [optional] 
**processing_time** | **datetime** | The date and time when the report is computed. | [optional] 
**report_type** | **str** | The aggregation period used in the report. | [optional] 
**number_of_remaining_transactions** | **int** | The number of unprocessed (new) items. | [optional] 
**number_of_in_progress_transactions** | **int** | The number of items in progress. | [optional] 
**number_of_application_exceptions** | **int** | The total number of application exceptions thrown while processing queue items in the given time period. | [optional] 
**number_of_business_exceptions** | **int** | The total number of business exceptions thrown while processing queue items in the given time period. | [optional] 
**number_of_successful_transactions** | **int** | The total number of successfully processed queue items in the given time period. | [optional] 
**number_of_retried_items** | **int** | The total number of processing retries occurred in the given time period. | [optional] 
**application_exceptions_processing_time** | **float** | The total number of seconds spent processing queue items that failed with application exception in the given time period. | [optional] 
**business_exceptions_processing_time** | **float** | The total number of seconds spent processing queue items that failed with business exception in the given time period. | [optional] 
**successful_transactions_processing_time** | **float** | The total number of seconds spent processing successful queue items in the given time period. | [optional] 
**total_number_of_transactions** | **int** | The total number of item processing transactions, both failed and successful. | [optional] 
**tenant_id** | **int** | The Id of the queue tenant. | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


