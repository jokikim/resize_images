#!/usr/bin/env python
# coding: utf-8

# # Resize Images

import os
import sys
import time
from tqdm import tqdm
from PIL import Image


# ## Set variables

def set_variables():
    # Set KB file size threshold.
    kb_threshold = 500

    # Resize dimensions.
    resize_dims = (1020,1360)

    # Set input and output folders.
    input_folder = os.path.join(os.getcwd(),'images','input')
    output_folder = os.path.join(os.getcwd(),'images','output')

    # List of all image directories.
    img_folders = [x[0] for x in os.walk(input_folder)][1:]
    
    # Print.
    print(f'   kb_threshold: {kb_threshold}')
    print(f'   resize_dims: {resize_dims}')
    print(f'   Current Directory: {os.getcwd()}')
    print(f'   Input Folder: {input_folder}')
    print(f'   Output Folder: {output_folder}')
    
    return kb_threshold,resize_dims,input_folder,output_folder,img_folders


# ## Resize Images

# In[3]:


def resize_all_images(img_folders, resize_dims):
    '''
    Given the list of image folders (img_folders), loop over each folder and call the
    resize_images to resize each image file within the folder.
    
    Params:
    =======
    img_folders : list
        List of all full path of image folders.
    '''
    
    def resize_images(dir_path, resize_dims):
        '''
        Loop over a single image folder and resize all image files within the folder.
        
        Params:
        =======
        dir_path : string
            Full Path (string) to the image directory. All files within this directory must contain the images.

        '''
        from PIL import Image

        # Gather all image files in the dir_path.
        imgs_list = [x[2] for x in os.walk(dir_path)][0]

        # Create full paths to the image files.
        imgs_path = [os.path.join(dir_path,x) for x in imgs_list]

        # Loop over each image file, and resize.
        new_imgs_list = []
        failed_imgs_list = []
        for img in imgs_path:

            # Open image.
            image = Image.open(img)

            # Extract dimensions.
            width, height = image.size

            # Check dimension ratio.
            check_ratio = round(width/height,2)

            # Resize, if ratio is correct.
            if 0.66 <= check_ratio <= 0.76:
                # Resize image.
                # print(f'Resizing: {img}')
                image = image.resize(resize_dims)
                new_imgs_list.append([img,image]) # Append image path and actual image.
            else:
                print('   Original Image much beyond the 3:4 ratio:')
                print(f'     Ratio: {check_ratio}')
                print(f'     Path: {img_path}')
                failed_imgs_list.append([img,image])  # Append image path and actual image.

        return ((new_imgs_list,failed_imgs_list))
    
    # Loop over all image folders and run the function.
    start_time = time.time()
    all_new_imgs = []
    all_failed_imgs = []
    tqdm_tim_folders = tqdm(img_folders)
    for img_dir in tqdm_tim_folders:
        tqdm_tim_folders.set_description(f"Processing Image Folder")
        new_images_list,failed_imgs_list = resize_images(img_dir,resize_dims)
        all_new_imgs.extend(new_images_list)
        all_failed_imgs.extend(failed_imgs_list)
    end_time = time.time()
    
    # Print.
    print(f'   Total Run Time: {round((end_time-start_time)/60,2)} mins')
    print(f'   Successful Image Resizes: {len(all_new_imgs)}')
    print(f'   Failed Image Resizes: {len(all_failed_imgs)}')
    
    return ((all_new_imgs,all_failed_imgs))


# ## Export

def save_all_images(all_new_imgs):
    '''
    Params:
    ======
    all_new_imgs : List
        List of list with first element as the full image file path, and the second element
        with the Image object.
    '''
    for img_path,img_image in all_new_imgs:

        # Get the subdirectories names after the input_folder path.
        subdir_names = img_path.replace(input_folder,'').split('/')
        subdir_names = [x for x in subdir_names if x != '']

        # Get the image folder path that holds the actual image files.
        # Create this folder if not exists.
        subdir_names_parent = os.path.join(output_folder,*subdir_names[:-1])
        if not os.path.exists(subdir_names_parent):
            os.makedirs(subdir_names_parent)

        # Create the full output path.
        img_output_path = os.path.join(output_folder,*subdir_names)

        # Export the image.
        img_image.save(img_output_path)

        # Check the file size.
        img_file_size = round(os.path.getsize(img_output_path)/1000,2)
        if img_file_size > kb_threshold:
            print(f'   File size Over {kb_threshold} KB threshold: {img_file_size} KB')
    
    return print('   Images successfully saved.')


# ## Execute main file

if __name__ == "__main__":
    
    print('Retrieving Variables....')
    # Return Variables
    kb_threshold,resize_dims,input_folder,output_folder,img_folders = set_variables()

    # Resize images.
    print('\nResizing Images....')
    all_new_imgs,all_failed_imgs = resize_all_images(img_folders=img_folders,
                                                     resize_dims=resize_dims)
    
    # Export images.
    print('\nExporting Images....')
    save_all_images(all_new_imgs=all_new_imgs)
