import os.path
import re
from data_structures import BoundingBox, GTObject

def read_groundtruth(gt, objclass = 'all'):
    if not os.path.isfile(gt):
        raise Exception('File \'{0}\' does not exists'.format(gt))

    gt_file = open(gt, 'r')
    gt_bboxes = []
    for line in gt_file:
        matcher = re.match(
            r'([\d]+)[ ]+([\w]+)[ ]+([\d]+)[ ]+([\d]+)[ ]+([\d]+)[ ]+([\d]+)',
            line)
        if matcher:
            fid = int(matcher.group(1))
            cid = matcher.group(2)
            bbox = BoundingBox(int(matcher.group(3)), int(matcher.group(4)),
                int(matcher.group(5)), int(matcher.group(6)))
            if (objclass.lower() == 'all') or (cid.lower() == objclass.lower()):
                gt_object = GTObject(fid, bbox)
                gt_bboxes.append(gt_object)
        else:
            raise Exception('File \'{0}\' contains not matched line \'{1}\''.
                format(gt, line))

    return gt_bboxes
