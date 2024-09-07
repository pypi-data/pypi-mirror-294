# BulkTasksCompletionRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Action taken on this task | 
**task_ids** | **list[int]** | List of Task Ids which have to be Bulk edited | 
**data** | **object** | Task data json | 
**title** | **str** | Title of tasks | [optional] 
**task_catalog_id** | **int** | Action Catalog to be associated with the tasks | [optional] 
**unset_task_catalog** | **bool** | Unset/Unassociate action catalogs with the tasks  Set to true for unassociating catalog | [optional] 
**priority** | **str** | Priority of tasks | [optional] 
**note_text** | **str** | Comment to be added while doing the bulk operation | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


