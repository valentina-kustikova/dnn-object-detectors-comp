from video_detector import VideoDetector


class StepwiseVideoDetector(VideoDetector):
    
    def __init__(self, video, detector, tracker, output_saver):
        VideoDetector.__init__(self, video, detector, tracker, output_saver)
    
    def __convert_bboxes2rois(self, xLeftTop, yLeftTop, xRightBottom,
            yRightBottom):
        size = len(xLeftTop)
        rois = []
        for idx in range(size):
            rois.append((xLeftTop[idx], yLeftTop[idx],
                xRightBottom[idx] - xLeftTop[idx] + 1,
                yRightBottom[idx] - yLeftTop[idx] + 1)
        return rois
    
    def __combine_dt_tr(self, dt_class_ids, dt_xLeftTop, dt_yLeftTop,
            dt_xRightBottom, dt_yRightBottom, dt_confidences,
            tr_xLeftTop, tr_yLeftTop, tr_xRightBottom, tr_yRightBottom):
        threshold = 0.5
        sindeces_dt_confidencies = \
            [ e[0] for e in sorted(enumerate(dt_confidences), \
                key = lambda x : x[1]) ]
        tracked_obj_num = len(tr_xLeftTop)
        flags = [-1 for i in range(tracked_obj_num)]
        for idx in sindeces_dt_confidencies:
            dt_x1 = dt_xLeftTop[idx]
            dt_y1 = dt_yLeftTop[idx]
            dt_x2 = dt_xRightBottom[idx]
            dt_y2 = dt_yRightBottom[idx]
            dt_s = (dt_x2 - dt_x1 + 1) * (dt_y2 - dt_y1 + 1)
            iou_max = 0
            iou_idx = -1
            for i in range(tracked_obj_num):
                tr_x1 = tr_xLeftTop[idx]
                tr_y1 = tr_yLeftTop[idx]
                tr_x2 = tr_xRightBottom[idx]
                tr_y2 = tr_yRightBottom[idx]
                tr_s = (tr_x2 - tr_x1 + 1) * (tr_x2 - tr_x1 + 1)
                intersection = (min(dt_x2, tr_x2) - max(dt_x1, tr_x1) + 1) * \
                    (min(dt_y2, tr_y2) - max(dt_y1, tr_y1) + 1)
                union = dt_s + tr_s - intersection
                iou = intersection / union
                if iou > iou_max:
                    iou_max = iou
                    iou_idx = i
            if (iou > threshold) and (flags[iou_idx] == -1):
                flags[iou_idx] = idx
        
        return [class_ids, xLeftTop, yLeftTop, \
                xRightBottom, yRightBottom, confidences]
    
    def process(self):
        # Frame identifier
        frame_idx = 0
        # Read the frame
        status, frame = self.video.read()
        if not status:
            raise ValueError('The frame {} was not read'.format(frame_idx))
        
        # Detect objects at the frame t
        print('Frame identifier: {}'.format(frame_idx))
        [class_ids, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences] = self.detector.detect(frame)
        
        # Save detected bounding boxes
        self.obj_class_ids.append(class_ids)
        self.obj_confidencies.append(confidences)
        self.obj_xLeftTop.append(xLeftTop)
        self.obj_yLeftTop.append(yLeftTop)
        self.obj_xRightBottom.append(xRightBottom)
        self.obj_yRightBottom.append(yRightBottom)
        self.obj_tracks = [ self.obj_tracks.append([ i ]) \ 
            for i in range(len(class_ids)) ]
        self.output_saver.save(frame_idx, class_ids, xLeftTop, yLeftTop,
            xRightBottom, yRightBottom, confidences)
        
        # Increment frame identifier
        frame_idx += 1
        
        while True:
            # Read the frame
            print('Frame identifier: {}'.format(frame_idx))
            status, next_frame = self.video.read()
            if not status:
                raise ValueError('The frame {} was not read'.format(frame_idx))
            
            # Track objects from the frame t to the frame t+1
            rois = self.__convert_bboxes2rois(xLeftTop, yLeftTop,
                xRightBottom, yRightBottom)
            self.tracker.update_track_rois(frame, rois)
            [tr_xLeftTop, tr_yLeftTop, tr_xRightBottom, \
                tr_yRightBottom] = self.tracker.track(next_frame)
        
            # Detect objects at the frame t+1            
            [dt_class_ids, dt_xLeftTop, dt_yLeftTop, dt_xRightBottom, \
                dt_yRightBottom, dt_confidences] = self.detector.detect(frame)
            
            # Combine detected and tracked bounding boxes
            [class_ids, xLeftTop, yLeftTop, \
                xRightBottom, yRightBottom, confidences] = \
                    self.__combine_dt_tr(dt_class_ids,
                        dt_xLeftTop, dt_yLeftTop,
                        dt_xRightBottom, dt_yRightBottom, dt_confidences,
                        bbox_indeces, tr_xLeftTop, tr_yLeftTop,
                        tr_xRightBottom, tr_yRightBottom)
            # Save combined results
            self.obj_class_ids.append(class_ids)
            self.obj_confidencies.append(confidences)
            self.obj_xLeftTop.append(xLeftTop)
            self.obj_yLeftTop.append(yLeftTop)
            self.obj_xRightBottom.append(xRightBottom)
            self.obj_yRightBottom.append(yRightBottom)            
            self.output_saver.save(frame_idx, class_ids, xLeftTop, yLeftTop,
                xRightBottom, yRightBottom, confidences)
            
            # Increment frame identifier
            frame_idx += 1
        