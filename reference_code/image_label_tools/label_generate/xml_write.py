# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:08:50 2017

@author: andrew
"""

import xml.dom.minidom as xd
import os.path as op


def add_node(dom, scope, node = 'None', value = '0'):
    # Create a new name scope and assign its value for xml element tree
    node_path = dom.createElement(node)
    node_value = dom.createTextNode(str(value))
    scope.appendChild(node_path)
    node_path.appendChild(node_value)
    

def create_scope(dom, root_scope, scope = 'None'):
    # Only create a new name scope
    scope = dom.createElement(scope)
    root_scope.appendChild(scope)
    return scope


def init_xml(name = 'None', height = 0, width = 0, label_perfix = 'None'):
    # Initialize a new xml element tree for writing in it
    impl = xd.getDOMImplementation()
    dom = impl.createDocument(None, name, None)
    root = dom.documentElement
    
    add_node(dom, root, 'folder', 'VOC2012')
    add_node(dom, root, 'filename', label_perfix + '.jpg')
    
    source_scope = create_scope(dom, root, 'source')
    add_node(dom, source_scope, 'database', 'The LabelMe Object Detection Database')
    
    size_scope = create_scope(dom, root, 'size')
    add_node(dom, size_scope, 'width', width)
    add_node(dom, size_scope, 'height', height)
    add_node(dom, size_scope, 'depth','3')
    
    return dom, root


def append_xml_info(dom, root, bbox, ratio):
    # Append same pattern information into xml file
    object_scope = create_scope(dom, root, 'object')
    add_node(dom, object_scope, 'name', bbox.name)
    add_node(dom, object_scope, 'pose', 'Unspecified')
    add_node(dom, object_scope, 'truncated', bbox.truncated)
    if bbox.difficult == 'x':
        add_node(dom, object_scope, 'difficult', '0')
    else:
        add_node(dom, object_scope, 'difficult', bbox.difficult)        
    bbox_scope = create_scope(dom, object_scope, 'bndbox')
    add_node(dom, bbox_scope, 'xmin', int(float(bbox.xmin) * ratio))
    add_node(dom, bbox_scope, 'ymin', int(float(bbox.ymin) * ratio))
    add_node(dom, bbox_scope, 'xmax', int(float(bbox.xmax) * ratio))
    add_node(dom, bbox_scope, 'ymax', int(float(bbox.ymax) * ratio))


def create_bbox(bbox_list, label_path, height, width, label_perfix, ratio):
    # Create a xml file and write all objects information into it.
    dom, root = init_xml('annotation', height, width, label_perfix)
    
    for bbox in bbox_list:
        append_xml_info(dom, root, bbox, ratio)
           
    with open(op.join(label_path, (label_perfix + '.xml')), 'w') as fh:
            dom.writexml(fh, addindent='  ', newl = '\n') 