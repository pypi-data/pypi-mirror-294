# StartProcessDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**release_key** | **str** | The unique key of the release associated with the process. | [optional] 
**strategy** | **str** | States which robots from the environment are being run by the process. | [optional] 
**robot_ids** | **list[int]** | The collection of ids of specific robots selected to be run by the current process. This collection must be empty only if the start strategy is not Specific. | [optional] 
**machine_session_ids** | **list[int]** | The machines used for running the job. If empty, the job will start on the first available machine | [optional] 
**no_of_robots** | **int** | DEPRECATED. Number of pending jobs to be created in the environment, for the current process. This number must be greater than 0 only if the start strategy is RobotCount. | [optional] 
**jobs_count** | **int** | Number of pending jobs to be created in the environment, for the current process. This number must be greater than 0 only if the start strategy is JobsCount. | [optional] 
**source** | **str** | The Source of the job starting the current process. | [optional] 
**job_priority** | **str** | Execution priority. If null, defaults to the JobPriority of its release. | [optional] 
**specific_priority_value** | **int** | Value for more granular control over execution priority. | [optional] 
**runtime_type** | **str** |  | [optional] 
**input_arguments** | **str** | Input parameters in JSON format to be passed to job execution. | [optional] 
**reference** | **str** | Optional user-specified reference for jobs | [optional] 
**machine_robots** | [**list[MachineRobotDto]**](MachineRobotDto.md) | The machine-robot mappings used for running the job. | [optional] 
**target_framework** | **str** |  | [optional] 
**resume_on_same_context** | **bool** | Gets or sets flag for honoring initial machine and robot choice upon resumption of created jobs, if jobs are suspended. &lt;br /&gt;  If set, the jobs will resume on the same robot-machine pair on which they initially ran. | [optional] 
**batch_execution_key** | **str** | Optional BatchExecutionKey | [optional] 
**requires_user_interaction** | **bool** | Specifies if the process can run in headless mode. | [optional] 
**stop_process_expression** | **str** | Number of seconds after which a running process will be stopped. | [optional] 
**stop_strategy** | **str** | The way a running process is stopped. | [optional] 
**kill_process_expression** | **str** | Grace period (in seconds) for soft stop. If a process doesn&#39;t stop after this amount, it will be killed | [optional] 
**remote_control_access** | **str** |  | [optional] 
**alert_pending_expression** | **str** |  | [optional] 
**alert_running_expression** | **str** |  | [optional] 
**run_as_me** | **bool** |  | [optional] 
**parent_operation_id** | **str** | Operation id which started the job. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


