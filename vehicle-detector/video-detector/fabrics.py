import sys
import cv2

sys.path.append('../detector')
sys.path.append('../tracker')

from dnn_object_detector import CaffeDNNObjectDetector
from opencv_object_tracker import OpenCVObjectTracker


def open_video(file_name):
    video = cv2.VideoCapture(file_name)
    if not video.isOpened():
        raise ValueError('Video {} is not opened'.format(file_name))
    return video


def create_detector(detector_name, labels_file, trained_model,
        model_description, means, cols, rows, scale_factor, threshold):
    if detector_name == 'CaffeDNN':
        detector = CaffeDNNObjectDetector(trained_model, model_description,
            labels_file, cols, rows, means, scale_factor, threshold)
    else:
        raise ValueError('Unsupported detector type')
    return detector


def create_tracker(tracker_name):
    try:
        tracker = OpenCVObjectTracker(tracker_name)
    except ValueError as exception:
        raise exception
    return tracker