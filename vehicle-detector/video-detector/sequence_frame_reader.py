import os
import cv2
from frame_reader import FrameReader


class SequenceFrameReader(FrameReader):
    
    def __init__(self, dir_name):
        FrameReader.__init__(self, dir_name)
        self.dir_name = dir_name
        if not os.path.isdir(dir_name):
            self.opened = False
        else:
            self.opened = True
            self.frame_idx = 0
            self.images = [os.path.join(dir_name, img) \
                for img in os.listdir(dir_name) \
                    if os.path.isfile(os.path.join(dir_name, img))]            
    
    def is_opened(self):
        return self.opened
    
    def read(self):
        if self.frame_idx >= len(self.images):
            return False, None
        frame = cv2.imread(self.images[self.frame_idx])
        if frame is None:
            raise ValueError('Error when reading the next image \'{}\''.
                format(self.images[self.frame_idx]))
        self.frame_idx += 1
        return True, frame
