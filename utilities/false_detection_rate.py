import argparse
import sys

sys.path.append('../readers')

from read_groundtruth import read_groundtruth
from read_detections import read_detections
from compute_detection_rates import compute_detection_rates


def false_detection_rate(gt, dt, objclass, percentage):
    gt_bboxes = read_groundtruth(gt, objclass)
    dt_bboxes = read_detections(dt, objclass)
    [fp, fn, tp, n] = compute_detection_rates(gt_bboxes, dt_bboxes, percentage)
    print('FP = ' + str(fp))
    print('FN = ' + str(fn))
    print('TP = ' + str(tp))
    print('N = ' + str(n))
    return float(fp) / float(tp + fp)


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
        print(false_detection_rate(args.groundtruth, args.detections,
            args.object_class, args.percentage))
    else:
        print('-----------------------------------')
        print('Groundtruth: ' + args.groundtruth)
        print('Detections: ' + args.detections)
        print('Object class: ' + args.object_class)
        print('Intersection percentage: ' + str(args.percentage))
        print('-----------------------------------')
        print('FDR = ' + str(false_detection_rate(args.groundtruth,
            args.detections, args.object_class, args.percentage)))
        print('-----------------------------------')
