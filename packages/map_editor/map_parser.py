# -*- coding: utf-8 -*-
import codecs
import json
import re

import numpy as np

from maptile import MapTile
from mapobject import MapObject
from PyQt5 import QtGui, QtCore
from mapviewer import MapViewer
import logging

logger = logging.getLogger('root')


rotation_val = {0: 'E', 90: 'S', 180: 'W', 270: 'N'}
_translate = QtCore.QCoreApplication.translate


def get_map_objects(map):
    result = ''
    padding = '   '
    padding2 = padding + padding
    barrier = 0
    building = 0
    bus = 0
    cone = 0
    duckie = 0
    duckiebot = 0
    house = 0
    tree = 0
    trafficlight = 0
    truck = 0
    item_layer = map.get_item_layer()
    if item_layer:
        for object in item_layer:
            if object.kind == 'barrier':
                barrier += 1
            elif object.kind == 'trafficlight':
                trafficlight += 1
            elif object.kind == 'tree':
                tree += 1
            elif object.kind == 'building':
                building += 1
            elif object.kind == 'bus':
                bus += 1
            elif object.kind == 'cone':
                cone += 1
            elif object.kind == 'duckie':
                duckie += 1
            elif object.kind == 'duckiebot':
                duckiebot += 1
            elif object.kind == 'house':
                house += 1
            elif object.kind == 'truck':
                truck += 1

    result += '{}\n'.format(_translate("MainWindow", "Objects"))
    if barrier:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Barrier"), barrier, _translate("MainWindow", "pcs"))
    if building:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Building"), building, _translate("MainWindow", "pcs"))
    if bus:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Bus"), bus, _translate("MainWindow", "pcs"))
    if truck:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Truck"), truck, _translate("MainWindow", "pcs"))
    if cone:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Cone"), cone, _translate("MainWindow", "pcs"))
    if house:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "House"), house, _translate("MainWindow", "pcs"))
    if tree:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Tree"), tree, _translate("MainWindow", "pcs"))
    if duckie:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Duckie"), duckie, _translate("MainWindow", "pcs"))
    if duckiebot:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Duckiebot"), duckiebot, _translate("MainWindow", "pcs"))
    if trafficlight:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Trafficlight"), trafficlight, _translate("MainWindow", "pcs"))
    return result


def get_map_elements(map):
    result = ''
    padding = '   '
    padding2 = padding + padding

    sign_no_right_turn = sign_no_left_turn = 0
    sign_oneway_right = sign_oneway_left = 0
    sign_right_T_intersect = sign_left_T_intersect = 0
    sign_duck = 0
    sign_4_way = sign_T = parking = 0
    sign_do_not_enter = 0
    sign_pedestrian = sign_stop = sign_yield = 0
    sign_t_light_ahead = 0

    count_of_curve = count_of_str = 0
    count_of_3way = count_of_4way = 0
    count_of_floor = count_of_grass = count_of_asphalt = 0

    for tile in np.array(map.get_tile_layer()).flat:
        if '4way' in tile.kind:
            count_of_4way += 1
        elif '3way' in tile.kind:
            count_of_3way +=1
        elif 'curve' in tile.kind:
            count_of_curve += 1
        elif 'straight' in tile.kind:
            count_of_str +=1
        elif 'grass' in tile.kind:
            count_of_grass +=1
        elif 'floor' in tile.kind:
            count_of_floor += 1
        elif 'asphalt' in tile.kind:
            count_of_asphalt +=1

    item_layer = map.get_item_layer()
    if item_layer:
        for object in item_layer:
            if object.kind == 'sign_4_way_intersect':
                sign_4_way += 1
            elif object.kind == 'sign_right_T_intersect':
                sign_right_T_intersect += 1
            elif object.kind == 'sign_left_T_intersect':
                sign_left_T_intersect += 1
            elif object.kind == 'sign_T_intersection':
                sign_T += 1
            elif object.kind == 'sign_do_not_enter':
                sign_do_not_enter += 1
            elif object.kind == 'sign_duck_crossing':
                sign_duck += 1
            elif object.kind == 'sign_no_right_turn':
                sign_no_right_turn += 1
            elif object.kind == 'sign_no_left_turn':
                sign_no_left_turn += 1
            elif object.kind == 'sign_oneway_right':
                sign_oneway_right += 1
            elif object.kind == 'sign_oneway_left':
                sign_oneway_left += 1
            elif object.kind == 'sign_pedestrian':
                sign_pedestrian += 1
            elif object.kind == 'sign_stop':
                sign_stop += 1
            elif object.kind == 'sign_yield':
                sign_yield += 1
            elif object.kind == 'sign_t_light_ahead':
                sign_t_light_ahead += 1
            elif object.kind == 'sign_parking':
                parking += 1
    result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Number of T-shaped crossroads"), count_of_3way, _translate("MainWindow", "pcs"))
    result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Number of crossroads"), count_of_4way, _translate("MainWindow", "pcs"))
    result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Number of road"), count_of_str, _translate("MainWindow", "pcs"))
    result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Number of turn"), count_of_curve, _translate("MainWindow", "pcs"))
    result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Number of grass"), count_of_grass, _translate("MainWindow", "pcs"))
    result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Number of asphalt"), count_of_asphalt, _translate("MainWindow", "pcs"))
    result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Number of floor"), count_of_floor, _translate("MainWindow", "pcs"))
    
    result +='{}\n'.format(_translate("MainWindow", "Signs"))
    if sign_4_way:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Crossroad"), sign_4_way, _translate("MainWindow", "pcs"))
    if sign_T:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "T-shaped crossroads"), sign_T, _translate("MainWindow", "pcs"))
    if sign_right_T_intersect:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "T-shaped right crossroads"), sign_right_T_intersect, _translate("MainWindow", "pcs"))
    if sign_left_T_intersect:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "T-shaped left crossroads"), sign_left_T_intersect, _translate("MainWindow", "pcs"))
    if sign_do_not_enter:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Give away"), sign_do_not_enter, _translate("MainWindow", "pcs"))
    if sign_no_right_turn:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "No right turn"), sign_no_right_turn, _translate("MainWindow", "pcs"))
    if sign_no_left_turn:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "No left turn"), sign_no_left_turn, _translate("MainWindow", "pcs"))
    if sign_oneway_right:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "One-way street right"), sign_oneway_right, _translate("MainWindow", "pcs"))
    if sign_oneway_left:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "One-way street left"), sign_oneway_left, _translate("MainWindow", "pcs"))
    if sign_pedestrian:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Pedestrian crossing"), sign_pedestrian, _translate("MainWindow", "pcs"))
    if sign_duck:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Duck crossing"), sign_duck, _translate("MainWindow", "pcs"))
    if sign_stop:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Stop"), sign_stop, _translate("MainWindow", "pcs"))
    if parking:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Parking"), parking, _translate("MainWindow", "pcs"))
    if sign_yield:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Give away"), sign_yield, _translate("MainWindow", "pcs"))
    if sign_t_light_ahead:
        result += '{}{}: {} {}\n'.format(padding, _translate("MainWindow", "Traffic light"), sign_t_light_ahead, _translate("MainWindow", "pcs"))
    return result


