# FormTaskCreateRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**form_layout** | **object** | Text representing the form layout schema | [optional] 
**form_layout_id** | **int** | Unique FormLayoutId for a form layout | [optional] 
**bulk_form_layout_id** | **int** | Unique BulkFormLayoutId for a form layout | [optional] 
**title** | **str** | Gets or sets title of this task. | 
**priority** | **str** | Gets or sets priority of this task. | [optional] 
**data** | **object** | Task data | [optional] 
**task_catalog_name** | **str** | Gets or sets the task catalog/category of the task | [optional] 
**external_tag** | **str** | Reference or name of external system | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) | List of tags associated to the task. | [optional] 
**parent_operation_id** | **str** | Operation id which created the task. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


