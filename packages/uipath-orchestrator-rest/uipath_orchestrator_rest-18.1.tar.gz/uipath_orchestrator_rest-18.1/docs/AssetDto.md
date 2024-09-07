# AssetDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | An unique identifier | [optional] 
**name** | **str** | A custom name for the asset. | 
**can_be_deleted** | **bool** | States if an assets can be deleted. The default value of this property is true. | [optional] 
**value_scope** | **str** | Defines the scope of the asset. | 
**value_type** | **str** | Defines the type of value stored by the asset. | [optional] 
**value** | **str** | The textual representation of the asset value, irrespective of value type. | [optional] 
**string_value** | **str** | The value of the asset when the value type is Text. Empty when the value type is not Text. | [optional] 
**bool_value** | **bool** | The value of the asset when the value type is Bool. False when the value type is not Bool. | [optional] 
**int_value** | **int** | The value of the asset when the value type is Integer. 0 when the value type is not Integer. | [optional] 
**credential_username** | **str** | The user name when the value type is Credential. Empty when the value type is not Credential. | [optional] 
**credential_password** | **str** | The password when the value type is Credential. Empty when the value type is not Credential. | [optional] 
**external_name** | **str** | Contains the value of the key in the external store used to store the credentials. | [optional] 
**credential_store_id** | **int** | The Credential Store used to store the credentials. | [optional] 
**key_value_list** | [**list[CustomKeyValuePair]**](CustomKeyValuePair.md) | A collection of key value pairs when the type is KeyValueList. Empty when the value type is not KeyValueList. | [optional] 
**has_default_value** | **bool** | The asset has a default value set. This value will be null when set from legacy components that don&#39;t support  the PerRobot assets with default value feature. | [optional] 
**description** | **str** | The description of the asset. | [optional] 
**robot_values** | [**list[AssetRobotValueDto]**](AssetRobotValueDto.md) | The collection of asset values per robot. Empty if the asset type is Global or PerUser. | [optional] 
**user_values** | [**list[AssetUserValueDto]**](AssetUserValueDto.md) | The collection of asset values per user. Empty if the asset type is Global or PerRobot. | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) |  | [optional] 
**folders_count** | **int** | Number of folders where the asset is shared. | [optional] 
**last_modification_time** | **datetime** |  | [optional] 
**last_modifier_user_id** | **int** |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**creator_user_id** | **int** |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


