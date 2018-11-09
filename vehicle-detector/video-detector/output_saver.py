from abc import ABC, abstractmethod


class OutputSaver(ABC):
    
    def __init__(self, output = None):
        self.output = output

    @abstractmethod
    def save(self, frame_idx, class_ids, xLeftTop, yLeftTop,
             xRightBottom, yRightBottom, confidences):
        """Method saves detected objects"""
        pass