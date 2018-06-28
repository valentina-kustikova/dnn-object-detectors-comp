import os.path
import re
from data_structures import BoundingBox, DTObject

def read_detections(dt, objclass):
    if not os.path.isfile(dt):
        raise Exception('File \'{0}\' does not exists'.format(dt))

    dt_file = open(dt, 'r')
    dt_bboxes = []
    for line in dt_file:
        matcher = re.match(
            r'([\d]+)[.\w]*[ ]+([\w]+)[ ]+([-\d]+)[ ]+([-\d]+)[ ]+([\d]+)[ ]+([\d]+)[ ]+([0-9\.]+)',
            line)
        if matcher:
            fid = int(matcher.group(1))
            cid = matcher.group(2)
            bbox = BoundingBox(int(matcher.group(3)), int(matcher.group(4)),
                int(matcher.group(5)), int(matcher.group(6)))
            conf = float(matcher.group(7))
            if cid.lower() == objclass.lower():
                dt_object = DTObject(fid, bbox, conf)
                dt_bboxes.append(dt_object)
        else:
            raise Exception('File \'{0}\' contains not matched line \'{1}\''.
                format(dt, line))

    return dt_bboxes
