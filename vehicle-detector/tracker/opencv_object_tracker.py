import cv2
from object_tracker import ObjectTracker


class OpenCVObjectTracker(ObjectTracker):

    def __create_opencv_tracker(self, tracker_name):        
        if tracker_name == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_name == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_name == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_name == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_name == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_name == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        elif tracker_name == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        elif tracker_name == "CSRT":
            tracker = cv2.TrackerCSRT_create()
        else:
            raise ValueError('Unsupported tracker')
        return tracker
    
    def __init__(self, tracker_name):
        self.tracker_name = tracker_name
        self.tracker = self.__create_opencv_tracker(tracker_name)
    
    def __init__(self, frame, roi, tracker_name):
        ObjectTracker.__init__(self, frame, roi)
        self.tracker_name = tracker_name
        self.tracker = self.__create_opencv_tracker(tracker_name)
        self.tracker.init(frame, roi)        

    def update(self, frame, roi):
        self.frame = frame
        self.roi = roi
        self.tracker.init(frame, roi)
    
    def track(self, next_frame):
        status, bbox = self.tracker.update(next_frame)
        if not status:
            raise Exception('ERROR: Tracking failed')
        return (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
