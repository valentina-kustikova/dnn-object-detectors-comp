import argparse
from read_groundtruth import read_groundtruth
from read_detections import read_detections
from compute_detection_rates import compute_detection_rates


def fppf_rate(gt, dt, objclass, percentage, kimages):
    gt_bboxes = read_groundtruth(gt, objclass)
    dt_bboxes = read_detections(dt, objclass)
    [fp, fn, tp, n] = compute_detection_rates(gt_bboxes, dt_bboxes, percentage)
    print('FP = ' + str(fp))
    print('FN = ' + str(fn))
    print('TP = ' + str(tp))
    print('N = ' + str(n))
    return float(fp) / float(kimages)


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-gt', '--groundtruth', help = 'groundtruth (file)')
    parser.add_argument('-dt', '--detections', help = 'detections (file)')
    parser.add_argument('-c', '--object_class',
        help = 'object class (by default CAR)', default = 'car', type = str)
    parser.add_argument('-s', '--silent', help = 'silent mode (print only TPR)',
        action = 'store_true')
    parser.add_argument('-p', '--percentage', help = 'intersection percentage'\
        ' (from 0 to 1, by default 0.5)', type = float, default = 0.5)
    parser.add_argument('-k', '--kimages', help = 'number of images',
        type = int)
    args = parser.parse_args()

    # print command line arguments
    if args.silent:
        print(fppf_rate(args.groundtruth, args.detections,
            args.object_class, args.percentage))
    else:
        print('-----------------------------------')
        print('Groundtruth: ' + args.groundtruth)
        print('Detections: ' + args.detections)
        print('Object class: ' + args.object_class)
        print('Intersection percentage: ' + str(args.percentage))
        print('Number of images: ' + str(args.kimages))
        print('-----------------------------------')
        print('FPperFrame = ' + str(fppf_rate(args.groundtruth,
            args.detections, args.object_class, args.percentage,
            args.kimages)))
        print('-----------------------------------')
