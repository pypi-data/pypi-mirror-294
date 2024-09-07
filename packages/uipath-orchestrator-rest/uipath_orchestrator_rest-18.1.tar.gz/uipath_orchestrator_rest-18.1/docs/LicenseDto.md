# LicenseDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**host_license_id** | **int** |  | [optional] 
**id** | **int** | License Id | [optional] 
**expire_date** | **int** | License expiration date in Epoch format | [optional] 
**grace_period_end_date** | **int** | License grace period end date in Epoch format | [optional] 
**grace_period** | **int** | Number of grace period days | [optional] 
**version_control** | **str** | The product version which can use this license | [optional] 
**allowed** | **dict(str, int)** | Contains the number of allowed licenses for each type | [optional] 
**used** | **dict(str, int)** | Contains the number of used licenses for each type | [optional] 
**attended_concurrent** | **bool** | States whether the license is Attended Concurrent | [optional] 
**development_concurrent** | **bool** | States whether the license is Development Concurrent | [optional] 
**studio_x_concurrent** | **bool** | States whether the license is Studio Business Concurrent | [optional] 
**studio_pro_concurrent** | **bool** | States whether the license is Studio Pro Concurrent | [optional] 
**licensed_features** | **list[str]** | What features are licensed (valid for individually-licensed features, like Analytics) | [optional] 
**is_registered** | **bool** | True if the current tenant is registered with a license. False otherwise. | [optional] 
**is_community** | **bool** | True if the current tenant is registered with a community license. | [optional] 
**is_pro_or_enterprise** | **bool** | True if the current tenant is registered with a pro license. | [optional] 
**subscription_code** | **str** | The license subscription code | [optional] 
**subscription_plan** | **str** | The license subscription plan | [optional] 
**is_expired** | **bool** | States whether the license is still valid or not. | [optional] 
**creation_time** | **datetime** | The date when the license was uploaded. | [optional] 
**code** | **str** | The license code. | [optional] 
**user_licensing_enabled** | **bool** | Whether user licensing is enabled or not. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


