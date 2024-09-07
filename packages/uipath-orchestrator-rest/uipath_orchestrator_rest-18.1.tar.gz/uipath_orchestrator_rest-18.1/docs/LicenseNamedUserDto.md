# LicenseNamedUserDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | The license key. | [optional] 
**user_name** | **str** | The Robot&#39;s UserName. | [optional] 
**last_login_date** | **datetime** | The last date when the Robot acquired a license. | [optional] 
**machines_count** | **int** | Total number of machines where a robot with UserName is defined. | [optional] 
**is_licensed** | **bool** | If the license is in use. | [optional] 
**is_external_licensed** | **bool** | If the robot is external licensed | [optional] 
**active_robot_id** | **int** | The Id of the Robot that uses the license. | [optional] 
**machine_names** | **list[str]** | The Machine names of the defined Robot. | [optional] 
**active_machine_names** | **list[str]** | The Machine names of the connected and licensed Robot. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


