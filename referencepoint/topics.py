from enum import Enum


class Topics(Enum):
    NEW_MAP = 'new-map'
    IMPORT_MAP = 'import-map'
    EXPORT_MAP = 'export-map'
    TOOL_SELECTED = 'tool-selected'
    MAP_CREATED = 'map-created'