def materials_of_map(map, specifications):
    padding = '   '
    padding2 = padding + padding
    result = '{}\n   {}\n'.format(_translate("MainWindow", "Map materials"), _translate("MainWindow", "Tape"))

    white = 0
    yellow = 0
    red = 0

    for tile in np.array(map.get_tile_layer()).flat:
        white += specifications[tile.kind]['white']
        yellow += specifications[tile.kind]['yellow']
        red += specifications[tile.kind]['red']

    if white:
        result += '{}{}: 4.8 x {} {}\n'.format(padding, _translate("MainWindow", "White"), white, _translate("MainWindow", "sm"))
    if yellow:
        result += '{}{}: 2.4 x {} {}\n'.format(padding, _translate("MainWindow", "Yellow"), yellow, _translate("MainWindow", "sm"))
    if red:
        result += '{}{}: 4.8 x {} {}\n'.format(padding, _translate("MainWindow", "Red"), red, _translate("MainWindow", "sm"))
    result += '{}\n'.format(_translate("MainWindow", "Blocks"))
    result += get_map_elements(map)
    result += get_map_objects(map)
    logger.debug("{}".format(result))
    return result


def specifications_of_map(map, specifications):
    road_length = 0
    result = "{}\n{}\n".format(_translate("MainWindow", "Map characteristics"), _translate("MainWindow", "Roads"))
    for tile in np.array(map.get_tile_layer()).flat:
        road_length += specifications[tile.kind]['length']

    result += '      {}: {} {}\n'.format(_translate("MainWindow", "Road len"), road_length, _translate("MainWindow", "sm"))
    result += get_map_elements(map)
    logger.debug("{}".format(result))
    return result


def map_to_png(map, map_name):
    if '.png' not in map_name:
        map_name = map_name + '.png'
    tile_layer = map.get_tile_layer()
    item_layer = map.get_item_layer()

    height = len(tile_layer)
    width = len(tile_layer[0])
    mergedImage = QtGui.QImage(width * map.gridSize, height * map.gridSize, QtGui.QImage.Format_RGB32)
    pt = QtGui.QPainter(mergedImage)
    transform = QtGui.QTransform()
    transform.translate(0, 0)
    pt.setTransform(transform, False)
    for y in range(len(tile_layer)):
        for x in range(len(tile_layer[y])):
            angle = tile_layer[y][x].rotation
            pt.translate(x * map.gridSize, y * map.gridSize)
            pt.drawRect(QtCore.QRectF(0, 0, map.gridSize, map.gridSize))
            pt.rotate(angle)
            if angle == 90:
                pt.translate(0, -map.gridSize)
            elif angle == 180:
                pt.translate(-map.gridSize, -map.gridSize)
            elif angle == 270:
                pt.translate(-map.gridSize, 0)
            pt.drawImage(QtCore.QRectF(0, 0, map.gridSize, map.gridSize),
                              MapViewer.tileSprites[tile_layer[y][x].kind])
            pt.setTransform(transform, False)

    item_layer = map.get_item_layer()
    if item_layer:
        for s in item_layer:
            if MapViewer.objects.__contains__(s.kind):
                pt.drawImage(
                    QtCore.QRectF(map.gridSize * MapViewer.sc * s.position['x'],
                                  map.gridSize * MapViewer.sc * s.position['y'],
                                  map.gridSize * MapViewer.sc / 2, map.gridSize * MapViewer.sc / 2),
                    MapViewer.objects[s.kind])
    pt.resetTransform()

    mergedImage.save(map_name, "png")
    pt.end()


