import argparse
import sys
import cv2

sys.path.append('../tracker')

from opencv_object_tracker import OpenCVObjectTracker


def show_track(frame, roi, next_frame, next_roi):
    cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]),
        (0, 255, 0), 1)
    cv2.namedWindow('Current frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Current frame', frame)
    
    cv2.rectangle(next_frame, (next_roi[0], next_roi[1]),
        (next_roi[0] + next_roi[2], next_roi[1] + next_roi[3]), (0, 255, 0), 1)
    cv2.namedWindow('Next frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Next frame', next_frame)
    if cv2.waitKey(10) == 27:
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--frame', default = 'frame.jpg',
        help = 'initial frame')
    parser.add_argument('-r', '--roi', default = '334 50 189 116',
        help = 'tracked region of interest')
    parser.add_argument('-n', '--next_frame', default = 'next_frame.jpg',
        help = 'next frame')
    parser.add_argument('-t', '--tracker_name', default = 'MEDIANFLOW',
        help = 'tracker name supported by OpenCV \
            (\'BOOSTING\', \'MIL\', \'KCF\', \'TLD\', \'MEDIANFLOW\', \
            \'GOTURN\', \'MOSSE\', \'CSRT\')')
    args = parser.parse_args()
    
    frame = cv2.imread(args.frame, cv2.IMREAD_COLOR)
    roi = [ int(x) for x in args.roi.split() ]
    next_frame = cv2.imread(args.next_frame, cv2.IMREAD_COLOR)
    tracker = OpenCVObjectTracker(frame, tuple(roi), args.tracker_name)
    next_roi = tracker.track(next_frame)
    show_track(frame, roi, next_frame, next_roi)
