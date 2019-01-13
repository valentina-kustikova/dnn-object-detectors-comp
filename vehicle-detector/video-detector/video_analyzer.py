import argparse
from fabrics import create_frame_reader, create_output_saver, \
    create_detector, create_tracker
from full_video_detector import FullVideoDetector
from stepwise_video_detector import StepwiseVideoDetector


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Video to detect and track vehicles
    parser.add_argument('-q', '--frame_sequence', action = 'store_true',
        help = 'flag that allows to process image sequence')
    parser.add_argument('-v', '--video', help = 'video to detect vehicles or \
        directory name containing image sequence')
    
    # Video-based detection algorithm
    parser.add_argument('-a', '--algorithm', default = 'FD', help = 'type \
        of video-based detection algorithm (\'FD\' - full detection \
        frame-by-frame, FDT - full detection + creating tracks)')
    
    # Detector parameters
    parser.add_argument('-d', '--detector', default = 'OpenCV',
        help = 'detector name (\'OpenCV\' mode supports DNN-based detectors)')
    #default = 'caffe'
    parser.add_argument('-f', '--framework', default = 'darknet',
        help = 'deep learning framework (\'caffe\', \'darknet\') \
        are supported')
    parser.add_argument('-l', '--labels', default = '../tests/voc_classes.txt',
        help = 'file containing object classes for object detection \
        in format \'<id> <class_name>\'')
    #default = '../tests/resnet50_rfcn_final.caffemodel',
    parser.add_argument('-w', '--weights',
        default = '../tests/yolo-voc.weights',
        help = 'model trained to detect objects')
    #default = '../tests/rfcn_pascal_voc_resnet50.prototxt',
    parser.add_argument('-p', '--representation',
        default = '../tests/yolo-voc.cfg',
        help = 'model description')
    #default = '102.9801 115.9465 122.7717',
    parser.add_argument('-m', '--mean', default = '0 0 0',
        help = 'mean intensity value')
    #default = 800,
    parser.add_argument('-c', '--cols', default = 416,
        help = 'input width (cols)')
    #default = 600,
    parser.add_argument('-r', '--rows', default = 416,
        help = 'input height (rows)')
    #default = 1.0,
    parser.add_argument('-s', '--scale_factor',  default = 0.00392,
        help = 'scale factor for the input blob')
    #default = 'bgr',
    parser.add_argument('-bgr', default = 'rgb',
        help = 'flag to set the sequence of channels (\'bgr\' or \'rgb\')')
    parser.add_argument('-e', '--confidence_threshold', default = 0.5,
        help = 'confidence threshold')
    
    # Tracker parameters
    parser.add_argument('-t', '--tracker', default = None, help = 'tracker \
        name supported by OpenCV (\'BOOSTING\', \'MIL\', \'KCF\', \'TLD\', \
        \'MEDIANFLOW\', \'GOTURN\', \'MOSSE\', \'CSRT\')')

    # Options
    parser.add_argument('-so', '--std_output', action = 'store_true',
        help = 'redirect output information about detected objects \
        to the standard output')
    parser.add_argument('-o', '--output', default = 'output.txt',
        help = 'output file containing list of detected vehicles')

    args = parser.parse_args()

    try:
        # Prepare video, detector and tracker
        video = create_frame_reader(args.frame_sequence, args.video)
        output_saver = create_output_saver(args.std_output, args.output)
        detector = create_detector(args.detector, args.labels, args.framework,
            args.weights, args.representation, args.mean, args.cols,
            args.rows, args.scale_factor, args.bgr, args.confidence_threshold)
        tracker = create_tracker(args.tracker)
        # Detect and track vehicles
        if (args.algorithm == 'FD'):
            video_detector = FullVideoDetector(video, detector,
                output_saver)
        elif (args.algorithm == 'FDT'):
            video_detector = StepwiseVideoDetector(video, detector, tracker,
                output_saver)
        else:
            raise ValueError('Video-based detection method {} \
                is not supported'.format(args.algorithm))
        video_detector.process()
    except Exception as ex:
        print('ERROR: {}'.format(str(ex)))
