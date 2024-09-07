# DefaultCredentialStoreDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_type** | **str** | This enum describes the type of resources that can be stored in the Credential Store. When  a new resource type is added, the default needs to be initialized in 3 places:  1. Existing tenants: At migration time.  2. Default tenant: At seed time in DefaultTenantCreator.cs.  3. New tenants: In TenantService.cs. | 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


