import argparse
import sys
from fabrics import open_video, create_detector, create_tracker


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Video to detect and track vehicles
    parser.add_argument('-v', '--video', help = 'video to detect vehicles')
    
    # Detector parameters
    parser.add_argument('-d', '--detector', help = 'detector name \
        (\'CaffeDNN\' is supported)')
    parser.add_argument('-l', '--labels', help = 'file containing object \
        classes for object detection in format \'<id> <class_name>\'')
    parser.add_argument('-w', '--weights', help = 'model trained to detect \
        objects')
    parser.add_argument('-r', '--representation', help = 'model description')
    parser.add_argument('-m', '--means', help = 'mean intensity value')
    parser.add_argument('-c', '--cols', help = 'input width (cols)')
    parser.add_argument('-r', '--rows', help = 'input height (rows)')
    parser.add_argument('-s', '--scale_factor',  help = 'scale factor \
        for the input blob')
    parser.add_argument('-f', '--confidence_threshold', default = 0.5,
        help = 'confidence threshold')
    
    # Tracker parameters
    parser.add_argument('-t', '--tracker', help = 'tracker name supported \
        by OpenCV (\'BOOSTING\', \'MIL\', \'KCF\', \'TLD\', \'MEDIANFLOW\', \
        \'GOTURN\', \'MOSSE\', \'CSRT\')')

    # Options
    parser.add_argument('-q', '--quiet', action = 'store_true',
        help = 'silent mode (detect and track objects, and write bounding \
        boxes to the output file)')
    parser.add_argument('-o', '--output', default = 'output.txt',
        help = 'output file containing list of detected vehicles')

    args = parser.parse_args()

    try:
        # Prepare video, detector and tracker
        video = open_video(args.video)
        detector = create_detector(args.detector, args.labels, args.weights,
            args.representation, args.means, args.cols, args.rows,
            args.scale_factor, args.threshold)
        tracker = create_tracker(args.tracker)
        # Detect and track vehicles
        if args.quiet:
            video_detector = OfflineVideoDetector(detector,
                tracker, args.output)
        else:
            video_detector = OnlineVideoDetector(detector, tracker)
    except:
        print('ERROR: {}'.format(sys.exc_info()[0]))
