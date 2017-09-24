# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:09:17 2017

@author: andrew
"""

from xml.etree import ElementTree
import assist_util as au
import numpy as np


def convert_point(pt, width, height):
    # Sometimes system will generate decimals
    x = int((pt.find('x').text).split('.')[0])
    y = int((pt.find('y').text).split('.')[0])
    x = min(x, width - 1)
    y = min(y, height - 1)
    x = max(x, 0)
    y = max(y, 0)    
    return x, y


def append_polygon_dict(obj, object_dict, object_class, width, height, omit):
    '''
    Store object name and polygon points into a object dict
    Data struct of object_dict{paint_layer: ['class_name', [points of polygon]], ...}
    If there a more than one region in same paint layer, data struct will be :
        object_dict{paint_layer: [['class_name', [points of region 1]],['class_name',[points of region 2]]], ...}
    '''
    item = []
    
    occluded = obj.find('occluded').text
    if occluded == 'yes' and omit == 1:
        name = 'ignore'
    else:
        name = object_class
    
    points = obj.find('polygon').findall('pt')
    
    point_list = [convert_point(pt, width, height) for pt in points]
       
    item = au.polygon(name, point_list)
    
    layer_attribute = obj.find('attributes').text
    if layer_attribute and layer_attribute.isdigit():
        paint_layer = int(layer_attribute)
        if paint_layer in object_dict:
            object_dict[paint_layer].append(item)
        else:
            object_dict[paint_layer] = []                    
            object_dict[paint_layer].append(item)
    else:            
        pass


def xml_decode_polygon(filename, args, label_ref = None):
    """
    Read object polygon information from xml file
    """
    try:
        file_root = ElementTree.parse(filename)
        image_size = file_root.find('imagesize')
        width = int(image_size.find('ncols').text)
        height = int(image_size.find('nrows').text)        
        list_object = file_root.findall('object')
        object_dict = {}
        
        for obj in list_object:               
            if obj.find('deleted').text != '1':
                object_class = obj.find('name').text
                if label_ref:
                    if au.gray_palette[object_class][0] in label_ref:
                        append_polygon_dict(obj, object_dict, object_class, width, height, args.omit)  
                    elif object_class == 'bump':
                        append_polygon_dict(obj, object_dict, 'road', width, height, omit = 0)    
                    else:                        
                        append_polygon_dict(obj, object_dict, 'background', width, height, omit = 0)       
                else:
                    append_polygon_dict(obj, object_dict, object_class, width, height, args.omit)            

    except Exception as e:
        print('Xml file : ', filename, ' load error happened : ', e)
        height = width = 0
        object_dict = {}       
                    
    return object_dict, width, height


def del_cover(bbox_list):
    # Delete small bounding box warp into another one
    new_list = []
    for i, box in enumerate(bbox_list):
        cover_flag = 0
        for b in bbox_list[i + 1: ]:
            if b.xmin <= box.xmin and box.xmax <= b.xmax and b.ymin <= box.ymin and box.ymax <= b.ymax:
                cover_flag = 1
                break
        if not cover_flag:
            new_list.append(box)
    return new_list


def optimal_edge(bbox_list, nwidth):
    new_list = []
    index_border = nwidth - 1
    # Correct bottom edge by ratio of bounding box width and height
    for box in bbox_list:
        valid_falg = 1
        if box.xmax == index_border or box.xmin == 0:
            bw = box.xmax - box.xmin
            bh = box.ymax - box.ymin
            ratio = bw / bh
            if ratio < 0.2 or bw < 25 or bh < 25:                
                valid_falg = 0
        if valid_falg:
            new_list.append(box)
            
    return new_list


def append_bbox_list(obj, bbox_list, name, width, height, lborder, rborder, nwidth, top_offset):
    """
    Load bounding box information from xml file and append to the list
    """
    if obj.find('type') == None:
        raise TypeError('This is not bounding box object: ', name, ' id: ', obj.find('id').text)
    else:
        occluded = obj.find('occluded').text
        if occluded == 'yes':
            trunc = 1
        else:
            trunc = 0
        attributes = obj.find('attributes').text
        if attributes == '1' or attributes == '0':
            difficult = attributes        
        else:
            difficult = 'x'
        
        points = obj.find('polygon').findall('pt')
        point_list = [convert_point(pt, width, height) for pt in points]
        xmin, ymin = np.min(point_list, axis = 0)
        xmax, ymax = np.max(point_list, axis = 0)

        # If valid FOV has set
        if lborder:
            if xmax < lborder or rborder < xmin:
                return
            elif xmin < lborder and xmax < rborder:
                xmin = 0
                xmax -= lborder
            elif rborder < xmax and lborder < xmin:
                xmax = nwidth - 1
                xmin -= lborder
            elif rborder < xmax and xmin < lborder:
                xmax = nwidth - 1
                xmin = 0
            else:
                xmin -= lborder
                xmax -= lborder
        else:
            pass

        if top_offset:
            if ymax - top_offset <= 0:
                return
            else:
                ymin = max(0, ymin- top_offset)
                ymax = max(0, ymax- top_offset)

        bbox_list.append(au.bbox(name, xmin, ymin, xmax, ymax, trunc, difficult))


def xml_decode_bbox(filename, args):
    """
    Read object bounding box information from xml file
    """
    try:
        file_root = ElementTree.parse(filename)
        image_size = file_root.find('imagesize')
        width = int(image_size.find('ncols').text)
        height = int(image_size.find('nrows').text)
        list_object = file_root.findall('object')  
        lborder, rborder, nwidth = au.fov_process(args.fov, width)
        bbox_list = []
        if args.palette:
            name_list = au.component_list
        else:
            name_list = au.collect_list
        for obj in list_object:
            if obj.find('deleted').text != '1':
                name = obj.find('name').text
                if name in name_list:
                    append_bbox_list(obj, bbox_list, name, width, height, lborder, rborder, nwidth, args.crop)
                else:
                    raise IOError('Invalid name: ', name)
        if lborder:
            bbox_list = del_cover(bbox_list)
            bbox_list = optimal_edge(bbox_list, nwidth)
        if args.crop:
            height -= args.crop
            
    except Exception as e:
        print('Xml file : ', filename, ' load error happened : ', e)
        height = width = 0
        bbox_list = []
        
    return bbox_list, width, height, lborder, rborder, nwidth


def extract_bbox(height, width, item_dict):
    # convert store format, because paint layer does not make senes for bounding box
    bbox_list = []
    if item_dict:
        item_keys = list(item_dict.keys())
        item_keys.sort()
        for k in item_keys:            
            name = None
            xmin = width
            ymin = height
            xmax = 0
            ymax = 0
            for part in item_dict[k]:
                if part.name in au.collect_list:
                    name = part.name                    
                    points = part.pts               
                    np_pts = np.array(points)
                    tmp_min = np.min(np_pts, axis = 0)
                    tmp_max = np.max(np_pts, axis = 0)                    
                    xmin = min(tmp_min[0], xmin)
                    ymin = min(tmp_min[1], ymin)
                    xmax = max(tmp_max[0], xmax)
                    ymax = max(tmp_max[1], ymax)
            if name:
                bbox_list.append(au.bbox(name, xmin, ymin, xmax, ymax, 0, 0))
            
    return bbox_list