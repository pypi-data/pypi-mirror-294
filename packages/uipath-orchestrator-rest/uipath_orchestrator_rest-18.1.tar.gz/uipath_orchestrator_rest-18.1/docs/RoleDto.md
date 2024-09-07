# RoleDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A custom name for the role. | [optional] 
**display_name** | **str** | An alternative name used for UI display. | [optional] 
**type** | **str** | Can be: Mixed, Tenant or Folder based on the permissions it includes | [optional] 
**groups** | **str** | Allows grouping multiple roles together. | [optional] 
**is_static** | **bool** | States whether this role is defined by the application and cannot be deleted or it is user defined and can be deleted. | [optional] 
**is_editable** | **bool** | States whether the permissions for this role can be modified or not. | [optional] 
**permissions** | [**list[PermissionDto]**](PermissionDto.md) | The collection of application permissions associated with the role. | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


