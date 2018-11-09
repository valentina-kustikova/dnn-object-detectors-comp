from output_saver import OutputSaver


class FileOutputSaver(OutputSaver):
    
    def __init__(self, output):
        OutputSaver.__init__(self, output)
            
    def save(self, frame_idx, class_ids, xLeftTop, yLeftTop,
             xRightBottom, yRightBottom, confidences):
        file = open(self.output, 'a+')
        for idx in range(len(class_ids)):
            file.write('{0:06d} {1} {2} {3} {4} {5} {6}\n'.format(
                frame_idx, class_ids[idx], xLeftTop[idx], yLeftTop[idx],
                xRightBottom[idx], yRightBottom[idx], confidences[idx]))
        file.close()
