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
import shutil
import argparse
import sys

rgb_palette = {'background': (0,0,0),
               'person': (255,0,0),                
               'car': (255,255,0),
               'bump': (0,255,255),
               'road': (0,255,0),
               'parkinglots': (255,0,255),
               'obstacle': (128,0,128),
               'ignore': (255,255,255)}                 
gray_palette = {'background': (0,),
                'person': (1,),
                'car': (2,), 
                'bump': (3,), 
                'road': (4,), 
                'parkinglots': (5,),
                'obstacle': (6,),
                'ignore': (255,)}
label_palette = {0: (0,0,0),
                 1: (255,0,0),                
                 2: (255,255,0),
                 3: (0,255,255),
                 4: (0,255,0),
                 5: (255,0,255),
                 6: (128,0,128),                 
                 255: (255,255,255)}

class process_bar(object):
    def __init__(self, num_items, bar_length = 50, init_count = 0.0):
        self.__process_bar_length = bar_length
        #The factor of percent must be not integer
        self.__num_files = float(num_items)
        self.__file_count = float(init_count)
    def update(self):
        self.__file_count += 1
        percent = self.__file_count / self.__num_files
        has_done = '#' * int(percent * self.__process_bar_length)
        spaces = ' ' * (self.__process_bar_length - len(has_done))
        sys.stdout.write("\rPercent: [%s] %d%%"%(has_done + spaces, percent * 100))
        sys.stdout.flush()
    
def randomPalette(length, min, max):  
    return [ np.random.randint(min, max) for x in range(length)]

def create_png_palette():
    png_palette = np.empty((256,3), dtype = np.uint8)
    png_palette.fill(128)
    for i in label_palette:
        png_palette[i,:] = label_palette[i]

    assign_palette = list(png_palette.flatten())
    
    assert len(assign_palette) == 768

    return assign_palette

def xml_decode(filename, omit = 1):
    '''
    Read object information from xml file
    '''
    try:
        file_root = ElementTree.parse(filename)
        image_name = file_root.find('filename').text    
        image_size = file_root.find('imagesize')
        width = int(image_size.find('ncols').text)
        height = int(image_size.find('nrows').text)
        
        list_object = file_root.findall('object')
        num_object = len(list_object)
        deleted_count = 0
        object_dict = {}
        
        for obj in list_object:               
            if obj.find('deleted').text != '1':
                occluded = obj.find('occluded').text
                item = []
                if occluded == 'yes' and omit == 1:
                    name = 'ignore'
                else:
                    name = obj.find('name').text
                item.append(name)
                points = obj.find('polygon').findall('pt')
                point_list = []
                for coor in points:
                    x = int(coor.find('x').text)
                    y = int(coor.find('y').text)            
                    point_list.append((x,y))
                item.append(point_list)       
                
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
            else:
                deleted_count += 1
        
        if deleted_count == num_object:
            valid_state = False
        else:
            valid_state = True
    except Exception as e:
        print('Xml file load error happened :', e)    
        image_name = None
        height = width = 0
        object_dict = {}
        valid_state = False       
                    
    return image_name, object_dict, width, height, valid_state

def draw_on_image(filename, image_dir, dst_dir, label_image, item_dict, 
                  line_width = 3, mask_pts = None, transparent = 1, alpha = 0.2):   
    img = pi.open(os.path.join(image_dir, filename)).convert('RGB')
    if transparent:
        attach_image = label_image.convert('RGB')
        blend_image = pi.blend(img, attach_image, alpha)
        blend_image.save(os.path.join(dst_dir, filename))  
        return blend_image
    else:
        draw_img = pd.Draw(img, 'RGB') 
        item_keys = list(item_dict.keys())
        item_keys.sort()       
        for i in item_keys:
            for part in item_dict[i]:
                name = part[0]
                points = part[1]
                try:
                    draw_img.polygon(points, fill = rgb_palette[name])
                except KeyError as e:
                    print('KeyError: ', e, ', happen with file: ', filename)
                points.append(points[0])
                draw_img.line(points, fill = rgb_palette['ignore'], width = line_width)
        if mask_pts is not None:
            draw_img.polygon(mask_pts, fill = rgb_palette['ignore'])
        img.save(os.path.join(dst_dir, filename))
        return img           

def create_label(image_name, folder, item_dict, width, height, 
                 assign_palette, line_width = 3, mask_pts = None):
    label = pi.new(mode = 'L', size = (width, height), color = (0,))
    draw_label = pd.Draw(label, 'L')     
    item_keys = list(item_dict.keys())
    item_keys.sort()
    for i in item_keys:
        for part in item_dict[i]:
            name = part[0]
            points = part[1]
            try:
                draw_label.polygon(points, fill = gray_palette[name])
            except KeyError as e:
                    print('\nKeyError: ', e, ', happen with file: ', image_name)    
            points.append(points[0])
            draw_label.line(points, fill = gray_palette['ignore'], width = line_width)
        
    if mask_pts is not None:
        draw_label.polygon(mask_pts, fill = gray_palette['ignore'])
        
    label.mode = 'P'
    label.putpalette(assign_palette)
    base_name = os.path.basename(image_name)
    prefix_name = os.path.splitext(base_name)[0]
    extension = '.png'
    label_name = prefix_name + extension
    label.save(os.path.join(folder, label_name))
    
    return label

