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
                yRightBottom[idx] - yLeftTop[idx] + 1))
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
                if (tr_x1 == -1) or (tr_x2 == -1) or \
                   (tr_y1 == -1) or (tr_y2 == -1):
                    break;
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
        
        return flags
    
    def process(self):
        # Frame identifier
        frame_idx = 0
        # Read the frame
        status, frame = self.video.read()
        if not status:
            raise ValueError('The frame {} was not read'.format(frame_idx))
        
        # Detect objects at the frame (t = 0)
        print('Frame identifier: {}'.format(frame_idx))
        [classIds, xLeftTop, yLeftTop, xRightBottom, \
            yRightBottom, confidences] = self.detector.detect(frame)
        trackIds = [ self.obj_tracks.append(i) for i in range(len(classIds)) ]
        # Set first free track identifier
        free_track_id = len(class_ids)
        
        # Save detected bounding boxes for the frame (t = 0)
        self.obj_class_ids.append(classIds)
        self.obj_confidencies.append(confidences)
        self.obj_xLeftTop.append(xLeftTop)
        self.obj_yLeftTop.append(yLeftTop)
        self.obj_xRightBottom.append(xRightBottom)
        self.obj_yRightBottom.append(yRightBottom)
        self.obj_trackIds.append(trackIds)
        self.output_saver.save(frame_idx, classIds, xLeftTop, yLeftTop,
            xRightBottom, yRightBottom, confidences, trackIds)
        
        # Increment frame identifier
        frame_idx += 1
        # Main loop for the next frames
        while True:
            # Read the frame
            print('Frame identifier: {}'.format(frame_idx))
            status, next_frame = self.video.read()
            if not status:
                raise ValueError('The frame {} was not read'.format(frame_idx))
            
            # Track objects from the frame (t) to the frame (t+1)
            rois = self.__convert_bboxes2rois(xLeftTop, yLeftTop,
                xRightBottom, yRightBottom)
            self.tracker.update_track_rois(frame, rois)
            [tr_xLeftTop, tr_yLeftTop, tr_xRightBottom, \
                tr_yRightBottom] = self.tracker.track(next_frame)
        
            # Detect objects at the frame (t+1)
            [dt_class_ids, dt_xLeftTop, dt_yLeftTop, dt_xRightBottom, \
                dt_yRightBottom, dt_confidences] = self.detector.detect(frame)
            
            # Combine detected and tracked bounding boxes, i.e. find correspondences
            #     <detected bbox at the frame (t)> ==
            #     <tracked bbox at the frame (t+1)> ->
            #     <detected bbox at the frame (t+1)>
            flags = self.__combine_dt_tr(dt_class_ids,
                dt_xLeftTop, dt_yLeftTop, dt_xRightBottom, dt_yRightBottom,
                dt_confidences, tr_xLeftTop, tr_yLeftTop, tr_xRightBottom,
                tr_yRightBottom)
            
            # Create bounding boxes for the frame t+1
            # 1. Clear containers
            xLeftTop.clear()
            yLeftTop.clear()
            xRightBottom.clear()
            yRightBottom.clear()
            classIds.clear()
            confidencies.clear()
            # 2. Continue existing tracks (detected bboxes at the frame (t+1)
            #    that have corresponding bbox at the frame (t))
            existing_tracks = []
            for prev_dt_idx in range(len(flags)):
                if (flags[prev_dt_idx] == -1):
                    # The track is over
                    break                
                # TODO: construct average detected and tracked bounding box
                dt_idx = flags[prev_dt_idx]
                classIds.append(dt_class_ids[dt_idx])
                confidencies.append(dt_confidences[dt_idx])
                xLeftTop.append(dt_xLeftTop[dt_idx])
                yLeftTop.append(dt_yLeftTop[dt_idx])
                xRightBottom.append(dt_xRightBottom[dt_idx])
                yRightBottom.append(dt_yRightBottom[dt_idx])
                existing_tracks.append(trackIds[prev_dt_idx])
            trackIds.clear()
            trackIds.append(existing_tracks)
            # 3. Add new objects and create new tracks
            for dt_idx in range(len(dt_confidences)):
                if dt_idx not in flags:
                    classIds.append(dt_class_ids[dt_idx])
                    confidencies.append(dt_confidences[dt_idx])
                    xLeftTop.append(dt_xLeftTop[dt_idx])
                    yLeftTop.append(dt_yLeftTop[dt_idx])
                    xRightBottom.append(dt_xRightBottom[dt_idx])
                    yRightBottom.append(dt_yRightBottom[dt_idx])
                    trackIds.append(free_track_id)
                    free_track_id += 1
            self.obj_class_ids.append(class_ids)
            self.obj_confidencies.append(confidences)
            self.obj_xLeftTop.append(xLeftTop)
            self.obj_yLeftTop.append(yLeftTop)
            self.obj_xRightBottom.append(xRightBottom)
            self.obj_yRightBottom.append(yRightBottom)
            self.obj_trackIds.append(trackIds)
            
            # Save results for the frame (t+1)
            self.output_saver.save(frame_idx, class_ids, xLeftTop, yLeftTop,
                xRightBottom, yRightBottom, confidences, trackIds)
            
            # Increment frame identifier
            frame_idx += 1
