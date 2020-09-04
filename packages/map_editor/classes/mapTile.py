# -*- coding: utf-8 -*-

from .baseClass import BaseEditorClass


class MapTile(BaseEditorClass):
    def __init__(self, kind, rotation=0):
        BaseEditorClass.__init__(self, dict(kind=kind, rotate=rotation))