def init_generate(args):
    xml_dir = args.dir
    if xml_dir == None:
        raise IOError('Xml direcotry must be specified')
    if not os.path.exists(xml_dir):
        raise IOError('No such directory contained xml named: ', xml_dir)
        
    mask_file = args.mask
    work_dir = os.path.join(os.getcwd(),'result')
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
        
    path_fraction = xml_dir.split('/')
    if path_fraction[-1] == '':
        orignal_dir = path_fraction[-2]
    else:
        orignal_dir = path_fraction[-1]
    
    label_dir = os.path.join(work_dir, (orignal_dir + '_label'))
    if os.path.exists(label_dir):
        shutil.rmtree(label_dir)
        os.makedirs(label_dir)
    else:
        os.makedirs(label_dir)
    
    dirlist = os.listdir(xml_dir)    
    files = [x for x in dirlist if os.path.isfile(os.path.join(xml_dir,x))]
    assign_palette = create_png_palette()
    if args.mask is None:
        mask = None
    else:
        mask = xml_decode(mask_file, 0)[1][0][0][1]

    image_path = args.images
    
    if image_path == None:
        blend_dir = None
        extract_dir = None
        images = []
    else:
        if not os.path.exists(image_path):
            raise IOError('No such directory contained images named: ', image_path)
        else:
            image_list = os.listdir(image_path)
            images = [x for x in image_list if os.path.isfile(os.path.join(image_path,x))]            
            if len(images):                
                blend_dir = os.path.join(work_dir, (orignal_dir + '_blend'))                
                if os.path.exists(blend_dir):
                    shutil.rmtree(blend_dir)
                    os.makedirs(blend_dir)
                else:
                    os.makedirs(blend_dir)
                #Copy labeled images to new directory
                extract_dir = os.path.join(work_dir, (orignal_dir + '_extract'))
                
                if os.path.exists(extract_dir):
                    shutil.rmtree(extract_dir)
                    os.makedirs(extract_dir)
                else:
                    os.makedirs(extract_dir)
            else:
                print('Image directory is empty!!!!')                
    
    return (xml_dir, work_dir, orignal_dir, label_dir, files, assign_palette, mask,
            image_path, blend_dir, extract_dir, images)

def label_generate(args):

    (xml_dir, work_dir, orignal_dir, label_dir, labels, assign_palette, mask, 
     image_path, blend_dir, extract_dir, images) = init_generate(args)
   
    bar_worker = process_bar(num_items= len(labels))
    
    if image_path == None:
        for f in labels:
            xml_file_name = os.path.join(xml_dir, f)
            
            image_name, object_dict, width, height, valid_state = xml_decode(xml_file_name, args.omit)
            bar_worker.update()
            if valid_state:
                create_label(image_name, label_dir, object_dict, 
                         width, height, assign_palette, mask_pts = mask, line_width = 4)
    else: 
        num_image = len(images)
        if num_image:
            images_perfix_list = [os.path.splitext(x)[0] for x in images]
            image_extension = os.path.splitext(images[0])[1]        
                
        for f in labels:
            xml_file_name = os.path.join(xml_dir, f)    
            image_name, object_dict, width, height, valid_state = xml_decode(xml_file_name, args.omit)
            bar_worker.update()
            if valid_state:
                label = create_label(image_name, label_dir, object_dict, 
                             width, height, assign_palette, mask_pts = mask, 
                             line_width = 4)
                label_perfix_name = os.path.splitext(f)[0]           
                
                if num_image and (label_perfix_name in images_perfix_list):
                    draw_on_image(label_perfix_name + image_extension, image_path,
                    blend_dir, label, object_dict, 3, mask, args.transparent, args.alpha)
                    shutil.copy(os.path.join(image_path, 
                                (label_perfix_name + image_extension)), extract_dir)    
    print('\n')
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(                                     
    description= 'Convert xml label to image label for image segmentation',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-d','--dir', type = str, default = None,
                        help = 'The directory that contain xml label files')
    parser.add_argument('-m','--mask', type = str, default = None,
                        help = 'The mask that will be used onto every label')
    parser.add_argument('-i','--images', type = str, default = None,
                        help = 
    'The image directory, if this argument is set ,label will show on orignal image')
    parser.add_argument('-t', '--transparent', type = int, default = 1,
                        help = 'Whether draw label on orignal image transparently')
    parser.add_argument('-a', '--alpha', type = float, default = 0.2,
                        help = 'Transparent ratio')
    parser.add_argument('-o', '--omit', type = int , default = 1,
                        help = 'Whether treat the occluded object as ignore')
    args = parser.parse_args()
    label_generate(args)
