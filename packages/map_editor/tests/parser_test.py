# -*- coding: utf-8 -*-
import unittest
import numpy as np

from map_parser import *
from classes.mapTile import MapTile
from classes.mapObjects import BaseEditorClass as MapObject
from map import DuckietownMap


class TestMapParser(unittest.TestCase):

    def test_empty_map_objects(self):
        objects_array = data_from_file('../maps/small_loop.yaml').get('objects')
        self.assertEqual(objects_array, None)

    def test_tile_size(self):
        tile_size = data_from_file('../maps/small_loop.yaml').get('tile_size')
        self.assertEqual(tile_size, 0.585)

    def test_tiles_to_objects(self):
        tiles_objects_array = tiles_to_objects(data_from_file('../maps/test.yaml').get('tiles'))
        new_tiles_objects_array = [[MapTile('curve_left', 180), MapTile('straight', 180)],
                                   [MapTile('straight', 90), MapTile('asphalt', 0)]]
        for tile, new_tile in zip(np.array(tiles_objects_array).flat, np.array(new_tiles_objects_array).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

    def test_map_objects_to_objects(self):
        map_objects_array = map_objects_to_objects(data_from_file('../maps/test.yaml').get('objects'))
        objects_array = [MapObject('trafficlight', position=[2.2, 2.2], rotation=45, height=0.4, optional=True, static=False)]
        for obj, new_obj in zip(map_objects_array, objects_array):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)

    def test_map_to_yaml_1(self):
        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(data_from_file('../maps/regress_4way_adam.yaml').get('tiles')))
        map.set_item_layer(map_objects_to_objects(data_from_file('../maps/regress_4way_adam.yaml').get('objects')))

        map_to_yaml(map, '../maps/test_result.yaml')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(data_from_file('../maps/test_result.yaml').get('tiles')))
        new_map.set_item_layer(map_objects_to_objects(data_from_file('../maps/test_result.yaml').get('objetcs')))

        for tile, new_tile in zip(np.array(map.get_tile_layer().data).flat, np.array(new_map.get_tile_layer().data).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

        for obj, new_obj in zip(map.get_item_layer().data, new_map.get_item_layer().data):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)

    def test_map_to_yaml_2(self):
        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(data_from_file('../maps/test.yaml').get('tiles')))
        map.set_item_layer(map_objects_to_objects(data_from_file('../maps/test.yaml').get('objects')))

        map_to_yaml(map, '../maps/test_result.yaml')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(data_from_file('../maps/test_result.yaml').get('tiles')))
        new_map.set_item_layer(map_objects_to_objects(data_from_file('../maps/test_result.yaml').get('objects')))

        for tile, new_tile in zip(np.array(map.get_tile_layer().data).flat, np.array(new_map.get_tile_layer().data).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

        for obj, new_obj in zip(map.get_item_layer().data, new_map.get_item_layer().data):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)

    def test_map_to_yaml_without_objects(self):

        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(data_from_file('../maps/regress_4way_drivable.yaml').get('tiles')))
        map.set_item_layer(map_objects_to_objects(data_from_file('../maps/regress_4way_drivable.yaml').get('objects')))

        map_to_yaml(map, '../maps/test_result.yaml')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(data_from_file('../maps/test_result.yaml').get('tiles')))
        new_map.set_item_layer(map_objects_to_objects(data_from_file('../maps/test_result.yaml').get('objects')))

        for tile, new_tile in zip(np.array(map.get_tile_layer().data).flat, np.array(new_map.get_tile_layer().data).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)
        self.assertEqual(map.get_item_layer().data, new_map.get_item_layer().data)

    def test_map_to_yaml_without_yaml(self):
        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(data_from_file('../maps/regress_4way_adam.yaml').get('tiles')))
        map.set_item_layer(map_objects_to_objects(data_from_file('../maps/regress_4way_adam.yaml').get('objects')))

        map_to_yaml(map, '../maps/test_result')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(data_from_file('../maps/test_result.yaml').get('tiles')))
        new_map.set_item_layer(map_objects_to_objects(data_from_file('../maps/test_result.yaml').get('objects')))

        for tile, new_tile in zip(np.array(map.get_item_layer().data).flat, np.array(new_map.get_item_layer().data).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

        for obj, new_obj in zip(map.get_item_layer().data, new_map.get_item_layer().data):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)


if __name__ == '__main__':
    unittest.main()
