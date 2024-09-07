# WrappedStartProcessDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**release_key** | **str** | The unique key of the release associated with the process. | [optional] 
**strategy** | **str** | States which robots from the environment are being run by the process. | [optional] 
**robot_ids** | **list[int]** | The collection of ids of specific robots selected to be run by the current process. This collection must be empty only if the start strategy is not Specific. | [optional] 
**jobs_count** | **int** | Number of pending jobs to be created in the environment, for the current process. This number must be greater than 0 only if the start strategy is JobsCount. | [optional] 
**source** | **str** | The Source of the job starting the current process. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


