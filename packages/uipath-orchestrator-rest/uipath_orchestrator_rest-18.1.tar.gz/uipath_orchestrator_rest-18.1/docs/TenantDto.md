# TenantDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the tenant. | [optional] 
**key** | **str** | Unique Key of the tenant. | [optional] 
**display_name** | **str** | Display name of the the tenant | [optional] 
**admin_email_address** | **str** | Default tenant&#39;s admin user account email address. | [optional] 
**admin_name** | **str** | Default tenant&#39;s admin user account name. | [optional] 
**admin_surname** | **str** | Default tenant&#39;s admin user account surname. | [optional] 
**admin_user_key** | **str** | Default tenant&#39;s admin user account key. | [optional] 
**admin_password** | **str** | Default tenant&#39;s admin user account password. Only valid for create/update operations. | [optional] 
**last_login_time** | **datetime** | The last time a user logged in this tenant. | [optional] 
**is_active** | **bool** | Specifies if the tenant is active or not. | [optional] 
**accepted_domains_list** | **list[str]** | DEPRECATED. Accepted DNS list. | [optional] 
**has_connection_string** | **bool** | DEPRECATED. Specifies if the the tenant has a connection string defined | [optional] 
**connection_string** | **str** | DEPRECATED. DB connection string | [optional] 
**license** | [**TenantLicenseDto**](TenantLicenseDto.md) |  | [optional] 
**organization_name** | **str** | Organization Name of the tenant. | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


