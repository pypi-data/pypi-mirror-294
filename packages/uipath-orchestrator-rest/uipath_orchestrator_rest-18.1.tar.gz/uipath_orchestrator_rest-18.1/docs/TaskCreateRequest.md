# TaskCreateRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Gets or sets type of this task, allowed type is &#39;ExternalTask&#39;. | [optional] 
**title** | **str** | Gets or sets title of this task. | 
**priority** | **str** | Gets or sets priority of this task. | [optional] 
**data** | **object** | Task data | [optional] 
**task_catalog_name** | **str** | Gets or sets the task catalog/category of the task | [optional] 
**external_tag** | **str** | Reference or name of external system | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) | List of tags associated to the task. | [optional] 
**parent_operation_id** | **str** | Operation id which created the task. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


