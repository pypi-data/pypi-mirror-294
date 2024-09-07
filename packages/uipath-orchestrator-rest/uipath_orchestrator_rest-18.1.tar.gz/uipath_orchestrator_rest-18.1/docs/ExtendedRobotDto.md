# ExtendedRobotDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user** | [**UserDto**](UserDto.md) |  | [optional] 
**license_key** | **str** | The key is automatically generated from the server for the Robot machine.  &lt;para /&gt;For the robot to work, the same key must exist on both the robot and Orchestrator.  &lt;para /&gt;All robots on a machine must have the same license key in order to register correctly. | [optional] 
**machine_name** | **str** | The name of the machine a Robot is hosted on. | [optional] 
**machine_id** | **int** | The Id of the machine a Robot is hosted on | [optional] 
**name** | **str** | A custom name for the robot. | 
**username** | **str** | The machine username. If the user is under a domain, you are required to also specify it in a DOMAIN\\username format.  &lt;para /&gt;Note: You must use short domain names, such as desktop\\administrator and NOT desktop.local/administrator. | [optional] 
**external_name** | **str** | Contains the value of the key in the external store used to store the password. | [optional] 
**description** | **str** | Used to add additional information about a robot in order to better identify it. | [optional] 
**type** | **str** | The Robot type. | 
**hosting_type** | **str** | The Robot hosting type (Standard / Floating). | 
**provision_type** | **str** | The Robot provision type. | [optional] 
**password** | **str** | The Windows password associated with the machine username. | [optional] 
**credential_store_id** | **int** | The Credential Store used to store the password. | [optional] 
**user_id** | **int** | The associated user&#39;s Id. | [optional] 
**enabled** | **bool** | Specificies the state of the Robot (enabled/disabled) - a disabled robot cannot connect to Orchestrator | [optional] 
**credential_type** | **str** | The robot credentials type (Default/ SmartCard) | [optional] 
**environments** | [**list[EnvironmentDto]**](EnvironmentDto.md) | The collection of environments the robot is part of. | [optional] 
**robot_environments** | **str** | The comma separated textual representation of environment names the robot is part of. | [optional] 
**execution_settings** | **dict(str, object)** | A collection of key value pairs containing execution settings for this robot. | [optional] 
**is_external_licensed** | **bool** | Flag to indicate if the robot uses an external license | [optional] 
**limit_concurrent_execution** | **bool** | Specifies if the robot can be used concurrently on multiple machines | [optional] 
**last_modification_time** | **datetime** |  | [optional] 
**last_modifier_user_id** | **int** |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**creator_user_id** | **int** |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


