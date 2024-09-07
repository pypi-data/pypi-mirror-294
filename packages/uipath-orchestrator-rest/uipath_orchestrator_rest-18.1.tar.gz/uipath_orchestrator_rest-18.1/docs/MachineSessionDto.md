# MachineSessionDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_user_name** | **str** |  | [optional] 
**robot** | [**RobotWithLicenseDto**](RobotWithLicenseDto.md) |  | [optional] 
**host_machine_name** | **str** | The name of the machine a Robot is hosted on. | [optional] 
**machine_id** | **int** | The Id of the Machine. | [optional] 
**machine_name** | **str** | The Machine&#39;s name. | [optional] 
**state** | **str** | The value of the last reported status. | [optional] 
**job** | [**JobDto**](JobDto.md) |  | [optional] 
**reporting_time** | **datetime** | The date and time when the last heartbeat came. | [optional] 
**info** | **str** | May store additional information about the robot state. | [optional] 
**is_unresponsive** | **bool** | If the robot did not report status for longer than 120 seconds. | [optional] 
**license_error_code** | **str** | DEPRECATED. Last licensing error status. | [optional] 
**organization_unit_id** | **int** | The folder Id. | [optional] 
**folder_name** | **str** | The folder display name. | [optional] 
**robot_session_type** | **str** | The robot session type. | [optional] 
**version** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**debug_mode_expiration_date** | **datetime** |  | [optional] 
**update_info** | [**UpdateInfoDto**](UpdateInfoDto.md) |  | [optional] 
**installation_id** | **str** |  | [optional] 
**platform** | **str** |  | [optional] 
**endpoint_detection** | **str** |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


