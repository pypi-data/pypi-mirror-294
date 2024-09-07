# HostAvailabilityDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**can_connect** | **bool** | Target host is reachable and a succesful TCP connection could be made on the specified port | [optional] 
**has_bad_ssl** | **bool** | Any error occurred during SSL/TLS authentication.  Includes bad certificates (name mismatch, expired certificates), unsupported protocol versions or cyphersuites | [optional] 
**connection_error** | **str** | An error code that further describes the type of connection error.  Does not include TLS/SSL errors | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


