# BucketDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Display name of the Bucket | 
**description** | **str** | Description of the Bucket | [optional] 
**identifier** | **str** | A stable unique identifier | 
**storage_provider** | **str** | Provider Name.  Otherwise one of the supported providers:  - FileSystem  - Azure  - Amazon  - Minio  - S3Compatible  Leave null for built-in Orchestrator host provider. | [optional] 
**storage_parameters** | **str** | Provider specific initialization parameters.  Use a $Password for where the password should be inserted.  Leave null for built-in Orchestrator host provider. | [optional] 
**storage_container** | **str** | Provider specific Container name (AWS, WASB).  Leave null for built-in Orchestrator host provider. | [optional] 
**options** | **str** | Bucket options | [optional] 
**credential_store_id** | **int** | Credential store used to keep the provider access password.  Leave null for built-in Orchestrator host provider. | [optional] 
**external_name** | **str** | The external name of the password in the credential store.  If null, it defaults to the bucket name.  Leave null for built-in Orchestrator host provider. | [optional] 
**password** | **str** | Provider specific password/secret.  It is inserted as a replacement of the $Password token in the StorageParameters.  Leave null for built-in Orchestrator host provider. | [optional] 
**folders_count** | **int** | Number of folders where the bucket is shared. | [optional] 
**tags** | [**list[TagDto]**](TagDto.md) |  | [optional] 
**id** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


