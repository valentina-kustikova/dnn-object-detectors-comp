import cv2
import re
from object_detector import ObjectDetector


class CaffeDNNObjectDetector(ObjectDetector):
    
    def __init__(self, weights_file_name, model_file_name, classes_file_name,
            input_width, input_height, mean_value, scale_factor):
        ObjectDetector.__init__(self, weights_file_name)
        self.model_file_name = model_file_name
        self.classes_file_name = classes_file_name
        self.net = cv2.dnn.readNetFromCaffe(model_file_name,
            weights_file_name)
        self.input_size = (input_width, input_height)
        self.mean_value = mean_value
        self.scale_factor = scale_factor
    
    def __read_classes(self):
        classes = {}
        file = open(self.classes_file_name, 'r')
        for line in file:
            matcher = re.match(r'([\d]+)[ ]+([\w]+)', line)
            if matcher:
                class_id = int(matcher.group(1))
                class_name = matcher.group(2)
                classes[class_id] = class_name.lower()
        file.close()
        return classes
    
    def __postprocess_detections(self, image, resized_image, detections):
        class_ids = []
        xLeftTop = []
        yLeftTop = []
        xRightBottom = []
        yRightBottom = []
        confidences = []
        
        height = image.shape[0]
        width = image.shape[1]
        resized_height = resized_image.shape[0]
        resized_width = resized_image.shape[1]
        yscale_factor = image.shape[0] / resized_height
        xscale_factor = image.shape[1] / resized_width
        classes = self.__read_classes()
        
        for i in range(detections.shape[2]):
            class_id = int(detections[0, 0, i, 1])
            confidence = detections[0, 0, i, 2]
            xLT = int(xscale_factor * int(detections[0, 0, i, 3] * resized_width))
            xLT = xLT if xLT >= 0 else 0
            yLT = int(yscale_factor * int(detections[0, 0, i, 4] * resized_height))
            yLT = yLT if yLT >= 0 else 0
            xRB = int(xscale_factor * int(detections[0, 0, i, 5] * resized_width))
            xRB = xRB if xRB < width else width - 1            
            yRB = int(yscale_factor * int(detections[0, 0, i, 6] * resized_height))
            yRB = yRB if yRB < height else height - 1
            
            class_ids.append(classes[class_id])
            confidences.append(confidence)
            xLeftTop.append(xLT)
            yLeftTop.append(yLT)
            xRightBottom.append(xRB)
            yRightBottom.append(yRB)

        return [class_ids, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences]
    
    def detect(self, image):
        resized_image = cv2.resize(image, self.input_size)
        
        blob = cv2.dnn.blobFromImage(resized_image, self.scale_factor,
            self.input_size, self.mean_value, False)
        self.net.setInput(blob)
        detections = self.net.forward()
        
        [class_ids, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences] = self.__postprocess_detections(image,
                resized_image, detections)
        
        return [class_ids, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences]
