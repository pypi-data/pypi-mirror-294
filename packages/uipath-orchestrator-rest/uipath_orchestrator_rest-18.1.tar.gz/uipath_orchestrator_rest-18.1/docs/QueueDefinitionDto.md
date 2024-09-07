# QueueDefinitionDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | A unique identifier associated to each queue. | [optional] 
**name** | **str** | A custom name for the queue. | 
**description** | **str** | Used to add additional information about a queue in order to better identify it. | [optional] 
**max_number_of_retries** | **int** | An integer value representing the number of times an item of this queue can be retried if its processing fails with application exception and auto retry is on. | [optional] 
**accept_automatically_retry** | **bool** | States whether a robot should retry to process an item if, after processing, it failed with application exception. | [optional] 
**enforce_unique_reference** | **bool** | States whether Item Reference field should be unique per Queue. Deleted and retried items are not checked against this rule. | [optional] 
**encrypted** | **bool** | States whether the Queue Item&#39;s data will be encrypted in the database. | [optional] 
**specific_data_json_schema** | **str** | JSON schema enforced onto the specific data field. | [optional] 
**output_data_json_schema** | **str** | JSON schema enforced onto the output data field. | [optional] 
**analytics_data_json_schema** | **str** | JSON schema enforced onto the analytics data field. | [optional] 
**creation_time** | **datetime** | The date and time when the queue was created. | [optional] 
**process_schedule_id** | **int** | The Id of the process schedule associated with the queue. | [optional] 
**sla_in_minutes** | **int** | Queue item processing SLA on the QueueDefinition level. | [optional] 
**risk_sla_in_minutes** | **int** | Queue Item processing Risk SLA on the QueueDefinition level. | [optional] 
**release_id** | **int** | The ProcessId Queue is associated with. | [optional] 
**is_process_in_current_folder** | **bool** | Flag to determine if the release is in the current folder | [optional] 
**folders_count** | **int** | Number of folders where the queue is shared. | [optional] 
**organization_unit_id** | **int** | DEPRECATED.  | [optional] 
**organization_unit_fully_qualified_name** | **str** | DEPRECATED.  | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


