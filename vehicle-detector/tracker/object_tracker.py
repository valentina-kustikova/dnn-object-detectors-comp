from abc import ABC, abstractmethod

class ObjectTracker(ABC):
    
    def __init__(self, frame, rois):
        self.frame = frame
        self.rois = rois
    
    @abstractmethod
    def update_track_roi(self, frame, roi):
        """Method updates frame and ROI"""
        pass

    @abstractmethod
    def update_track_rois(self, frame, rois):
        """Method updates frame and ROIs"""
        pass
    
    @abstractmethod
    def track(self, next_frame):
        """Method tracks object on the given image"""
        pass
