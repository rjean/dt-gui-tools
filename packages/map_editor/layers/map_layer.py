from layers.layer_type import LayerType
from layers.relations import get_class_by_object_type
from layers.relations import LAYER_TYPE_WITH_OBJECTS


import logging

logger = logging.getLogger('root')


class MapLayer:
    def __init__(self, layer_type: LayerType, layer_data: list, name=''):
        self.name = name if name else layer_type.value
        self.type = layer_type
        self.data = layer_data
        self.visible = True

    def __iter__(self):
        yield from {
            'name': self.name,
            'type': str(self.type),
            'data': self.get_processed_layer_data(),
        }.items()

    def add_elem(self, elem):
        """
        Add element to layer's data
        :param elem: elem for adding
        :return: -
        """
        self.data.append(elem)

    def get_processed_layer_data(self):
        """
        Get layer data as dict()
        :return: dict
        """
        def process_data(data):
            """
            Process list of data
            :param data: list(), layer's data
            :return: list of dict()
            """
            processed_data = []
            for elem in data:
                processed_data.append(dict(elem))  # TODO: __iter__ for MapObject
            return processed_data

        if self.type == LayerType.TILES:
            layer_data = []
            for row in self.data:
                layer_data.append(process_data(row))
            return layer_data
        else:
            return process_data(self.data)

    def get_objects(self):
        """
        Get layer's objects
        If layer_type doesn't support objects return empty generator TODO: add exceptions
        :return: generator
        """
        if self.type not in LAYER_TYPE_WITH_OBJECTS:
            logger.info("Layer type {} doesn't support objects. Allowed types: {}".format(self.type, LAYER_TYPE_WITH_OBJECTS))
            yield from ()
        else:
            for layer_object in self.data:
                yield layer_object

    @staticmethod
    def create_layer_object(object_type, object_data):
        return get_class_by_object_type(object_type)(object_data)
