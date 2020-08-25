# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('root')

TILE_LAYER_NAME = "tiles"
ITEM_LAYER_NAME = "items"


class DuckietownMap:
    name = None
    gridSize = 58.5

    def __init__(self):
        self.layer_list = [TILE_LAYER_NAME, ITEM_LAYER_NAME]
        self.layer_info = {
            TILE_LAYER_NAME: [[]],
            ITEM_LAYER_NAME: []
        }

    # Getters

    def get_tile_layer(self):
        """
        Get tile layer's data (default name define by TILE_LAYER_NAME)
        :return: list(list)
        """
        return self.get_layer(TILE_LAYER_NAME)

    def get_item_layer(self):
        """
        Get item layer's data (default name define by ITEM_LAYER_NAME)
        If item layer doesn't exist, function create it
        :return: list
        """
        layer = self.get_layer(ITEM_LAYER_NAME)
        if layer is None:   # if layer doesn't exist, layer = None
            self.set_item_layer([])
            layer = []
        return layer

    def get_layer(self, name):
        """
        Get layer's data by name
        :param name: name of layer
        :return: list, if name doesn't exist, return None
        """
        return self.layer_info.get(name, None)

    # Setters

    def set_tile_layer(self, layer):
        """
        Set tile layer's data
        :param layer: list(list)
        :return: -
        """
        self.set_layer(TILE_LAYER_NAME, layer)

    def set_item_layer(self, layer):
        """
        Set item layer's data
        :param layer: list
        :return: -
        """
        self.set_layer(ITEM_LAYER_NAME, layer)

    def set_layer(self, name, layer):
        """
        Set layer's data by name
        :param name: layer's name
        :param layer: list
        :return: -
        """
        self.layer_info[name] = layer
        if name not in self.layer_list:  # for adding new layers in future
            self.layer_list.append(name)

    # Adding elem to layers

    def add_item(self, item):
        """
        Add item to item layer (default name define by ITEM_LAYER_NAME)
        :param item: MapObject. Note: after adding specific layers, it can change
        :return: bool (looks like it always True)
        """
        return self.add_elem_to_layer(ITEM_LAYER_NAME, item)

    def add_elem_to_layer(self, name, elem):
        """
        Add elem to layer by name
        (Doesn't add elements to tile_layer due to different structure)
        :param name: layer's name
        :param elem: MapObject. Note: after adding specific layers, it can change
        :return: bool. If layer doesn't exist - False,
        """
        if name == TILE_LAYER_NAME:
            logger.warning("Don't use this method for tile layer.")
            return False
        layer = self.get_layer(name)

        if layer is not None:   # layer can exist, but be empty. get_layer return None, if layer doesn't exist
            layer.append(elem)
            return True
        else:
            logger.debug('No such layer name: {}'.format(name))
            return False
