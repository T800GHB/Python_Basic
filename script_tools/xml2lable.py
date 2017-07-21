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

import os
import os.path as op
import shutil
import argparse
import assist_util as au
import xml_write as xw
import xml_read as xr
import draw_mark as dm
    
def init_generate(args):
    xml_dir = args.dir
        
    result_dir = op.join(os.getcwd(),'result')
    if not op.exists(result_dir):
        os.mkdir(result_dir)
        
    path_fraction = xml_dir.split('/')
    if path_fraction[-1] == '':
        orignal_dir = path_fraction[-2]
    else:
        orignal_dir = path_fraction[-1]
    
    label_dir = op.join(result_dir, (orignal_dir + '_label'))
    if op.exists(label_dir):
        shutil.rmtree(label_dir)
        os.makedirs(label_dir)
    else:
        os.makedirs(label_dir)
    
    dirlist = os.listdir(xml_dir)    
    files = [x for x in dirlist if op.isfile(op.join(xml_dir,x))]
    assign_palette = au.create_png_palette()
    
    mask_file = args.mask
    if args.mask:
        mask = (xr.xml_decode_polygon(mask_file, args)[0][0][0]).pts 
    else:        
        mask = None
    
    if args.reference:        
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
    
    if args.images:
        if not op.exists(args.images):
            raise IOError('No such directory contained images named: ', args.images)
        else:
            image_list = os.listdir(args.images)
            images = [x for x in image_list if op.isfile(op.join(args.images,x))]            
            if len(images):                
                check_dir = op.join(result_dir, (orignal_dir + '_check'))                
                if op.exists(check_dir):
                    shutil.rmtree(check_dir)
                    os.makedirs(check_dir)
                else:
                    os.makedirs(check_dir)
                #Copy labeled images to new directory
                extract_dir = op.join(result_dir, (orignal_dir + '_extract'))
                
                if op.exists(extract_dir):
                    shutil.rmtree(extract_dir)
                    os.makedirs(extract_dir)
                else:
                    os.makedirs(extract_dir)
            else:
                print('Image directory is empty!!!!')        
    else:
        check_dir = None
        extract_dir = None
        images = []              
    
    return (xml_dir, label_dir, files, assign_palette, mask,
            args.images, check_dir, extract_dir, images, label_ref)

def label_generate(args):

    (xml_dir, label_dir, labels, assign_palette, mask, 
     image_path, check_dir, extract_dir, images, label_ref) = init_generate(args)
   
    bar_worker = au.process_bar(num_items= len(labels))
    
    if image_path == None:
        for f in labels:
            xml_file_name = op.join(xml_dir, f)
            
            object_dict, width, height = xr.xml_decode_polygon(xml_file_name, args, label_ref)
            label_perfix = op.splitext(f)[0] 
            bar_worker.update()
            if object_dict:
                dm.create_label(label_perfix, label_dir, object_dict, 
                         width, height, assign_palette,  args, mask_pts = mask)
    else: 
        num_image = len(images)
        if num_image:
            images_perfix_list = [op.splitext(x)[0] for x in images]
            image_extension = op.splitext(images[0])[1]
                
        for f in labels:
            xml_file_name = op.join(xml_dir, f)    
            object_dict, width, height = xr.xml_decode_polygon(xml_file_name, args, label_ref)
            label_perfix = op.splitext(f)[0] 
            bar_worker.update()
            if object_dict:
                label = dm.create_label(label_perfix, label_dir, object_dict, 
                             width, height, assign_palette, args, mask_pts = mask)                          
                
                if num_image and (label_perfix in images_perfix_list):
                    dm.draw_on_image(label_perfix + image_extension, image_path,
                    check_dir, label, object_dict, args, mask)
                    au.copy_image(extract_dir, image_path, label_perfix + image_extension, args.size)    
    print('\n')

def bbox_generate(args):
    (xml_dir, label_dir, labels, assign_palette, mask, 
     image_path, check_dir, extract_dir, images, label_ref) = init_generate(args)
    
    bar_worker = au.process_bar(num_items= len(labels))
    
    #Define a inner function for different data source
    if args.bndbox == 1:
        #From polygon
        def xml_decode(xml_file_name, args):
            object_dict, width, height = xr.xml_decode_polygon(xml_file_name, args.omit)
            bbox_list = xr.extract_bbox(height, width, object_dict)
            return bbox_list, height, width
    elif args.bndbox == 2:
        #From bounding box
        def xml_decode(xml_file_name, args):
            bbox_list, width, height = xr.xml_decode_bbox(xml_file_name, args.palette, args.fov)
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
            bbox_list, width, height = xml_decode(xml_file_name, args)
            lborder, rborder, narrow_width = au.fov_process(args.fov, width)
            bar_worker.update()
            if bbox_list:
                
                label_perfix = op.splitext(f)[0]          
                
                if num_image and (label_perfix in images_perfix_list):                     
                    dm.draw_poly2bbox(label_perfix + image_extension, image_path, check_dir, bbox_list, 
                                      args.palette, narrow_width, lborder)
                    xw.create_bbox(bbox_list, label_dir, height, narrow_width, label_perfix, args.size)
                    au.copy_image(extract_dir, image_path, label_perfix + image_extension, args.size, 
                                  narrow_width, lborder)
    else:
        raise IOError('Orignal image path must be provided!')
    
    print('\n')            
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(                                     
    description= '''Convert xml label to image label for image segmentation
                 ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-d','--dir', type = str, default = None, required = True,
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
    parser.add_argument('-p', '--palette', type = int, default = 0,
                        help = '0 object palette, 1 component palette')
    parser.add_argument('-f', '--fov', type = int, default = 128,
                        help = 'Keep the scope of picture by FOV')

    args = parser.parse_args()
    
    if args.bndbox:
        bbox_generate(args)
    else:
        label_generate(args)
