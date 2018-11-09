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
    
    def __init__(self, tracker_name, frame = None, rois = []):
        self.tracker_name = tracker_name
        self.tracker = self.__create_opencv_tracker(tracker_name)
        self.frame = frame
        self.rois = rois

    def update_track_roi(self, frame, roi):
        self.frame = frame
        self.rois = [ roi ]
        self.tracker.init(frame, roi)
    
    def update_track_rois(self, frame, rois):
        self.frame = frame
        self.rois = rois
    
    def track(self, next_frame):
        xLeftTop = []
        yLeftTop = []
        xRightBottom = []
        yRightBottom = []
        for roi in self.rois:
            self.tracker.init(self.frame, roi)
            status, bbox = self.tracker.update(next_frame)
            if not status:
                xLeftTop.append(-1)
                yLeftTop.append(-1)
                xRightBottom.append(-1)
                yRightBottom.append(-1)
                print('WARNING: Tracking failed')
            xLeftTop.append(int(bbox[0]))
            yLeftTop.append(int(bbox[1]))
            xRightBottom.append(int(bbox[0] + bbox[2]))
            yRightBottom.append(int(bbox[1] + bbox[3]))
        return [xLeftTop, yLeftTop, xRightBottom, yRightBottom] 
