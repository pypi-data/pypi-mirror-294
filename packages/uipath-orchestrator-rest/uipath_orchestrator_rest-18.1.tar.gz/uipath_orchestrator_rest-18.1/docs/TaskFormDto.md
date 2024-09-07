# TaskFormDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**form_layout** | **object** | Task Form Layout json | [optional] 
**form_layout_id** | **int** | Task Form Layout Id | [optional] 
**bulk_form_layout_id** | **int** | Task Form Layout Id | [optional] 
**action_label** | **str** | Task form action label | [optional] 
**status** | **str** | Task status | [optional] 
**data** | **object** | Task form data json | [optional] 
**action** | **str** | Task form action | [optional] 
**wait_job_state** | **str** | State of the job(if any) waiting on the current task | [optional] 
**organization_unit_fully_qualified_name** | **str** | Fully qualified folder name | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) | List of tags associated to the task. | [optional] 
**assigned_to_user** | [**UserLoginInfoDto**](UserLoginInfoDto.md) |  | [optional] 
**title** | **str** | Gets or sets title of this task. | [optional] 
**type** | **str** | Gets or sets type of this task. | [optional] 
**priority** | **str** | Gets or sets priority of this task. | [optional] 
**assigned_to_user_id** | **int** | Gets the id of the actual assigned user, if any. | [optional] 
**organization_unit_id** | **int** | Gets or sets the folder/organization-unit id. | [optional] 
**external_tag** | **str** | Identifier of external system where this task is handled | [optional] 
**creator_job_key** | **str** | Key of the job which created this task | [optional] 
**wait_job_key** | **str** | Key job which is waiting on this task | [optional] 
**last_assigned_time** | **datetime** | Datetime when task was last assigned. | [optional] 
**completion_time** | **datetime** | Datetime when task was completed. | [optional] 
**parent_operation_id** | **str** | Operation id which created the task. | [optional] 
**key** | **str** | The unique Task identifier. | [optional] 
**is_deleted** | **bool** |  | [optional] 
**deleter_user_id** | **int** |  | [optional] 
**deletion_time** | **datetime** |  | [optional] 
**last_modification_time** | **datetime** |  | [optional] 
**last_modifier_user_id** | **int** |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**creator_user_id** | **int** |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


