# AlertDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**notification_name** | **str** | The name of a specific type of notification, e.g. Robot.StatusChanged.NotResponding. | [optional] 
**data** | **str** | Stores data about the context in which the event occurred, in JSON format. | [optional] 
**component** | **str** | The component that raised the alert. | [optional] 
**severity** | **str** | The severity level of the alert. | 
**creation_time** | **datetime** | The date and time when the alert was generated. | [optional] 
**state** | **str** | Defines if a specified notification has been read or not.  &lt;para /&gt;Members: Unread (0) - the specified notification has not been marked as read; Read (1) - the specified notification has been marked as read. | [optional] 
**user_notification_id** | **str** | The database unique identifier for the alert notification sent to the current user. | [optional] 
**deep_link_relative_url** | **str** | Relative deep link for front-end usage.  e.g /alerts/deeplink/{alert_title}?{alert_param1}&#x3D;{alert_param1_value}&amp;{alert_param2}&#x3D;{alert_param2_value} | [optional] 
**id** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


