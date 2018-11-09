from abc import ABC, abstractmethod


class FrameReader(ABC):
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def is_opened(self):
        """Method verifies that frame sequence is opened"""
        pass
    
    @abstractmethod
    def read():
        """Method reads next frame"""
        pass