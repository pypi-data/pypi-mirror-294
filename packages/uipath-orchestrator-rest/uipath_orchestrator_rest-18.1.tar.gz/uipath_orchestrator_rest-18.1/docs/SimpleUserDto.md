# SimpleUserDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the person for which the user is created. | [optional] 
**surname** | **str** | The surname of the person for which the user is created. | [optional] 
**user_name** | **str** | The name used to login to Orchestrator. | [optional] 
**domain** | **str** | The domain from which the user is imported | [optional] 
**directory_identifier** | **str** | The directory identifier from which the user is imported | [optional] 
**full_name** | **str** | The full name of the person constructed with the format Name Surname. | [optional] 
**email_address** | **str** | The e-mail address associated with the user. | [optional] 
**is_email_confirmed** | **bool** | States if the email address is valid or not. | [optional] 
**last_login_time** | **datetime** | The date and time when the user last logged in, or null if the user never logged in. | [optional] 
**is_active** | **bool** | States if the user is active or not. An inactive user cannot login to Orchestrator. | [optional] 
**creation_time** | **datetime** | The date and time when the user was created. | [optional] 
**authentication_source** | **str** | The source which authenticated this user. | [optional] 
**password** | **str** | The password used during application login. | [optional] 
**is_external_licensed** | **bool** |  | [optional] 
**user_roles** | [**list[UserRoleDto]**](UserRoleDto.md) | The collection of roles associated with the user. | [optional] 
**roles_list** | **list[str]** | The collection of role names associated with the user. | [optional] 
**login_providers** | **list[str]** | The collection of entities that can authenticate the user. | [optional] 
**organization_units** | [**list[OrganizationUnitDto]**](OrganizationUnitDto.md) | The collection of organization units associated with the user. | [optional] 
**tenant_id** | **int** | The id of the tenant owning the user. | [optional] 
**tenancy_name** | **str** | The name of the tenant owning the user. | [optional] 
**tenant_display_name** | **str** | The display name of the tenant owning the user. | [optional] 
**tenant_key** | **str** | The key of the tenant owning the user. | [optional] 
**type** | **str** | The user type. | [optional] 
**provision_type** | **str** | The user type. | [optional] 
**license_type** | **str** | The user&#39;s license type. | [optional] 
**robot_provision** | [**AttendedRobotDto**](AttendedRobotDto.md) |  | [optional] 
**unattended_robot** | [**UnattendedRobotDto**](UnattendedRobotDto.md) |  | [optional] 
**notification_subscription** | [**UserNotificationSubscription**](UserNotificationSubscription.md) |  | [optional] 
**key** | **str** | Unique key for a user | [optional] 
**may_have_user_session** | **bool** | Specifies whether this user is allowed to have a User session (default: true) | [optional] 
**may_have_robot_session** | **bool** | Specifies whether this user is allowed to have an Attended Robot attached (default: true) | [optional] 
**may_have_unattended_session** | **bool** | Specifies whether this user is allowed to have an Unattended Robot attached (default: false) | [optional] 
**may_have_personal_workspace** | **bool** | Specifies whether this user is allowed to have a Personal Workspace | [optional] 
**restrict_to_personal_workspace** | **bool** | Restrict to personal workspace view | [optional] 
**update_policy** | [**UpdatePolicyDto**](UpdatePolicyDto.md) |  | [optional] 
**account_id** | **str** |  | [optional] 
**last_modification_time** | **datetime** |  | [optional] 
**last_modifier_user_id** | **int** |  | [optional] 
**creator_user_id** | **int** |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


