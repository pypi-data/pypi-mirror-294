# UnattendedRobotDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_name** | **str** | The UserName used to authenticate on the Host Machine. | [optional] 
**password** | **str** | The Password used to authenticate on the Host Machine. | [optional] 
**credential_store_id** | **int** | The Credential Store used to store the password. | [optional] 
**credential_type** | **str** | The robot credentials type (Default/ SmartCard) | [optional] 
**credential_external_name** | **str** | Contains the value of the key in the external store used to store the password. | [optional] 
**execution_settings** | **dict(str, object)** | An object containing execution settings for the Robot. | [optional] 
**limit_concurrent_execution** | **bool** | Specifies if the robot can be used concurrently on multiple machines | [optional] 
**robot_id** | **int** | The actual Id of the provisioned Robot. | [optional] 
**machine_mappings_count** | **int** | Number of assigned machine mappings. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


