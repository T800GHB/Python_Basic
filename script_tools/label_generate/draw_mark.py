# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:21:23 2017

@author: andrew
"""

import PIL.Image as pi
import PIL.ImageDraw as pd
import os.path as op
import assist_util as au

def draw_poly2bbox(filename, image_dir, dst_dir, bbox_list, args, narrow_width, lborder):
    
    img = pi.open(op.join(image_dir, filename)).convert('RGB')
    if lborder:
        img = img.crop((lborder, args.crop, lborder + narrow_width, img.height))
    elif args.crop:
        img = img.crop((0, args.crop, img.width, img.height))
    draw_object = pd.Draw(img)
    
    if args.palette:
        palette = au.component_palette
    else:
        palette = au.rgb_palette

    for bbox in bbox_list:        
        draw_object.rectangle((bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax), outline = palette[bbox.name])
        draw_object.text((bbox.xmin, bbox.ymin), str(bbox.difficult), palette[bbox.name])    
            
    img.save(op.join(dst_dir, filename))


def draw_on_image(filename, image_dir, dst_dir, label_image, item_dict, args, mask_pts = None):   
    img = pi.open(op.join(image_dir, filename)).convert('RGB')
    if args.transparent:
        attach_image = label_image.convert('RGB')
        blend_image = pi.blend(img, attach_image, args.alpha)
        if args.crop:
            top = int(float(args.crop) / args.size)
            blend_image = blend_image.crop((0, top, blend_image.width, blend_image.height))
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
        if mask_pts:
            draw_img.polygon(mask_pts, fill = au.rgb_palette['ignore'])

        if args.crop:
            top = int(float(args.crop) / args.size)
            img = img.crop((0, top, img.width, img.height))

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
        
    if mask_pts:
        draw_label.polygon(mask_pts, fill = au.gray_palette['ignore'])
        
    label.mode = 'P'
    label.putpalette(assign_palette)
    extension = '.png'
    label_name = image_name + extension
    if args.size != 1.0:
        re_height = int(args.size * float(height))
        re_width = int(args.size * float(width))
        resize_label = label.resize((re_width, re_height), pi.NEAREST)
    else:
        resize_label = label
    if args.crop:
        crop_label = resize_label.crop((0, args.crop, resize_label.width, resize_label.height))
    else:
        crop_label = resize_label

    crop_label.save(op.join(folder, label_name))
    
    return label