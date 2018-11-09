from video_detector import VideoDetector


class FullVideoDetector(VideoDetector):
    
    def __init__(self, video, detector, output_saver):
        VideoDetector.__init__(self, video, detector, None, output_saver)
        
    
    def process(self):
        # Frame identifier
        frame_idx = 0
        
        while True:
            # Read the frame
            status, frame = self.video.read()
            if not status:
                raise ValueError('The frame {} was not read'.format(frame_idx))
        
            # Detect and save objects
            print('Frame identifier: {}'.format(frame_idx))
            [class_ids, xLeftTop, yLeftTop, xRightBottom, \
                yRightBottom, confidences] = self.detector.detect(frame)
            self.output_saver.save(frame_idx, class_ids, xLeftTop, yLeftTop,
                xRightBottom, yRightBottom, confidences)
            
            # Increment frame identifier
            frame_idx += 1
        