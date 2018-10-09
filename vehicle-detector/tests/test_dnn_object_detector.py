import argparse
import cv2
import sys

sys.path.append('../detector')

from dnn_object_detector import CaffeDNNObjectDetector


def show_detections(image, class_ids, xLeftTop, yLeftTop, xRightBottom,
        yRightBottom, confidences):
    num_bboxes = len(confidences)
    for i in range(num_bboxes):
        cv2.rectangle(image, (xLeftTop[i], yLeftTop[i]),
            (xRightBottom[i], yRightBottom[i]), (0, 255, 0))
        
        text = class_ids[i] + ': ' + str(confidences[i])
        
        labelSize, baseLine = cv2.getTextSize(text,
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        yLT = max(yLeftTop[i], labelSize[1])
        cv2.rectangle(image, (xLeftTop[i], yLT - labelSize[1]),
            (xLeftTop[i] + labelSize[0], yLT + baseLine),
            (255, 255, 255), cv2.FILLED)
        cv2.putText(image, text, (xLeftTop[i], yLT),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", image)
    if cv2.waitKey(10) == 27:
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', default = 'image.jpg',
        help = 'image name')
    parser.add_argument('-t', '--trained_model',
        default = 'MobileNetSSD_deploy.caffemodel',
        help = 'model file (.caffemodel)')
    parser.add_argument('-p', '--prototxt',
        default = 'MobileNetSSD_deploy.prototxt',
        help = 'model description (.prototxt)')
    parser.add_argument('-l', '--labels', default = 'voc_classes.txt',
        help = 'file containing network labels in format \'<id> <class_name>\'')
    parser.add_argument('-m', '--mean', default = 127.5, help = 'mean value')
    parser.add_argument('-c', '--cols', default = 300, help = 'input width (cols)')
    parser.add_argument('-r', '--rows', default = 300, help = 'input height (rows)')
    parser.add_argument('-s', '--scale_factor', default = 0.007843,
        help = 'scale factor for the input blob')
    args = parser.parse_args()
    
    image = cv2.imread(args.image, cv2.IMREAD_COLOR)
    detector = CaffeDNNObjectDetector(args.trained_model, args.prototxt,
        args.labels, args.cols, args.rows, args.mean, args.scale_factor)
    [class_ids, xLeftTop, yLeftTop, xRightBottom, \
        yRightBottom, confidences] = detector.detect(image)
    show_detections(image, class_ids, xLeftTop, yLeftTop, xRightBottom, \
        yRightBottom, confidences)
    