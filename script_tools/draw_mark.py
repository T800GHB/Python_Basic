# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:21:23 2017

@author: andrew
"""

import PIL.Image as pi
import PIL.ImageDraw as pd
import os.path as op
import assist_util as au

def draw_poly2bbox(filename, image_dir, dst_dir, bbox_list, palette_flag, narrow_width, lborder):
    
    img = pi.open(op.join(image_dir, filename)).convert('RGB')
    if lborder:
        img = img.crop((lborder, 0, lborder + narrow_width, img.height))
    draw_object = pd.Draw(img)
    
    if palette_flag:
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
        final_label = label.resize((re_width, re_height), pi.NEAREST)
    else:
        final_label = label
    final_label.save(op.join(folder, label_name))
    
    return label