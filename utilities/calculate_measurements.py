import argparse
import sys
import os
import re

sys.path.append('../readers')

from read_groundtruth import read_groundtruth
from read_detections import read_detections
from average_precision import average_precision_curve
from compute_detection_rates import compute_detection_rates


def compute_all_detection_rates(gt_bboxes, dt_bboxes, object_class,
        percentage, kimages):
    [fp, fn, tp, n] = compute_detection_rates(gt_bboxes, dt_bboxes, percentage)
    tpr = float(tp) / float(n)
    fdr = float(fp) / float(tp + fp)
    fppf = float(fp) / float(kimages)
    [ap, recall, precision] = average_precision_curve(gt_bboxes, dt_bboxes,
        object_class, percentage)
    return [ap, tpr, fdr, fppf]


def read_track_frames(file_name):
    track_frames = {}
    file = open(file_name, 'r')
    for line in file:
        matcher = re.match(r'([\w\-]+)[ ]+([\d]+)', line)
        if matcher:
            track_name = matcher.group(1).lower()
            kimages = int(matcher.group(2))
            track_frames[track_name] = kimages
        else:
            print('Line \'{}\' does not match a template.'.format(line))
    file.close()
    return track_frames


def calculate_measurements(groundtruth_directory, detections_directory,
        object_class, percentage, track_kimages_file, output_file):
    if not os.path.isdir(groundtruth_directory):
        print('Parameter \'{}\' is not a directory.'.
            format(groundtruth_directory))
        return
    if not os.path.isdir(detections_directory):
        print('Parameter \'{}\' is not a directory.'.
            format(detections_directory))
        return
    if not os.path.isfile(track_kimages_file):
        print('Parameter \'{}\' is not a file.'.
            format(track_kimages_file))
        return
    
    detection_files = [ f for f in os.listdir(detections_directory) \
        if os.path.isfile(os.path.join(detections_directory, f)) ]
    track_kimages_dict = read_track_frames(track_kimages_file)
    
    ofile = open(output_file, 'w')
    ofile.write('Track identifier;Model identifier;AP;TPR;FDR;FPperFrame\n')
    for detections_file_name in detection_files:
        matcher = re.match(r'([\w\-]+)_imgs_([\w\-]+)\.txt', detections_file_name)
        if matcher:
            model_name = matcher.group(1)
            track_name = matcher.group(2)
            groundtruth_file_name = os.path.join(groundtruth_directory,
                '{}.txt'.format(track_name))
            if not os.path.isfile(groundtruth_file_name):
                print('There is no groundtruth file \'{0}\' corresponding \
                    to the detection file \'{1}\' in the directory.'.format(
                        groundtruth_file_name, detections_file_name))
                continue
            detections_file_name = os.path.join(detections_directory,
                detections_file_name)
            print(groundtruth_file_name)
            gt_bboxes = read_groundtruth(groundtruth_file_name, object_class)
            dt_bboxes = read_detections(detections_file_name)
            kimages = track_kimages_dict[track_name.lower()]
            if kimages == None:
                print('There is no line corresponding to the track {}'.format(
                    track_name))
                continue
            [ap, tpr, fdr, fppf] = compute_all_detection_rates(gt_bboxes,
                dt_bboxes, object_class, percentage, kimages)
            ofile.write('{0};{1};{2};{3};{4};{5}\n'.format(track_name,
                model_name, ap, tpr, fdr, fppf))
        else:
            print('File \'{}\' does not match a template.'.
                format(detections_file_name))
    ofile.close()        
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--groundtruth_directory',
        help = 'directory that contains groundtruth files \
        (file name is as follows <track_name>.txt)')
    parser.add_argument('-d', '--detections_directory',
        help = 'directory that contains files with detections \
        (file name is as follows <model_name>_imgs_<track_name>.txt)')
    parser.add_argument('-f', '--track_frames', help = 'file that contains \
        number of track frames (each line is as follows \
        \'<track_name> <kimages>\')')
    parser.add_argument('-c', '--object_class',
        help = 'object class (by default CAR)', default = 'car', type = str)
    parser.add_argument('-p', '--percentage', help = 'intersection percentage'\
        ' (from 0 to 1, by default 0.5)', type = float, default = 0.5)
    parser.add_argument('-o', '--output_file', help = 'output file name \
        (file contains a table with AP, TPR, FDR, FPperFrame for \
        the existing detections)')    
    args = parser.parse_args()
    if (len(sys.argv) < 5):
        parser.print_help()
        sys.exit()

    calculate_measurements(args.groundtruth_directory,
        args.detections_directory, args.object_class, args.percentage,
        args.track_frames, args.output_file)
