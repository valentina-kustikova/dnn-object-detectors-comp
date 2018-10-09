from abc import ABC, abstractmethod


class ObjectDetector(ABC):
    
    def __init__(self, weights_file_name):
        # Binary model file
        self.weights_file_name = weights_file_name
    
    @abstractmethod
    def detect(self, img):
        """Method detects objects on the given image"""
        pass
