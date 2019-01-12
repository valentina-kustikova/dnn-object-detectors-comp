from output_saver import OutputSaver


class StdOutputSaver(OutputSaver):
    
    def __init__(self):
        OutputSaver.__init__(self)
        
    def save(self, frame_idx, class_ids, xLeftTop, yLeftTop,
             xRightBottom, yRightBottom, confidences, trackIds = None):
        if (trackIds is not None):
            for idx in range(len(class_ids)):
                print('{0:06d} {1} {2} {3} {4} {5} {6} {7}'.format(
                    frame_idx, class_ids[idx], xLeftTop[idx], yLeftTop[idx],
                    xRightBottom[idx], yRightBottom[idx], confidences[idx],
                    trackIds[idx]))
        else:
            for idx in range(len(class_ids)):
                print('{0:06d} {1} {2} {3} {4} {5} {6}'.format(
                    frame_idx, class_ids[idx], xLeftTop[idx], yLeftTop[idx],
                    xRightBottom[idx], yRightBottom[idx], confidences[idx]))
        return