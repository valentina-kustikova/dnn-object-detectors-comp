class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BoundingBox(object):
    def __init__(self, x1, y1, x2, y2):
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        self.ltp = Point(x1, y1)
        self.rbp = Point(x2, y2)

    def area(self):
        if (self.ltp.x < self.rbp.x) and (self.ltp.y < self.rbp.y):
            return (self.rbp.x - self.ltp.x + 1) *\
                   (self.rbp.y - self.ltp.y + 1)
        else:
            return 0


class GTObject(object):
    def __init__(self, fid, cid, bbox):
        self.fid = fid
        self.cid = cid
        self.bbox = bbox
        self.checked = False

    def show(self):
        print(str(self.fid) + ' ' + str(self.bbox.ltp.x) + ' ' + \
            str(self.bbox.ltp.y) + ' ' + str(self.bbox.rbp.x) + ' ' + \
            str(self.bbox.rbp.y))


class DTObject(object):
    def __init__(self, fid, cid, bbox, conf):
        self.fid = fid
        self.cid = cid
        self.bbox = bbox
        self.conf = conf

    def show(self):
        print(str(self.fid) + ' ' + str(self.bbox.ltp.x) + ' ' + \
            str(self.bbox.ltp.y) + ' ' + str(self.bbox.rbp.x) + ' ' + \
            str(self.bbox.rbp.y) + ' ' + str(self.conf))

def intersection_area(dt, gt):
    bbox = BoundingBox(max(dt.bbox.ltp.x, gt.bbox.ltp.x),
        max(dt.bbox.ltp.y, gt.bbox.ltp.y),
        min(dt.bbox.rbp.x, gt.bbox.rbp.x),
        min(dt.bbox.rbp.y, gt.bbox.rbp.y))
    return bbox.area()

def union_area(dt, gt):
    bbox = BoundingBox(max(dt.bbox.ltp.x, gt.bbox.ltp.x),
        max(dt.bbox.ltp.y, gt.bbox.ltp.y),
        min(dt.bbox.rbp.x, gt.bbox.rbp.x),
        min(dt.bbox.rbp.y, gt.bbox.rbp.y))
    return dt.bbox.area() + gt.bbox.area() - bbox.area()

def iou(dt, gt):
    i = intersection_area(dt, gt)
    u = union_area(dt, gt) # not zero
    return float(i) / float(u)

