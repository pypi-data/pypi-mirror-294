# TransactionDataDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the queue in which to search for the next item or in which to insert the item before marking it as InProgress and sending it to the robot. | [optional] 
**robot_identifier** | **str** | The unique key identifying the robot that sent the request. | [optional] 
**specific_content** | **dict(str, object)** | If not null a new item will be added to the queue with this content before being moved to InProgress state and returned to the robot for processing.  &lt;para /&gt;If null the next available item in the list will be moved to InProgress state and returned to the robot for processing. | [optional] 
**defer_date** | **datetime** | The earliest date and time at which the item is available for processing. If empty the item can be processed as soon as possible. | [optional] 
**due_date** | **datetime** | The latest date and time at which the item should be processed. If empty the item can be processed at any given time. | [optional] 
**reference** | **str** | An optional, user-specified value for queue item identification. | [optional] 
**reference_filter_option** | **str** | Declares the strategy used to filter the Reference value. | [optional] 
**parent_operation_id** | **str** | Operation id which created the queue item. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


