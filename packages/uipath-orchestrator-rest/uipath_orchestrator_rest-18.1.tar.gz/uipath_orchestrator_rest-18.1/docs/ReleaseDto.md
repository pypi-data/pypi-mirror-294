# ReleaseDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | A unique identifier associated to each release. | [optional] 
**process_key** | **str** | The unique identifier of the process associated with the release. | 
**process_version** | **str** | The version of the process associated with the release. | 
**is_latest_version** | **bool** | States whether the version of process associated with the release is latest or not. | [optional] 
**is_process_deleted** | **bool** | States whether the process associated with the release is deleted or not. | [optional] 
**description** | **str** | Used to add additional information about a release in order to better identify it. | [optional] 
**name** | **str** | A custom name of the release. The default name format is ProcessName_EnvironmentName. | 
**environment_id** | **int** | The Id of the environment associated with the release. | [optional] 
**environment_name** | **str** | The name of the environment associated with the release. | [optional] 
**environment** | [**EnvironmentDto**](EnvironmentDto.md) |  | [optional] 
**entry_point_id** | **int** |  | [optional] 
**entry_point_path** | **str** |  | [optional] 
**entry_point** | [**EntryPointDto**](EntryPointDto.md) |  | [optional] 
**input_arguments** | **str** | Input parameters in JSON format to be passed as default values to job execution. | [optional] 
**process_type** | **str** |  | [optional] 
**supports_multiple_entry_points** | **bool** |  | [optional] 
**requires_user_interaction** | **bool** |  | [optional] 
**is_attended** | **bool** |  | [optional] 
**is_compiled** | **bool** |  | [optional] 
**automation_hub_idea_url** | **str** |  | [optional] 
**current_version** | [**ReleaseVersionDto**](ReleaseVersionDto.md) |  | [optional] 
**release_versions** | [**list[ReleaseVersionDto]**](ReleaseVersionDto.md) | The collection of release versions that current release had over time. | [optional] 
**arguments** | [**ArgumentMetadata**](ArgumentMetadata.md) |  | [optional] 
**process_settings** | [**ProcessSettingsDto**](ProcessSettingsDto.md) |  | [optional] 
**video_recording_settings** | [**VideoRecordingSettingsDto**](VideoRecordingSettingsDto.md) |  | [optional] 
**auto_update** | **bool** |  | [optional] 
**hidden_for_attended_user** | **bool** |  | [optional] 
**feed_id** | **str** |  | [optional] 
**job_priority** | **str** | The execution priority. If null, it defaults to Normal. | [optional] 
**specific_priority_value** | **int** | Value for more granular control over execution priority. | [optional] 
**organization_unit_id** | **int** | Id of the folder this release is part of. | [optional] 
**organization_unit_fully_qualified_name** | **str** | Fully qualified name of the folder this release is part of. | [optional] 
**target_framework** | **str** |  | [optional] 
**robot_size** | **str** |  | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) |  | [optional] 
**remote_control_access** | **str** |  | [optional] 
**last_modification_time** | **datetime** |  | [optional] 
**last_modifier_user_id** | **int** |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**creator_user_id** | **int** |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


