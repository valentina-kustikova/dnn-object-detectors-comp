import cv2
from frame_reader import FrameReader


class VideoFrameReader(FrameReader):
    
    def __init__(self, file_name):
        FrameReader.__init__(self, file_name)
        self.video = cv2.VideoCapture(file_name)
    
    def is_opened(self):
        return self.video.isOpened()
    
    def read(self):
        return self.video.read()
