# TaskDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Gets or sets the status of this task. | [optional] 
**assigned_to_user** | [**UserLoginInfoDto**](UserLoginInfoDto.md) |  | [optional] 
**creator_user** | [**UserLoginInfoDto**](UserLoginInfoDto.md) |  | [optional] 
**last_modifier_user** | [**UserLoginInfoDto**](UserLoginInfoDto.md) |  | [optional] 
**task_catalog_name** | **str** | Gets or sets the task catalog/category of the task | [optional] 
**is_completed** | **bool** |  | [optional] 
**bulk_form_layout_id** | **int** | Gets or sets the bulkFormLayoutId of the task | [optional] 
**form_layout_id** | **int** | Gets or sets the formLayoutId of the task | [optional] 
**encrypted** | **bool** | Indicates if the task Data field is stored in an encrypted form. | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) | List of tags associated to the task. | [optional] 
**action** | **str** | Gets or sets the action performed on the task | [optional] 
**activities** | [**list[TaskActivityDto]**](TaskActivityDto.md) | Gets the associated task activities for the task | [optional] 
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


