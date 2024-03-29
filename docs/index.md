---
hide:
  - navigation
---

# Reference Point Navigation Map Builder Plugin

## Installation

The current release of the plugin can be downloaded [here](https://github.com/ReferencePointNavigation/MapCreator/releases).

| :exclamation:  In order to function correctly, the [OpenLayers](https://github.com/sourcepole/qgis-openlayers-plugin) plugin must be installed and enabled. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Map Files

The `.rpn` files generated by the Map Builder Plugin are a standard [`.zip`](https://en.wikipedia.org/wiki/ZIP_(file_format)) file which contains the map data in serialized protobuf format. Full documentation of the protocol buffer definitions can be found [here](proto.md)

![Contents of a Map file](media/map_file.png)

### Map file contents

- The `.map` file corresponds to the [Map.proto](proto.md#map) definition. This is the "index" of all of the other objects (Buildings, Paths etc.) in the `.rpn` file. Clients should extract this file first and use the `buildings` field to extract the required buildings as needed. This greatly reduces the amount of data that needs to be deserialized and loaded into memory.

- The `.bldg` file corresponds to the [Building.proto](proto.md#building) definiton.

| :exclamation:  top level paths and landmarks have not yet been implemented |
|----------------------------------------------------------------------------|

## The Plugin

The Map Builder plugin installs a toolbar in QGis that allows the user to import, edit and export maps in the `.rpn` format.

![The plugin toolbar](media/toolbar.png)

| Tool | Description |
|------|-------------|
| ![Help](media/icon.png)  | Shows the plugin about screen (not implemented)  |
| ![New](media/new.png)    | Creates a new empty map  |
| ![Open](media/open.png)  | Opens an existing map  |
| ![Save](media/save.png)  | Saves the current map  |
| ![New Building](media/new_building.png)  | Add a new building to the map  |
| ![New Navigable Space](media/new_nav_space.png)  | Add a new navigable space to a building  |
| ![New Landmark](media/new_landmark.png)  | Add a new landmark to the map  |
| ![New Path](media/new_path.png)  | Add a new path to the map  |
| ![Move](media/move_object.png)  | Move an object on the map  |
| ![Show Minimap](media/minimap.png)  | Show the minimap grid :exclamation: can be computationally expensive  |
| ![Show levels](media/levels.png)  | Show objects on different building levels  |
