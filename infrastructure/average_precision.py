import argparse
import numpy as np
from operator import attrgetter
from itertools import groupby, compress, chain
from read_groundtruth import read_groundtruth
from read_detections import read_detections
from data_structures import iou


def compute_precision_recall(dt_bboxes, gt_bboxes, percentage):    
    # sort detections by confidence
    dt_bboxes = sorted(dt_bboxes, key = attrgetter('conf'), reverse = True)
    
    # sort groundtruth and group by frame identifier
    get_attr = attrgetter('fid')
    fid_gt_bboxes = [list(g) for k, g in groupby(sorted(gt_bboxes, 
                     key = get_attr), get_attr)]
    
    # create arrays to check correspondences between groundthuth and detections
    tp = [0 for x in range(len(dt_bboxes))]
    fp = [0 for x in range(len(dt_bboxes))]
    
    # each detection
    for dt_idx in range(0, len(dt_bboxes)):
        dt = dt_bboxes[dt_idx]
        iou_max = 0
        iou_max_idx = -1
        # compare with groudtruth of the same frame identifier
        try:
            fid_gt_len = len(fid_gt_bboxes[dt.fid])
        except:
            fp[dt_idx] = 1
            continue
        for gt_idx in range(0, fid_gt_len):
            iou_value = iou(dt, fid_gt_bboxes[dt.fid][gt_idx])
            if (iou_value >= percentage) and (iou_value > iou_max):
                iou_max = iou_value
                iou_max_idx = gt_idx
        if iou_max_idx >= 0:
            tp[dt_idx] = 1
        else:
            fp[dt_idx] = 1
    
    # compute cumulative sum of true positives and false positives
    tp = np.cumsum(tp)
    fp = np.cumsum(fp)
    recall = tp / len(gt_bboxes)
    precision = tp / (fp + tp) # element-wise division
    
    return [recall, precision]


def compute_average_precision(recall, precision):
    ap = 0.0
    t = 0.0
    step = 0.1
    kpoints = 11
    while t <= 1.0:
        pr = max(chain(compress(precision.tolist(), 
                                (recall >= t).tolist()), [0.0]))
        ap += pr / kpoints
        t += step
    
    return ap


def average_precision_curve(gt, dt, objclass, percentage):
    gt_bboxes = read_groundtruth(gt, objclass)
    dt_bboxes = read_detections(dt, objclass)
    [recall, precision] = compute_precision_recall(dt_bboxes,
        gt_bboxes, percentage)
    ap = compute_average_precision(recall, precision)

    return [ap, recall, precision]


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-gt', '--groundtruth', help = 'groundtruth (file)')
    parser.add_argument('-dt', '--detections', help = 'detections (file)')
    parser.add_argument('-c', '--object_class',
        help = 'object class (by default CAR)', default = 'car', type = str)
    parser.add_argument('-q', '--quiet', help = 'silent mode (print only TPR)',
        action = 'store_true')
    parser.add_argument('-p', '--percentage', help = 'intersection percentage'\
        ' (from 0 to 1, by default 0.5)', type = float, default = 0.5)
    args = parser.parse_args()

    # print command line arguments
    if args.quiet:
        print(average_precision_curve(args.groundtruth, args.detections,
            args.object_class, args.percentage))
    else:
        print('-----------------------------------')
        print('Groundtruth: ' + args.groundtruth)
        print('Detections: ' + args.detections)
        print('Object class: ' + args.object_class)
        print('Intersection percentage: ' + str(args.percentage))
        print('-----------------------------------')
        [ap, recall, precision] = average_precision_curve(
            args.groundtruth, args.detections, args.object_class,
            args.percentage)
        print('Average precision = ' + str(ap))
        print('-----------------------------------')
