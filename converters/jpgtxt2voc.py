import sys
import os
import shutil
import argparse

sys.path.append('../readers')

from read_groundtruth import read_groundtruth


def create_directories(track_name, output_directory):
    root_dir = os.path.join(output_directory, track_name)
    if not os.path.exists(root_dir):
        print('Removing old directory.')
        shutil.rmtree(root_dir)
    os.makedirs(root_dir)
    
    annotations_directory = os.path.join(root_dir, 'Annotations')
    os.mkdir(annotations_directory)
    
    list_directory = os.path.join(root_dir, 'ImageSets/Main')
    os.makedirs(list_directory)
    
    image_directory = os.path.join(root_dir, 'JPEGImages')
    os.mkdir(image_directory)
    return [annotations_directory, list_directory, image_directory]


def copy_images(src, dst, track_name = ''):
    if not os.path.isdir(src):
        print('Directory \'{}\' does not exists.'.format(src))
        sys.exit()
    image_names = [ f for f in os.listdir(src) \
        if os.path.isfile(os.path.join(src, f)) ]
    for image_name in image_names:
        shutil.copyfile(os.path.join(src, image_name),
            os.path.join(dst, '{0}_{1}'.format(track_name, image_name)))
    return image_names


def convert_txt2xml(groundtruth, image_directory,
        track_name, output_directory):
    gt_bboxes = read_groundtruth(groundtruth)
    
    if not os.path.isdir(image_directory):
        print('Directory \'{}\' does not exists.'.format(image_directory))
        sys.exit()
    image_names = [ f for f in os.listdir(image_directory) \
        if os.path.isfile(os.path.join(image_directory, f)) ]
    for image_name in image_names:
        
    return


def create_image_lists(output_directory, track_name, image_names):
    return


def convert_jpgtxt2voc(track_name, image_directory,
        groundtruth, output_directory):
    [annotations_directory, list_directory, output_image_directory] = \
        create_directories(track_name, output_directory)
    
    [image_names] = copy_images(image_directory, output_image_directory,
        track_name)
    
    convert_txt2xml(groundtruth, image_directory, track_name, output_directory)
    
    create_image_lists(output_directory, track_name, image_names)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--track_name', help = 'track name to add \
        to the image file names')
    parser.add_argument('-i', '--image_directory', help = 'Directory containing \
        a set of images')
    parser.add_argument('-g', '--groundtruth', help = 'Groundtruth file \
        (line is as follows <fid> <class> <ltp.x> <ltp.y> <rbp.x> <rbp.y>)')
    parser.add_argument('-o', '--output_directory', help = 'Output directory \
        to save training data in VOC format')
    args = parser.parse_args()
    if (sys.argv < 5):
        parser.print_help()
        sys.exit()
    
    convert_jpgtxt2voc(args.track_name, args.image_directory,
        args.groundtruth, args.output_directory)
