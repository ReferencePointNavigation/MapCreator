# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [Building.proto](#Building-proto)
    - [Building](#referencepoint-proto-Building)
  
- [Coordinates.proto](#Coordinates-proto)
    - [Coordinates](#referencepoint-proto-Coordinates)
  
- [Floor.proto](#Floor-proto)
    - [Floor](#referencepoint-proto-Floor)
  
- [Landmark.proto](#Landmark-proto)
    - [Landmark](#referencepoint-proto-Landmark)
  
    - [Landmark.LandmarkType](#referencepoint-proto-Landmark-LandmarkType)
  
- [Map.proto](#Map-proto)
    - [Map](#referencepoint-proto-Map)
    - [Map.BuildingsEntry](#referencepoint-proto-Map-BuildingsEntry)
  
- [MapService.proto](#MapService-proto)
    - [MapService](#referencepoint-proto-MapService)
  
- [Minimap.proto](#Minimap-proto)
    - [Minimap](#referencepoint-proto-Minimap)
    - [Minimap.Tile](#referencepoint-proto-Minimap-Tile)
  
- [NavigableSpace.proto](#NavigableSpace-proto)
    - [NavigableSpace](#referencepoint-proto-NavigableSpace)
    - [Ring](#referencepoint-proto-Ring)
  
- [Particle.proto](#Particle-proto)
    - [Particle](#referencepoint-proto-Particle)
  
- [Path.proto](#Path-proto)
    - [Path](#referencepoint-proto-Path)
  
- [Polygon.proto](#Polygon-proto)
    - [Polygon](#referencepoint-proto-Polygon)
  
- [Route.proto](#Route-proto)
    - [Route](#referencepoint-proto-Route)
  
- [Step.proto](#Step-proto)
    - [Step](#referencepoint-proto-Step)
  
- [Telemetry.proto](#Telemetry-proto)
    - [TelemetryData](#referencepoint-proto-TelemetryData)
    - [TelemetryData.Filter](#referencepoint-proto-TelemetryData-Filter)
    - [TelemetrySummary](#referencepoint-proto-TelemetrySummary)
    - [UUID](#referencepoint-proto-UUID)
  
    - [TelemetryData.FilterType](#referencepoint-proto-TelemetryData-FilterType)
  
    - [Telemetry](#referencepoint-proto-Telemetry)
  
- [Scalar Value Types](#scalar-value-types)



<a name="Building-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Building.proto



<a name="referencepoint-proto-Building"></a>

### Building
Represents a physical enclosed structure with navigable spaces.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| boundary | [Coordinates](#referencepoint-proto-Coordinates) | repeated | The building&#39;s boundary |
| name | [string](#string) |  | The building&#39;s name. |
| floors | [Floor](#referencepoint-proto-Floor) | repeated | An array of the floors of this building. |





 

 

 

 



<a name="Coordinates-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Coordinates.proto



<a name="referencepoint-proto-Coordinates"></a>

### Coordinates
The protobuf for the Coordinates class used to define points in the map.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| x | [double](#double) |  | The x coordinate. |
| y | [double](#double) |  | The y coordinate. |





 

 

 

 



<a name="Floor-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Floor.proto



<a name="referencepoint-proto-Floor"></a>

### Floor
The protobuf definition for the Floor class.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| number | [int32](#int32) |  | The floor&#39;s number. |
| landmarks | [Landmark](#referencepoint-proto-Landmark) | repeated | This floor&#39;s landmarks. |
| navigableSpaces | [NavigableSpace](#referencepoint-proto-NavigableSpace) | repeated | The navigable spaces of this floor. |
| minimap | [Minimap](#referencepoint-proto-Minimap) |  | The minimap representing the navigability of this floor. |





 

 

 

 



<a name="Landmark-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Landmark.proto



<a name="referencepoint-proto-Landmark"></a>

### Landmark
The protobuf definition for the Landmark class. Landmarks are used by the BuildingMap protobufs 
as a variable to represent doors, stairs, etc..


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| location | [Coordinates](#referencepoint-proto-Coordinates) |  | The landmark&#39;s x,y coordinates. |
| name | [string](#string) |  | The landmark&#39;s name. |
| type | [Landmark.LandmarkType](#referencepoint-proto-Landmark-LandmarkType) |  | The object the landmark represents (see LandmarkType enum) |
| particles | [Coordinates](#referencepoint-proto-Coordinates) | repeated | Particles used to define an accessible area close to the landmark. |
| description | [string](#string) |  | a short description of the landmark |





 


<a name="referencepoint-proto-Landmark-LandmarkType"></a>

### Landmark.LandmarkType
The different types landmarks.

| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| DOOR | 1 |  |
| HALLWAY_INTERSECTION | 2 |  |
| STAIRS | 3 |  |
| ELEVATOR | 4 |  |


 

 

 



<a name="Map-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Map.proto



<a name="referencepoint-proto-Map"></a>

### Map



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| minCoordinates | [Coordinates](#referencepoint-proto-Coordinates) |  | The map&#39;s minimum coordinates. |
| maxCoordinates | [Coordinates](#referencepoint-proto-Coordinates) |  | The map&#39;s maximum coordinates. |
| name | [string](#string) |  | the name of the map |
| description | [string](#string) |  | a brief description of the map |
| buildings | [Map.BuildingsEntry](#referencepoint-proto-Map-BuildingsEntry) | repeated | the set of buildings contained in the map |
| paths | [Path](#referencepoint-proto-Path) | repeated | the set of paths contained in the map |
| landmarks | [Landmark](#referencepoint-proto-Landmark) | repeated | the set of Landmarks not contained in buildings |






<a name="referencepoint-proto-Map-BuildingsEntry"></a>

### Map.BuildingsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [Polygon](#referencepoint-proto-Polygon) |  |  |





 

 

 

 



<a name="MapService-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## MapService.proto


 

 

 


<a name="referencepoint-proto-MapService"></a>

### MapService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| ListMaps | [Coordinates](#referencepoint-proto-Coordinates) | [Map](#referencepoint-proto-Map) stream |  |

 



<a name="Minimap-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Minimap.proto



<a name="referencepoint-proto-Minimap"></a>

### Minimap
The protobuf definition for the Minimap class. Minimaps are used in the Floor protobuf class
in order to speed up landmark search and help discretize navigation.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sideSize | [double](#double) |  | The size of the minimap&#39;s tile&#39;s side. |
| rows | [int32](#int32) |  | The number of rows in the minimap. |
| columns | [int32](#int32) |  | The number of columns in the minimap. |
| minCoordinates | [Coordinates](#referencepoint-proto-Coordinates) |  | The minimap&#39;s minimum coordinates. */ |
| tiles | [Minimap.Tile](#referencepoint-proto-Minimap-Tile) | repeated | The tiles of the minimap. |






<a name="referencepoint-proto-Minimap-Tile"></a>

### Minimap.Tile
The tiles used in minimap that a hold landmark information for a discreet amount of space.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| row | [int32](#int32) |  | The tile&#39;s row it is placed in the minimap. |
| column | [int32](#int32) |  | The tile&#39;s column it is placed in the minimap. |
| landmarks | [int32](#int32) | repeated | The closest landmarks to this tile. This is the index of the corresponding landmark in the collection of landmarks stored in the corresponding floor. |





 

 

 

 



<a name="NavigableSpace-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## NavigableSpace.proto



<a name="referencepoint-proto-NavigableSpace"></a>

### NavigableSpace
The protobuf that defines the NavigableSpace class.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| outerBoundary | [Coordinates](#referencepoint-proto-Coordinates) | repeated | The outer polygon that defines the navigable space. |
| rings | [Ring](#referencepoint-proto-Ring) | repeated | The inner rings that define the non navigable spaces within the polygon. |






<a name="referencepoint-proto-Ring"></a>

### Ring
The protobuf that defines the Ring class.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| polygon | [Coordinates](#referencepoint-proto-Coordinates) | repeated | The inner rings of the navigable space which are inaccessible. |





 

 

 

 



<a name="Particle-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Particle.proto



<a name="referencepoint-proto-Particle"></a>

### Particle



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| step | [double](#double) |  |  |
| mean_x | [double](#double) |  |  |
| mean_y | [double](#double) |  |  |
| cov_x | [double](#double) |  |  |
| cov_xy | [double](#double) |  |  |
| cov_y | [double](#double) |  |  |





 

 

 

 



<a name="Path-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Path.proto



<a name="referencepoint-proto-Path"></a>

### Path



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| steps | [Step](#referencepoint-proto-Step) | repeated |  |





 

 

 

 



<a name="Polygon-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Polygon.proto



<a name="referencepoint-proto-Polygon"></a>

### Polygon



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| vertices | [Coordinates](#referencepoint-proto-Coordinates) | repeated |  |





 

 

 

 



<a name="Route-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Route.proto



<a name="referencepoint-proto-Route"></a>

### Route



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| from | [Landmark](#referencepoint-proto-Landmark) |  |  |
| to | [Landmark](#referencepoint-proto-Landmark) |  |  |
| path | [Path](#referencepoint-proto-Path) |  |  |





 

 

 

 



<a name="Step-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Step.proto



<a name="referencepoint-proto-Step"></a>

### Step



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| time | [uint64](#uint64) |  |  |
| mean_x | [double](#double) |  |  |
| mean_y | [double](#double) |  |  |
| particles | [Particle](#referencepoint-proto-Particle) | repeated |  |





 

 

 

 



<a name="Telemetry-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## Telemetry.proto
Copyright 2019 Reference Point Navigation
@author: Chris Daley


<a name="referencepoint-proto-TelemetryData"></a>

### TelemetryData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| route_id | [UUID](#referencepoint-proto-UUID) |  |  |
| time | [int64](#int64) |  |  |
| mean_x | [double](#double) |  |  |
| mean_y | [double](#double) |  |  |
| particles | [TelemetryData.Filter](#referencepoint-proto-TelemetryData-Filter) | repeated |  |
| filter_type | [TelemetryData.FilterType](#referencepoint-proto-TelemetryData-FilterType) |  |  |






<a name="referencepoint-proto-TelemetryData-Filter"></a>

### TelemetryData.Filter



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| step | [double](#double) |  |  |
| mean_x | [double](#double) |  |  |
| mean_y | [double](#double) |  |  |
| cov_x | [double](#double) |  |  |
| cov_xy | [double](#double) |  |  |
| cov_y | [double](#double) |  |  |






<a name="referencepoint-proto-TelemetrySummary"></a>

### TelemetrySummary



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| data_count | [int32](#int32) |  |  |
| elapsed_time | [int32](#int32) |  |  |






<a name="referencepoint-proto-UUID"></a>

### UUID



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |





 


<a name="referencepoint-proto-TelemetryData-FilterType"></a>

### TelemetryData.FilterType


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| PARTICLE | 1 |  |
| KALMAN | 2 |  |


 

 


<a name="referencepoint-proto-Telemetry"></a>

### Telemetry
The Telemetry service captures telemetry data from debug clients

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| RecordRoute | [Route](#referencepoint-proto-Route) | [UUID](#referencepoint-proto-UUID) |  |
| RecordData | [TelemetryData](#referencepoint-proto-TelemetryData) stream | [TelemetrySummary](#referencepoint-proto-TelemetrySummary) |  |

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

