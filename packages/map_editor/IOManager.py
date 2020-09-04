# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from map_parser import *


def init_map(parent: QtWidgets.QWidget):
    input_map = './maps/empty.yaml'
    if new_map:
        map_info = data_from_file(input_map)
        parent.map.set_tile_layer(tiles_to_objects((map_info['tiles'])))
        param = map_info['objects'] if 'objects' in map_info else None
        parent.map.clear_objects_layers()
        parent.map.add_objects_to_map(map_objects_to_objects(param), parent.info_json['info'])
        parent.map.gridSize = 58.5


def open_map(parent: QtWidgets.QWidget):
    input_map = QFileDialog.getOpenFileName(parent, 'Open file', '.', filter='YAML file (*.yaml)')[0]
    if input_map:
        parent.map.name = input_map
        map_info = data_from_file(input_map)
        parent.map.set_tile_layer(tiles_to_objects((map_info['tiles'])))
        param = map_info['objects'] if 'objects' in map_info else None
        parent.map.clear_objects_layers()
        parent.map.add_objects_to_map(map_objects_to_objects(param), parent.info_json['info'])
        parent.map.gridSize = 100 * map_info['tile_size']


def save_map_as(parent: QtWidgets.QWidget):
    if parent.map.get_tile_layer():
        output_map = QFileDialog.getSaveFileName(parent, 'Save file', '.', filter='YAML file (*.yaml)')[0]
        if output_map:
            map_to_yaml(parent.map, output_map)


def save_map(parent: QtWidgets.QWidget):
    if parent.map.name:
        if parent.map.get_tile_layer():
            map_to_yaml(parent.map, parent.map.name)
    else:
        save_map_as(parent)


def export_png(parent: QtWidgets.QWidget):
    if parent.map.get_tile_layer():
        output_map = QFileDialog.getSaveFileName(parent, 'Save file', '.', filter='PNG file (*.png)')[0]
        if output_map:
            map_to_png(parent.mapviewer, output_map)


def new_map(parent: QtWidgets.QWidget):
    new_map_file = QFileDialog.getSaveFileName(parent, 'Save file', '.', filter='YAML file (*.yaml)')[0]
    input_map = './maps/empty.yaml'
    if new_map_file:
        parent.map.name = new_map_file
        map_info = data_from_file(input_map)
        parent.map.set_tile_layer(tiles_to_objects((map_info['tiles'])))
        param = map_info['objects'] if 'objects' in map_info else None
        parent.map.set_item_layer(map_objects_to_objects(param))
        map_to_yaml(parent.map, new_map_file)


def get_map_specifications(parent: QtWidgets.QWidget):
    return specifications_of_map(parent.map, parent.info_json['info'])


def get_map_materials(parent: QtWidgets.QWidget):
    return materials_of_map(parent.map, parent.info_json['info'])
