import os
import argparse
import cv2
from read_groundtruth import read_groundtruth
from read_detections import read_detections
from auxiliary_functions import list_images


def get_gt_img_bboxes(gt_bboxes, img_name):
    img_gt_bboxes = [gt_bbox for gt_bbox in gt_bboxes \
        if gt_bbox.fid == img_name]        
    return img_gt_bboxes


def get_dt_img_bboxes(dt_bboxes, img_name):
    img_dt_bboxes = [dt_bbox for dt_bbox in dt_bboxes \
        if dt_bbox.fid == img_name]
    return img_dt_bboxes


def play_bboxes(img_dir, gt, dt, obj_class):
    img_list = list_images(img_dir)
    gt_bboxes = read_groundtruth(gt, obj_class)
    dt_bboxes = read_detections(dt, obj_class)
    for img_full_name in img_list:
        img = cv2.imread(img_full_name)
        img_name = os.path.basename(img_full_name)
        img_name, img_ext = os.path.splitext(img_name)
        fid = int(img_name)
        img_gt_bboxes = get_gt_img_bboxes(gt_bboxes, fid)
        img_dt_bboxes = get_dt_img_bboxes(dt_bboxes, fid)
        for gt_bbox in img_gt_bboxes:
            cv2.rectangle(img, (gt_bbox.bbox.ltp.x, gt_bbox.bbox.ltp.y),
                (gt_bbox.bbox.rbp.x, gt_bbox.bbox.rbp.y), (0, 255, 0), 2)
        for dt_bbox in img_dt_bboxes:
            cv2.rectangle(img, (dt_bbox.bbox.ltp.x, dt_bbox.bbox.ltp.y),
                (dt_bbox.bbox.rbp.x, dt_bbox.bbox.rbp.y), (0, 0, 255), 2)
        cv2.imshow('Image', img)
        key = cv2.waitKey(0)
        if key == 27:
            break
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-gt', '--groundtruth', help = 'groundtruth (file)')
    parser.add_argument('-dt', '--detections', help = 'detections (file)')
    parser.add_argument('-dir', '--image_directory', help = 'image directory')
    parser.add_argument('-c', '--object_class',
        help = 'object class (by default ALL)', default = 'all', type = str)
    args = parser.parse_args()
    
    # play bounding boxes
    play_bboxes(args.image_directory, args.groundtruth, args.detections,
        args.object_class)
