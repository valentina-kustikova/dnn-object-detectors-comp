import sys

sys.path.append('../detector')
sys.path.append('../tracker')

from std_output_saver import StdOutputSaver
from file_output_saver import FileOutputSaver
from video_frame_reader import VideoFrameReader
from sequence_frame_reader import SequenceFrameReader
from opencvdnn_object_detector import OpenCVDNNObjectDetector
from opencv_object_tracker import OpenCVObjectTracker


def create_frame_reader(is_frame_sequence, name):
    if is_frame_sequence:
        video = SequenceFrameReader(name)
        if not video.is_opened():
            raise ValueError('Error when loading frame sequence \
                from directory \'{}\''.format(name))
    elif name is not None:
        video = VideoFrameReader(name)
        if not video.is_opened():
            raise ValueError('Video {} is not opened'.format(name))
    else:
        raise ValueError('You try to read video but you have not set \
            corresponding file name')
    return video


def create_output_saver(f, output):
    if f:
        output_saver = StdOutputSaver()
    elif output is not None:
        output_saver = FileOutputSaver(output)
    else:
        raise ValueError('You try to save information about bounding boxes \
            to the file, but you have not set output file name')
    return output_saver


def create_detector(detector_name, labels_file, framework, trained_model,
        model_description, mean, cols, rows, scale_factor, bgr, threshold):
    if detector_name == 'OpenCV':
        means = [ float(m) for m in mean.split() ]
        detector = OpenCVDNNObjectDetector(framework, trained_model,
            model_description, labels_file, cols, rows, means, scale_factor,
            bgr, threshold)
    else:
        raise ValueError('Unsupported detector type')
    return detector


def create_tracker(tracker_name):
    if tracker_name == None:
        return None
    try:
        tracker = OpenCVObjectTracker(tracker_name)
    except ValueError as exception:
        raise exception
    return tracker
