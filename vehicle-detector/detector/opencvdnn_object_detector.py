import cv2
import re
import numpy as np
from object_detector import ObjectDetector


class OpenCVDNNObjectDetector(ObjectDetector):
    
    def __init__(self, framework, weights_file_name, model_file_name,
            classes_file_name, input_width, input_height, mean_value,
            scale_factor, bgr, threshold):
        ObjectDetector.__init__(self, weights_file_name)
        self.model_file_name = model_file_name
        self.classes_file_name = classes_file_name
        self.net = cv2.dnn.readNet(model_file_name, weights_file_name,
            framework)
        self.input_size = (input_width, input_height)
        self.mean_value = mean_value
        self.scale_factor = scale_factor
        self.threshold = threshold
        if bgr == 'bgr':
            self.reorder_channels = False
        elif bgr == 'rgb':
            self.reorder_channels = True
        else:
            raise ValueError('Unsupported channel sequence')
    
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
    
    def __postprocess_detections(self, image, resized_image, detections, im_info):
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
        
        layer_names = self.net.getLayerNames()
        last_layer_id = self.net.getLayerId(layer_names[-1])
        last_layer = self.net.getLayer(last_layer_id)
        
        if im_info != -1: # Faster R-CNN or R-FCN
            for i in range(detections.shape[2]):
                class_id = int(detections[0, 0, i, 1])
                confidence = detections[0, 0, i, 2]
                if confidence < self.threshold:
                    continue
                xLT = int(xscale_factor * detections[0, 0, i, 3])
                xLT = xLT if xLT >= 0 else 0
                yLT = int(yscale_factor * detections[0, 0, i, 4])
                yLT = yLT if yLT >= 0 else 0
                xRB = int(xscale_factor * detections[0, 0, i, 5])
                xRB = xRB if xRB < width else width - 1            
                yRB = int(yscale_factor * detections[0, 0, i, 6])
                yRB = yRB if yRB < height else height - 1
                
                class_ids.append(classes[class_id])
                confidences.append(confidence)
                xLeftTop.append(xLT)
                yLeftTop.append(yLT)
                xRightBottom.append(xRB)
                yRightBottom.append(yRB)
        elif last_layer.type == 'DetectionOutput': # SSD
            for i in range(detections.shape[2]):
                class_id = int(detections[0, 0, i, 1])
                confidence = detections[0, 0, i, 2]
                if confidence < self.threshold:
                    continue
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
        elif last_layer.type == 'Region': # YOLO
            for i in range(detections.shape[0]):
                scores = detections[i, 5:]
                class_id = np.argmax(scores)
                confidence = float(scores[class_id])
                class_id += 1 # scores don't contain background
                if confidence < self.threshold:
                    continue
                center_x = int(detections[i, 0] * resized_width)
                center_y = int(detections[i, 1] * resized_height)
                bbox_width = int(detections[i, 2] * resized_width)
                bbox_height = int(detections[i, 3] * resized_height)
                
                xLT = int(xscale_factor * (center_x - bbox_width / 2))
                xLT = xLT if xLT >= 0 else 0
                yLT = int(yscale_factor * (center_y - bbox_height / 2))
                yLT = yLT if yLT >= 0 else 0
                xRB = int(xscale_factor * (center_x + bbox_width / 2))
                xRB = xRB if xRB < width else width - 1            
                yRB = int(yscale_factor * (center_y + bbox_height / 2))
                yRB = yRB if yRB < height else height - 1
                
                class_ids.append(classes[class_id])
                confidences.append(confidence)
                xLeftTop.append(xLT)
                yLeftTop.append(yLT)
                xRightBottom.append(xRB)
                yRightBottom.append(yRB)
        else:
            raise ValueError('Unsupported output layer {}'.
			    format(last_layer.type))

        return [class_ids, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences]
    
    def detect(self, image):
        resized_image = cv2.resize(image, self.input_size)
  
        blob = cv2.dnn.blobFromImage(resized_image, self.scale_factor,
            self.input_size, self.mean_value, self.reorder_channels)
        self.net.setInput(blob)
        if self.net.getLayer(0).outputNameToIndex('im_info') != -1:
            self.net.setInput(
                np.array([[self.input_size[0], self.input_size[1], 1.6]],
                           dtype = np.float32), 'im_info')
        detections = self.net.forward()
        
        [class_ids, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences] = self.__postprocess_detections(image,
                resized_image, detections,
                self.net.getLayer(0).outputNameToIndex('im_info'))
        
        return [class_ids, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences]
