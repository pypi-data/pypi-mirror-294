# JobsCreatedEventDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**event_id** | **str** |  | 
**entity_key** | **str** |  | [optional] 
**timestamp** | **datetime** |  | 
**start_info** | [**WrappedStartProcessDto**](WrappedStartProcessDto.md) |  | [optional] 
**jobs** | [**list[WrappedJobDto]**](WrappedJobDto.md) | List of jobs that were created and are in pending state | [optional] 
**event_time** | **datetime** |  | [optional] 
**tenant_id** | **int** |  | [optional] 
**organization_unit_id** | **int** |  | [optional] 
**organization_unit_key** | **str** |  | [optional] 
**user_id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