def map_to_yaml(map, map_name):
    if '.yaml' not in map_name:
        map_name = map_name + '.yaml'
    f = open(map_name, 'w')
    f.write('tiles:\n')
    for tile_string in map.get_tile_layer():
        f.write('- [')
        for tile in tile_string:
            f.write(tile.kind)
            if tile.rotation == 0:
                if tile.kind != 'empty' and tile.kind != 'asphalt' and tile.kind != 'grass' and tile.kind != 'floor' and tile.kind != '4way':
                    f.write('/' + rotation_val[tile.rotation])
            else:
                f.write('/' + rotation_val[tile.rotation])
            if tile_string.index(tile) != len(tile_string) - 1:
                f.write(' , ')
        f.write(']\n')
    item_layer = map.get_item_layer()
    if item_layer:
        f.write('\nobjects:')
        for map_object in item_layer:
            f.write('\n- ')
            f.write('kind: ' + map_object.kind)
            f.write('\n  pos: [' + str(map_object.position['x']) + ', ' + str(map_object.position['y']) + ']')
            f.write('\n  rotate: ' + str(map_object.rotation))
            f.write('\n  height: ' + str(map_object.height))
            if map_object.optional:
                f.write('\n  optional: true')
            if not map_object.static:
                f.write('\n  static: False')
            f.write('\n')
    f.write('\ntile_size: 0.585')
    f.close()


def tiles_to_objects(tiles):
    tiles_objects_array = []
    for tile_string in tiles:
        tiles_object_string = []
        for tile in tile_string:
            tiles_object_string.append(MapTile(tile['kind'], tile['rotate']))
        tiles_objects_array.append(tiles_object_string)
    return tiles_objects_array


def map_objects_to_objects(map_objects):
    map_objects_array = []
    if not map_objects:
        return map_objects_array
    for object in map_objects:
        x, y = re.sub(r"[\[\]]", "", object['pos']).split(',')
        position = [float(x), float(y)]
        rotation = float(object['rotate'])
        height = float(object['height'])
        optional = True if object['optional'] == 'true' else False
        static = True if object['static'] == 'True' else False
        map_objects_array.append(MapObject(object['kind'], position, rotation, height, optional, static))
    return map_objects_array


def get_tiles(name):
    tiles_array = []
    try:
        f = open(name, 'r')
    except IOError:
        logger.debug("{}".format(_translate("MainWindow", "Could not open file!")))
        return None

    while True:
        map_line = f.readline()
        if 'tiles:' in map_line != -1:
            break

    map_line = f.readline()
    while map_line[0] == '-':
        map_line = re.sub(r"[ \t\[\]\-\n]", "", map_line)
        tiles = map_line.split(',')

        tile_string = []
        for tile in tiles:
            if tile == "":
                continue
            tile_object = {}
            if '/' in tile != -1:
                kind, rotate = tile.split('/')
                tile_object['kind'] = kind
                for angle, word in rotation_val.items():
                    if word == rotate:
                        tile_object['rotate'] = angle
            else:
                tile_object['kind'] = tile
                tile_object['rotate'] = 0
            tile_string.append(tile_object)
        tiles_array.append(tile_string)
        map_line = f.readline()

    f.close()
    return tiles_array


def get_objects(name):
    objects_array = []
    try:
        f = open(name, 'r')
    except IOError:
        logger.debug("{}".format(_translate("MainWindow", "Could not open file!")))
        return None

    map_line = f.readline()
    while map_line:
        if 'objects:' in map_line != -1:
            break
        map_line = f.readline()

    if not map_line:
        f.close()
        return None

    while map_line[0] != 't':
        if map_line[0] == '-':
            map_object = {}
            while True:
                map_line = re.sub(r"[ \t\n-]", "", map_line)
                splits_line = map_line.split(':')
                map_object[splits_line[0]] = splits_line[1]
                map_line = f.readline()

                if map_line[0] == '-' or map_line[0] == 't' or map_line[0] == "\n":
                    if 'optional' not in map_object:
                        map_object['optional'] = 'false'
                    if 'static' not in map_object:
                        map_object['static'] = 'True'
                    objects_array.append(map_object)
                    break
        else:
            map_line = f.readline()
    f.close()
    return objects_array


def get_tile_size(name):
    try:
        f = open(name, 'r')
    except IOError:
        logger.debug("{}".format(_translate("MainWindow", "Could not open file!")))
        return None

    while True:
        map_line = f.readline()
        if 'tile_size:' in map_line != -1:
            break
    map_line = map_line.split(':')

    f.close()
    return float(map_line[1])
