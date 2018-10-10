from abc import ABC, abstractmethod

class ObjectTracker(ABC):
    
    def __init__(self, frame, roi):        
        self.frame = frame
        self.roi = roi
    
    @abstractmethod
    def track(self, next_frame):
        """Method tracks object on the given image"""
        pass
