from abc import ABC, abstractmethod


class VideoDetector(ABC):
    
    def __init__(self, video, detector, tracker = None, output_saver = None):
        self.video = video
        self.detector = detector
        self.tracker = tracker
        self.output_saver = output_saver        
        self.obj_class_ids = []
        self.obj_confidencies = []
        self.obj_xLeftTop = []
        self.obj_yLeftTop = []
        self.obj_xRightBottom = []
        self.obj_yRightBottom = []        
        self.obj_tracks = []

    @abstractmethod
    def process():
        """Method that implements video-based detection"""
        pass
        