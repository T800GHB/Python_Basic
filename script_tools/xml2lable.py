#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:08:48 2017

@author: andrew

This script could read polygon coordiante from a xml file and 
draw those ones and fill according to palette.
Draw result will save as 8-bits png with palette format.
In order to observe the result of drawing, draw_on_image method will
blend result on orignal image.
If some part will draw wiht same pattern on every image, we could set
mask xml file to do that.
We could call script by terminal and assign some options.
"""
from xml.etree import ElementTree
import PIL.Image as pi
import PIL.ImageDraw as pd
import numpy as np
import os
import os.path as op
import shutil
import argparse
import assist_util as au
import xml.dom.minidom as xd

def append_polygon_dict(obj, object_dict, object_class, omit):
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
    point_list = []
    for coor in points:
        #Sometimes system will generate decimals
        x = int((coor.find('x').text).split('.')[0])
        y = int((coor.find('y').text).split('.')[0])            
        point_list.append((x,y))
       
    item = au.polygon(name, point_list)
    
    layer_attribute = obj.find('attributes').text
    if layer_attribute == None:
        pass
    else:            
        paint_layer = int(layer_attribute)
        if paint_layer in object_dict.keys():
            object_dict[paint_layer].append(item)
        else:
            object_dict[paint_layer] = []                    
            object_dict[paint_layer].append(item)

def xml_decode_polygon(filename, args, label_ref = None):
    '''
    Read object polygon information from xml file
    '''
    try:
        file_root = ElementTree.parse(filename)
#        image_name = file_root.find('filename').text    
        image_size = file_root.find('imagesize')
        width = int(image_size.find('ncols').text)
        height = int(image_size.find('nrows').text)        
        list_object = file_root.findall('object')
        object_dict = {}
        
        for obj in list_object:               
            if obj.find('deleted').text != '1':
                object_class = obj.find('name').text
                if label_ref != None:
                    if au.gray_palette[object_class][0] in label_ref:
                        append_polygon_dict(obj, object_dict, object_class, args.omit)  
                    else:
                        if object_class == 'bump':
                            append_polygon_dict(obj, object_dict, 'road', omit = 0)    
                        else:                        
                            append_polygon_dict(obj, object_dict, 'background', omit = 0)       
                else:
                    append_polygon_dict(obj, object_dict, object_class, args.omit)            
                        
            else:
                pass
    except Exception as e:
        print('Xml file : '  ,filename, ' load error happened : ', e)    
#        image_name = None
        height = width = 0
        object_dict = {}       
                    
    return object_dict, width, height

def append_bbox_list(obj, bbox_list, name):
    '''
    Load bounding box information from xml file and append to the list
    '''
    if obj.find('type') == None:
        raise TypeError('This is not bounding box object: ', name, ' id: ', obj.find('id').text)
    else:
        occluded = obj.find('occluded').text
        if occluded == 'yes':
            trunc = 1
        else:
            trunc = 0
        attributes = obj.find('attributes').text
        if attributes == '1':
            difficult = 1
        else:
            difficult = 0
        points = obj.find('polygon').findall('pt')
        x_list = np.empty((4,), dtype = np.int)
        y_list = np.empty((4,), dtype = np.int)
                                  
        for i in range(4):
            #Sometimes system will generate decimals
            x = int((points[i].find('x').text).split('.')[0])
            y = int((points[i].find('y').text).split('.')[0])            
            x_list[i] = x
            y_list[i] = y
        
        bbox_list.append(au.bbox(name, x_list.min(), y_list.min(), x_list.max(), y_list.max(), trunc, difficult))

def xml_decode_bbox(filename, args, label_ref = None):
    '''
    Read object bounding box information from xml file
    '''
    try:
        file_root = ElementTree.parse(filename)
#        image_name = file_root.find('filename').text    
        image_size = file_root.find('imagesize')
        width = int(image_size.find('ncols').text)
        height = int(image_size.find('nrows').text)
        list_object = file_root.findall('object')      
        bbox_list = []

        for obj in list_object:
            if obj.find('deleted').text != '1':
                name = obj.find('name').text
                if label_ref != None:
                    if au.gray_palette[name][0] in label_ref:
                        append_bbox_list(obj, bbox_list, name)
                    else:
                        pass
                else:
                     append_bbox_list(obj, bbox_list, name)
            else:
                pass     
            
    except Exception as e:
        print('Xml file : '  ,filename, ' load error happened : ', e)    
#        image_name = None
        height = width = 0
        bbox_list = []
        
    return bbox_list, width, height

def draw_poly2bbox(filename, image_dir, dst_dir, bbox_list):
    
    img = pi.open(op.join(image_dir, filename)).convert('RGB')        
    draw_object = pd.Draw(img)
    
    for bbox in bbox_list:        
        draw_object.rectangle((bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax), outline = au.rgb_palette[bbox.name])
        draw_object.text((bbox.xmin, bbox.ymin), str(bbox.difficult), au.rgb_palette[bbox.name])
            
    img.save(op.join(dst_dir, filename))
def extract_bbox(height, width, item_dict):
    #convert store format, because paint layer does not make senes for bounding box
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
                
                tmp_name = part.name
                
                if tmp_name in au.collect_list:
                    name = tmp_name                    
                    points = part.pts                                        
                    np_pts = np.array(points)
                    tmp_min = np.min(np_pts, axis = 0)
                    tmp_max = np.max(np_pts, axis = 0)
                    if tmp_min[0] < xmin:
                        xmin = tmp_min[0]
                    if tmp_min[1] < ymin:
                        ymin = tmp_min[1]
                    if xmax < tmp_max[0]:
                        xmax = tmp_max[0]
                    if ymax < tmp_max[1]:
                        ymax = tmp_max[1]
            if name:
                bbox_list.append(au.bbox(name, xmin, ymin, xmax, ymax))
            
    return bbox_list

def add_node(dom, scope, node = 'None', value = '0'):
    #Create a new name scope and assign its value for xml element tree
    node_path = dom.createElement(node)
    node_value = dom.createTextNode(str(value))
    scope.appendChild(node_path)
    node_path.appendChild(node_value)
    

def create_scope(dom, root_scope, scope = 'None'):
    #Only create a new name scope
    scope = dom.createElement(scope)
    root_scope.appendChild(scope)
    return scope

def init_xml(name = 'None'):
    #Initialize a new xml element tree for writing in it
    impl = xd.getDOMImplementation()
    dom = impl.createDocument(None, name, None)
    root = dom.documentElement
    return dom, root
                
def create_bbox(bbox_list, label_path, height, width, label_perfix, args):
    #Create a xml file and write all objects information into it.
    dom, root = init_xml('annotation')
    
    add_node(dom, root, 'folder', 'VOC2012')
    add_node(dom, root, 'filename', label_perfix + '.jpg')
    
    source_scope = create_scope(dom, root, 'source')
    add_node(dom, source_scope, 'database', 'The LabelMe Object Detection Database')
    
    size_scope = create_scope(dom, root, 'size')
    add_node(dom, size_scope, 'depth','3')
    add_node(dom, size_scope, 'height', height)
    add_node(dom, size_scope, 'width', width)
    
    ratio = args.size
    
    for bbox in bbox_list:
        object_scope = create_scope(dom, root, 'object')
        add_node(dom, object_scope, 'name', bbox.name)
        add_node(dom, object_scope, 'pose', 'Unspecified')
        add_node(dom, object_scope, 'truncated', bbox.truncated)
        add_node(dom, object_scope, 'difficult', bbox.difficult)        
        bbox_scope = create_scope(dom, object_scope, 'bndbox')
        add_node(dom, bbox_scope, 'xmin', int(float(bbox.xmin) * ratio))
        add_node(dom, bbox_scope, 'ymin', int(float(bbox.ymin) * ratio))
        add_node(dom, bbox_scope, 'xmax', int(float(bbox.xmax) * ratio))
        add_node(dom, bbox_scope, 'ymax', int(float(bbox.ymax) * ratio))
                
    
    with open(op.join(label_path, (label_perfix + '.xml')),'w') as fh:
            dom.writexml(fh, addindent='  ', newl = '\n')           

def draw_on_image(filename, image_dir, dst_dir, label_image, item_dict, args, mask_pts = None):   
    img = pi.open(op.join(image_dir, filename)).convert('RGB')
    if args.transparent:
        attach_image = label_image.convert('RGB')
        blend_image = pi.blend(img, attach_image, args.alpha)
        blend_image.save(op.join(dst_dir, filename))  
        return blend_image
    else:
        draw_img = pd.Draw(img, 'RGB') 
        item_keys = list(item_dict.keys())
        item_keys.sort()       
        for i in item_keys:
            for part in item_dict[i]:
                name = part.name
                points = part.pts
                try:
                    draw_img.polygon(points, fill = au.rgb_palette[name])
                except KeyError as e:
                    print('KeyError: ', e, ', happen with file: ', filename)
                if args.linewidth:
                    points.append(points[0])
                    draw_img.line(points, fill = au.rgb_palette['ignore'], width = args.linewidth)
                else:
                    pass
        if mask_pts is not None:
            draw_img.polygon(mask_pts, fill = au.rgb_palette['ignore'])
        img.save(op.join(dst_dir, filename))
        return img 
    
def create_label(image_name, folder, item_dict, width, height, 
                 assign_palette,  args, mask_pts = None):
    label = pi.new(mode = 'L', size = (width, height), color = (0,))
    draw_label = pd.Draw(label, 'L')     
    item_keys = list(item_dict.keys())
    item_keys.sort()
    for i in item_keys:
        for part in item_dict[i]:
            name = part.name
            points = part.pts
            try:
                draw_label.polygon(points, fill = au.gray_palette[name])
            except KeyError as e:
                    print('\nKeyError: ', e, ', happen with file: ', image_name)
            if args.linewidth and name != 'background':
                points.append(points[0])
                draw_label.line(points, fill = au.gray_palette['ignore'], width = args.linewidth)
            else:
                pass
        
    if mask_pts is not None:
        draw_label.polygon(mask_pts, fill = au.gray_palette['ignore'])
        
    label.mode = 'P'
    label.putpalette(assign_palette)
    extension = '.png'
    label_name = image_name + extension
    if args.size != 1.0:
        re_height = int(args.size * float(height))
        re_width = int(args.size * float(width))
        final_label = label.resize((re_width, re_height), pi.NEAREST)
    else:
        final_label = label
    final_label.save(op.join(folder, label_name))
    
    return label

def copy_image(extract_dir, image_path, image_name, args):
    #Copy the orignal image or reize it than store at specific location
    if args.size != 1.0:
        org_img = pi.open(op.join(image_path, image_name))
        re_height = int(args.size * float(org_img.height))
        re_width = int(args.size * float(org_img.width))
        resize_img = org_img.resize((re_width, re_height), pi.ANTIALIAS)
        resize_img.save(op.join(extract_dir,image_name))
    else:
        shutil.copy(op.join(image_path, image_name), extract_dir)

def init_generate(args):
    xml_dir = args.dir
    if xml_dir == None:
        raise IOError('Xml direcotry must be specified')
    if not op.exists(xml_dir):
        raise IOError('No such directory contained xml named: ', xml_dir)
        
    mask_file = args.mask
    work_dir = op.join(os.getcwd(),'result')
    if not op.exists(work_dir):
        os.mkdir(work_dir)
        
    path_fraction = xml_dir.split('/')
    if path_fraction[-1] == '':
        orignal_dir = path_fraction[-2]
    else:
        orignal_dir = path_fraction[-1]
    
    label_dir = op.join(work_dir, (orignal_dir + '_label'))
    if op.exists(label_dir):
        shutil.rmtree(label_dir)
        os.makedirs(label_dir)
    else:
        os.makedirs(label_dir)
    
    dirlist = os.listdir(xml_dir)    
    files = [x for x in dirlist if op.isfile(op.join(xml_dir,x))]
    assign_palette = au.create_png_palette()
    if args.mask is None:
        mask = None
    else:
        #Second return val, first paint layer, first polygon
        mask = (xml_decode_polygon(mask_file, args)[0][0][0]).pts 
    
    if args.reference != None:        
        str_index = args.reference
        try:
            label_index = str_index.split(',')
            label_ref = [int(x) for x in label_index]
            label_ref.append(int(255))
        except ValueError as e :
            print('Specific an abnormal class index: ', e )
            exit()
    else:
        label_ref = None

    image_path = args.images
    
    if image_path == None:
        check_dir = None
        extract_dir = None
        images = []
    else:
        if not op.exists(image_path):
            raise IOError('No such directory contained images named: ', image_path)
        else:
            image_list = os.listdir(image_path)
            images = [x for x in image_list if op.isfile(op.join(image_path,x))]            
            if len(images):                
                check_dir = op.join(work_dir, (orignal_dir + '_check'))                
                if op.exists(check_dir):
                    shutil.rmtree(check_dir)
                    os.makedirs(check_dir)
                else:
                    os.makedirs(check_dir)
                #Copy labeled images to new directory
                extract_dir = op.join(work_dir, (orignal_dir + '_extract'))
                
                if op.exists(extract_dir):
                    shutil.rmtree(extract_dir)
                    os.makedirs(extract_dir)
                else:
                    os.makedirs(extract_dir)
            else:
                print('Image directory is empty!!!!')       
                
    
    return (xml_dir, work_dir, orignal_dir, label_dir, files, assign_palette, mask,
            image_path, check_dir, extract_dir, images, label_ref)

def label_generate(args):

    (xml_dir, work_dir, orignal_dir, label_dir, labels, assign_palette, mask, 
     image_path, check_dir, extract_dir, images, label_ref) = init_generate(args)
   
    bar_worker = au.process_bar(num_items= len(labels))
    
    if image_path == None:
        for f in labels:
            xml_file_name = op.join(xml_dir, f)
            
            object_dict, width, height = xml_decode_polygon(xml_file_name, args, label_ref)
            label_perfix = op.splitext(f)[0] 
            bar_worker.update()
            if object_dict:
                create_label(label_perfix, label_dir, object_dict, 
                         width, height, assign_palette,  args, mask_pts = mask)
    else: 
        num_image = len(images)
        if num_image:
            images_perfix_list = [op.splitext(x)[0] for x in images]
            image_extension = op.splitext(images[0])[1]
                
        for f in labels:
            xml_file_name = op.join(xml_dir, f)    
            object_dict, width, height = xml_decode_polygon(xml_file_name, args, label_ref)
            label_perfix = op.splitext(f)[0] 
            bar_worker.update()
            if object_dict:
                label = create_label(label_perfix, label_dir, object_dict, 
                             width, height, assign_palette, args, mask_pts = mask)                          
                
                if num_image and (label_perfix in images_perfix_list):
                    draw_on_image(label_perfix + image_extension, image_path,
                    check_dir, label, object_dict, args, mask)                    

                    copy_image(extract_dir, image_path, label_perfix + image_extension, args)    
    print('\n')

def bbox_generate(args):
    (xml_dir, work_dir, orignal_dir, label_dir, labels, assign_palette, mask, 
     image_path, check_dir, extract_dir, images, label_ref) = init_generate(args)
    
    bar_worker = au.process_bar(num_items= len(labels))
    
    #Define a inner function for different data source
    if args.bndbox == 1:
        #From polygon
        def xml_decode(xml_file_name, args, label_ref):
            object_dict, width, height = xml_decode_polygon(xml_file_name, args, label_ref)
            bbox_list = extract_bbox(height, width, object_dict)
            return bbox_list, height, width
    elif args.bndbox == 2:
        #From bounding box
        def xml_decode(xml_file_name, args, label_ref):
            bbox_list, width, height = xml_decode_bbox(xml_file_name, args, label_ref)
            return bbox_list, width, height
    else:
        raise ValueError('Specify a invalid method type: args - ', args.bndbox)
    
    if image_path:
        num_image = len(images)
        if num_image:
            images_perfix_list = [op.splitext(x)[0] for x in images]
            image_extension = op.splitext(images[0])[1]        
        for f in labels:
            xml_file_name = op.join(xml_dir, f)  
            bbox_list, width, height = xml_decode(xml_file_name, args, label_ref)
            bar_worker.update()
            if bbox_list:
                
                label_perfix = op.splitext(f)[0]          
                
                if num_image and (label_perfix in images_perfix_list):                     
                    draw_poly2bbox(label_perfix + image_extension, image_path, check_dir, bbox_list)
                    create_bbox(bbox_list, label_dir, height, width, label_perfix, args)
                    copy_image(extract_dir, image_path, label_perfix + image_extension, args)  
    else:
        raise IOError('Orignal image path must be provided!')
    print('\n')
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(                                     
    description= '''Convert xml label to image label for image segmentation
                    Class index:
                        background: 0
                        road: 1
                        car: 2
                        person: 3
                        obstacle: 4
                        parkinglots: 5
                        bump: 6
                        ignore: 255
                 ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-d','--dir', type = str, default = None,
                        help = 'The directory that contain xml label files')
    parser.add_argument('-m','--mask', type = str, default = None,
                        help = 'The mask that will be used onto every label')
    parser.add_argument('-i','--images', type = str, default = None,
                        help = '''The image directory, if this argument is set ,
                                    label will show on orignal image''')
    parser.add_argument('-t', '--transparent', type = int, default = 1,
                        help = 'Whether draw label on orignal image transparently')
    parser.add_argument('-a', '--alpha', type = float, default = 0.4,
                        help = 'Transparent ratio')
    parser.add_argument('-o', '--omit', type = int , default = 1,
                        help = 'Whether treat the occluded object as ignore')
    parser.add_argument('-r', '--reference', type = str, default = None,
                        help = '''Specific the which label will be used. 
                                Assign class index and sperate by comma''')    
    parser.add_argument('-l', '--linewidth', type = int, default = 2,
                        help = 'Ignore line width between different objects')
    parser.add_argument('-s', '--size', type = float, default = 1.0,
                        help = 'Size ratio of orignal images and labels')
    parser.add_argument('-b', '--bndbox', type = int, default = 0,
                        help = 'Wether to generate bounding box format label')
    args = parser.parse_args()
    
    if args.bndbox:
        bbox_generate(args)
    else:
        label_generate(args)
