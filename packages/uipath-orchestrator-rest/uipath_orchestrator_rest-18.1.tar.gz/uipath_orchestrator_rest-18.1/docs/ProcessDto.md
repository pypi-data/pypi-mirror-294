# ProcessDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_active** | **bool** | Specifies if the process is still active. | [optional] 
**arguments** | [**ArgumentMetadata**](ArgumentMetadata.md) |  | [optional] 
**supports_multiple_entry_points** | **bool** | Specifies if the process has multiple entry points. | [optional] 
**main_entry_point_path** | **str** | The main entry point path. | [optional] 
**requires_user_interaction** | **bool** | Specifies if the process can run in headless mode. | [optional] 
**is_attended** | **bool** |  | [optional] 
**target_framework** | **str** |  | [optional] 
**entry_points** | [**list[EntryPointDto]**](EntryPointDto.md) | Entry points. | [optional] 
**title** | **str** | The custom name of the package. | [optional] 
**version** | **str** | The current version of the given package. | [optional] 
**key** | **str** | The unique identifier for the package. | [optional] 
**description** | **str** | Used to add additional information about a package in order to better identify it. | [optional] 
**published** | **datetime** | The date and time when the package was published or uploaded. | [optional] 
**is_latest_version** | **bool** | Specifies whether the current version is the latest of the given package. | [optional] 
**old_version** | **str** | Specifies the last version before the current one. | [optional] 
**release_notes** | **str** | Package release notes. | [optional] 
**authors** | **str** | Package authors. | [optional] 
**project_type** | **str** | Package project type. | [optional] 
**tags** | **str** | Package tags. | [optional] 
**is_compiled** | **bool** | Disable explore packages for compiled processes | [optional] 
**license_url** | **str** | License URL | [optional] 
**project_url** | **str** | Project URL | [optional] 
**resource_tags** | [**list[TagDto]**](TagDto.md) | Tags set up by orchestrator | [optional] 
**id** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


