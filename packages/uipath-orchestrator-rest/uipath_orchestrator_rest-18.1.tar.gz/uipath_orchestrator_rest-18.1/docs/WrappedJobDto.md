# WrappedJobDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**key** | **str** | The unique job identifier. | [optional] 
**creation_time** | **datetime** | The Creation time of the job | [optional] 
**start_time** | **datetime** | The date and time when the job execution started or null if the job hasn&#39;t started yet. | [optional] 
**end_time** | **datetime** | The date and time when the job execution ended or null if the job hasn&#39;t ended yet. | [optional] 
**state** | **str** | The state in which the job is. | [optional] 
**source** | **str** | The Source name of the job. | [optional] 
**source_type** | **str** | The Source type of the job. | [optional] 
**batch_execution_key** | **str** | The unique identifier grouping multiple jobs. It is usually generated when the job is created by a schedule. | [optional] 
**info** | **str** | Additional information about the current job. | [optional] 
**starting_schedule_id** | **int** | The Id of the schedule that started the job, or null if the job was started by the user. | [optional] 
**release_name** | **str** | The name of the release associated with the current name. | [optional] 
**type** | **str** | The type of the job, Attended if started via the robot, Unattended otherwise | [optional] 
**host_machine_name** | **str** | The name of the machine where the Robot run the job. | [optional] 
**robot** | [**WrappedRobotDto**](WrappedRobotDto.md) |  | [optional] 
**release** | [**WrappedReleaseDto**](WrappedReleaseDto.md) |  | [optional] 
**input_arguments** | **object** | Input parameters in JSON format to be passed to job execution | [optional] 
**output_arguments** | **object** | Output parameters in JSON format resulted from job execution | [optional] 
**runtime_type** | **str** | The type of license used to run the job | [optional] 
**process_type** | **str** | The type of process | [optional] 
**specific_priority_value** | **int** | The priority for a job | [optional] 
**project_key** | **str** | The project key which the job is part of | [optional] 
**parent_operation_id** | **str** | The operation id which created the job | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


