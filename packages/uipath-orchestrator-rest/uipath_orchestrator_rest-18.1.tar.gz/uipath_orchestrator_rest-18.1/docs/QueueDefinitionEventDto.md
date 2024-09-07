# QueueDefinitionEventDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**key** | **str** |  | [optional] 
**name** | **str** | A custom name for the queue. | [optional] 
**description** | **str** | Used to add additional information about a queue in order to better identify it. | [optional] 
**max_number_of_retries** | **int** | An integer value representing the number of times an item of this queue can be retried if its processing fails with application exception and auto retry is on. | [optional] 
**accept_automatically_retry** | **bool** | States whether a robot should retry to process an item if, after processing, it failed with application exception. | [optional] 
**enforce_unique_reference** | **bool** | States whether Item Reference field should be unique per Queue. Deleted and retried items are not checked against this rule. | [optional] 
**sla_in_minutes** | **int** | An integer value representing the Queue SLA in minutes. | [optional] 
**risk_sla_in_minutes** | **int** | An integer value representing the Queue RiskSla in minutes. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


