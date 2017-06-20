"""
Created on Sun Apr 23 14:17:34 2017

@author: andrew

Use the result of xml2label.py to create dataset just like VOC style
"""

import os
import os.path as op
import shutil
import argparse
import numpy as np
import assist_util as au

def initialization(args):
    #Create directory that we will use in the future    
    labels_root =  args.nlabel
    images_root = args.nimage
    list_root = args.nlist
    set_name = args.name
    if op.exists(set_name):
        shutil.rmtree(set_name)
        os.makedirs(set_name)
    else:
        os.makedirs(set_name)
        
    if op.exists(labels_root):
        shutil.rmtree(labels_root)
        os.makedirs(labels_root)
    else:
        os.makedirs(labels_root)
        
    if op.exists(images_root):
        shutil.rmtree(images_root)
        os.makedirs(images_root)
    else:
        os.makedirs(images_root)
    
    if op.exists(list_root):
        shutil.rmtree(list_root)
        os.makedirs(list_root)
    else:
        os.makedirs(list_root)
    
def dataset_creation(args):
    '''
    Create data set from result of xml2label
    '''
    src_root = args.dir
    labels_root =  args.nlabel
    images_root = args.nimage
    list_root = args.nlist
    set_name = args.name
    
    list_src_root = os.listdir(src_root)    
    list_src_root = [x for x in list_src_root if op.isdir(op.join(src_root,x))]
    #Copy file from the result of xml2label
    for d in list_src_root:
        end_tag = d.split('_')[-1]
        if end_tag == 'label':
            list_label = os.listdir(op.join(src_root,d))
            list_label = [x for x in list_label if op.isfile(op.join(src_root,d,x))]
            for f in list_label:
                '''This method will move the source file to destination with another name'''
                os.rename(op.join(src_root,d,f), op.join(labels_root, d[0:-len(end_tag)] + f))
        if end_tag == 'extract':
            list_image = os.listdir(op.join(src_root,d))
            list_image = [x for x in list_image if op.isfile(op.join(src_root,d,x))]
            for f in list_image:
                os.rename(op.join(src_root,d,f), op.join(images_root, d[0:-len(end_tag)] + f))             
    print('File copy completed')
    #Data augmentation
    if args.mirror:
        au.mirror_augmentation(images_root, labels_root)
        print('Mirror augmentation completed')
    if args.auto:
        au.autoconstrast_augmentation(images_root, labels_root)
        print('Auto constrast augmentation completed')
    #Achive the file name from label or image set
    list_data_set = os.listdir(labels_root)
    list_data_set = [x for x in list_data_set if op.isfile(op.join(labels_root, x))]    
    base_name_list = [x.split('.')[0] for x in list_data_set]    
    capacity_set = len(base_name_list)    
    num_train = int(capacity_set * args.ratio)
    if args.shuffle:
        np.random.shuffle(base_name_list)
    #Seperate train and val list
    train_list = base_name_list[0: num_train]
    val_list = base_name_list[num_train : -1]  
    #np.random.shuffle(train_list)
    for i in range(len(train_list) - 1):
        train_list[i] += '\n'
    for i in range(len(val_list) - 1):
        val_list[i] += '\n'
    #Write list to file
    train_list_loc = op.join(list_root, 'train.txt')
    val_list_loc = op.join(list_root, 'val.txt')
    
    with open(train_list_loc,'w') as ft:
        ft.writelines(train_list)
        
    with open(val_list_loc,'w') as fv:
        fv.writelines(val_list)
    print('List file has cteated')
    #Move image and label dataset to directory that you named
    os.rename(images_root, op.join(set_name, images_root))
    os.rename(labels_root, op.join(set_name, labels_root))
    os.makedirs(op.join(set_name, list_root))
    os.rename(train_list_loc, op.join(set_name, train_list_loc))
    os.rename(val_list_loc, op.join(set_name, val_list_loc))
    shutil.rmtree(list_root.split('/')[0])
    print('DataSet creation process done')
    
def create_dataset(args):
    initialization(args)
    dataset_creation(args)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(                                     
    description= '''Create a dataset with VOC style
                 ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-d','--dir', type = str, default = './result',
                        help = 'The directory that contain xml label files')
    parser.add_argument('-n','--name', type = str, default = 'underground_parkinglots',
                        help = 'Dataset name')
    parser.add_argument('-r','--ratio', type = float, default = 0.85,
                        help = 'Sepreate ratio of train and validation dataset')
    parser.add_argument('-m','--mirror', type = int, default = 1,
                        help = 'Use image mirror to augment dataset')
    parser.add_argument('-a','--auto', type = int, default = 1,
                        help = 'Use image auto constrast to augment dataset')
    parser.add_argument('--nlabel', type = str, default = 'SegmentationClass',
                        help = 'Label set name')
    parser.add_argument('--nimage', type = str, default = 'JPEGImages',
                        help = 'Image set name')
    parser.add_argument('--nlist', type = str, default = 'ImageSets/Segmentation',
                        help = 'Path for training and validation list')
    parser.add_argument('-s', '--shuffle', type = int, default = 0,
                        help = 'Whether to shuffle the data list')
    
    args = parser.parse_args()
    
    create_dataset(args)
