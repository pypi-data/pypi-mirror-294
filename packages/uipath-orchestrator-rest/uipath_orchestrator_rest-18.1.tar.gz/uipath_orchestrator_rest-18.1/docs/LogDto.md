# LogDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**level** | **str** | Defines the log severity. | [optional] 
**windows_identity** | **str** | The name of the user that performed the action that was logged. | [optional] 
**process_name** | **str** | The name of the process. | [optional] 
**time_stamp** | **datetime** | The exact date and time the action was performed. | [optional] 
**message** | **str** | The log message. This can also be a message logged through the Log Message activity in UiPath Studio. | [optional] 
**job_key** | **str** | The key of the job running the process that generated the log, if any. | [optional] 
**raw_message** | **str** | A JSON format message containing all the above fields. | [optional] 
**robot_name** | **str** | The name of the Robot that generated the log. | [optional] 
**host_machine_name** | **str** | The name of the machine that generated the log | [optional] 
**machine_id** | **int** | The Id of the Machine on which the Robot that generated the log is running. | [optional] 
**machine_key** | **str** | The Key of the Machine on which the Robot that generated the log is running. | [optional] 
**runtime_type** | **str** | The RuntimeType of the job referenced by the JobKey field | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


