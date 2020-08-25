# -*- coding: utf-8 -*-
class MapObject:

    #position = {'x': 0, 'y': 0}
    def __init__(self, kind, position=(0.0, 0.0), rotation=0, height=1, optional=False, static=True):
        self.kind = kind
        self.position = {}
        self.position['x'], self.position['y'] = position
        self.rotation = rotation
        self.height = height
        self.optional = optional
        self.static = static
