import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from operator import attrgetter
from itertools import groupby, chain, compress
from read_groundtruth import read_groundtruth
from read_detections import read_detections
from data_structures import iou


def compute_precision_recall(dt_bboxes, gt_bboxes, percentage):    
    # sort detections by confidence
    dt_bboxes = sorted(dt_bboxes, key = attrgetter('conf'), reverse = True)
    
    # sort groundtruth and group by frame identifier
    get_attr = attrgetter('fid')
    fid_gt_bboxes = {k: list(g) for k, g in groupby(sorted(gt_bboxes, 
                     key = get_attr), get_attr)}
    
    # create arrays to check correspondences between groundthuth and detections
    tp = [0 for x in range(len(dt_bboxes))]
    fp = [0 for x in range(len(dt_bboxes))]
    
    # each detection
    for dt_idx in range(len(dt_bboxes)):
        dt = dt_bboxes[dt_idx]
        iou_max = percentage
        iou_max_idx = -1
        # compare with groudtruth of the same frame identifier
        try:
            fid_gt_len = len(fid_gt_bboxes[dt.fid])
        except:
            fp[dt_idx] = 1
            continue
        for gt_idx in range(fid_gt_len):
            gt = fid_gt_bboxes[dt.fid][gt_idx]
            iou_value = iou(dt, gt)
            if (iou_value >= iou_max):
                iou_max = iou_value
                iou_max_idx = gt_idx
        if (iou_max_idx >= 0) and (not fid_gt_bboxes[dt.fid][iou_max_idx].checked):
            tp[dt_idx] = 1
            fid_gt_bboxes[dt.fid][iou_max_idx].checked = True
        else:
            fp[dt_idx] = 1
    
    # compute cumulative sum of true positives and false positives
    tp = list(np.cumsum(tp))
    fp = list(np.cumsum(fp))
    recall = [x / len(gt_bboxes) for x in tp]
    precision = [tp[i] / (fp[i] + tp[i]) for i in range(len(tp))]
    
    return [recall, precision]


def compute_average_precision(recall, precision):
    ap = 0.0
    t = 0.0
    step = 0.1
    kpoints = 11
    while t <= 1.0:
        pr = max(chain(compress(precision,
            [recall[i] >= t for i in range(len(recall))]), [0.0]))
        ap += pr / kpoints
        t += step
    
    return ap


def average_precision_curve(gt_bboxes, dt_bboxes, objclass, percentage):    
    [recall, precision] = compute_precision_recall(dt_bboxes,
        gt_bboxes, percentage)
    ap = compute_average_precision(recall, precision)

    return [ap, recall, precision]


def show_precision_recall_curve(ap, recall, precision):
    plt.plot(recall, precision)
    plt.title('AP = {0:.3f}'.format(ap))
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.show()


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--groundtruth', help = 'groundtruth (file)')
    parser.add_argument('-d', '--detections', help = 'detections (file)')
    parser.add_argument('-c', '--object_class',
        help = 'object class (by default CAR)', default = 'car', type = str)
    parser.add_argument('-q', '--quiet', help = 'silent mode (print only TPR)',
        action = 'store_true')
    parser.add_argument('-p', '--percentage', help = 'intersection percentage'\
        ' (from 0 to 1, by default 0.5)', type = float, default = 0.5)
    args = parser.parse_args()
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit()

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
        gt_bboxes = read_groundtruth(args.groundtruth, args.object_class)
        dt_bboxes = read_detections(args.detections, args.object_class)
        [ap, recall, precision] = average_precision_curve(
            args.groundtruth, args.detections, args.object_class,
            args.percentage)
        print('Average precision = ' + str(ap))
        show_precision_recall_curve(ap, recall, precision)
        print('-----------------------------------')
