# TaskCatalogDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | Key of the Task Catalog. | [optional] 
**name** | **str** | Name of the Task Catalog. | [optional] 
**description** | **str** | Description of this task catalog. | [optional] 
**creation_time** | **datetime** | Creation time of task catalog | [optional] 
**last_modification_time** | **datetime** | Last Modification time of task catalog | [optional] 
**folders_count** | **int** | Number of folders where the task catalog is shared. | [optional] 
**encrypted** | **bool** | If the catalog is encrypted, tasks asociated to this will have their Data encrypted | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) | List of tags associated to the task. | [optional] 
**retention_action** | **str** | Action to take at retention limit | [optional] 
**retention_period** | **int** | Retention period | [optional] 
**retention_bucket_id** | **int** | Retention bucket Id | [optional] 
**retention_bucket_name** | **str** | Retention bucket name | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


