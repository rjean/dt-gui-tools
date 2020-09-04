# -*- coding: utf-8 -*-
from .baseClass import BaseEditorClass


class MapBaseObject(BaseEditorClass):
    def __init__(self, init_info):
        BaseEditorClass.__init__(self, init_info)
        self.position = {'x': init_info['pos'][0], 'y': init_info['pos'][1]}
        self.height = init_info['height']
        self.optional = init_info['optional']
        self.static = init_info['static']

    def __iter__(self):
        yield from {
            'kind': self.kind,
            'height': self.height,
            'position': self.position,
            'rotation': self.rotation,
            'optional': self.optional,
            'static': self.static
        }.items()

    def get_editable_attrs(self):
        return {
            'height': self.height,
            'position': self.position,
            'rotation': self.rotation,
            'optional': self.optional,
            'static': self.static
        }


class SignObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)


class CityObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)


class WatchTowerObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)
        self.hostname = init_info["hostname"] if "hostname" in init_info else "watchtower02" # TODO: How to init hostname?

    def get_editable_attrs(self):
        return {
            'height': self.height,
            'position': self.position,
            'rotation': self.rotation,
            'hostname': self.hostname
        }


class GroundAprilTagObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)
