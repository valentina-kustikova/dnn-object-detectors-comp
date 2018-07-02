from operator import attrgetter
from data_structures import BoundingBox, GTObject, DTObject


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


def compute_detection_rates(gt_bboxes, dt_bboxes, percentage):
    n = 0
    fp = 0
    fn = 0
    tp = 0
    dt_idx = 0
    gt_idx = 0
    dt = dt_bboxes.pop(dt_idx)
    dt_bboxes.insert(dt_idx, dt)
    gt = gt_bboxes.pop(gt_idx)
    gt_bboxes.insert(gt_idx, gt)

    while True:
        while (dt_idx < len(dt_bboxes) - 1) and (dt.fid < gt.fid):
            fp += 1
            dt_idx += 1
            dt = dt_bboxes.pop(dt_idx)
            dt_bboxes.insert(dt_idx, dt)
        if dt_idx == len(dt_bboxes) - 1:
            break

        while (gt_idx < len(gt_bboxes) - 1) and (dt.fid > gt.fid):
            n += 1
            fn += 1
            gt_idx += 1
            gt = gt_bboxes.pop(gt_idx)
            gt_bboxes.insert(gt_idx, gt)
        if gt_idx == len(gt_bboxes) - 1:
            break

        if dt.fid == gt.fid:
            fid = dt.fid
            fdts = []
            fgts = []
            while (dt_idx < len(dt_bboxes) - 1) and (dt.fid == fid):
                fdts.append(dt)
                dt_idx += 1
                dt = dt_bboxes.pop(dt_idx)
                dt_bboxes.insert(dt_idx, dt)
            if (dt_idx == len(dt_bboxes) - 1) and (dt.fid == fid):
                fdts.append(dt)
            sorted(fdts, key = attrgetter('conf'), reverse = True)
            while (gt_idx < len(gt_bboxes) - 1) and (gt.fid == fid):
                fgts.append(gt)
                gt_idx += 1
                gt = gt_bboxes.pop(gt_idx)
                gt_bboxes.insert(gt_idx, gt)
            if (gt_idx == len(gt_bboxes) - 1) and (gt.fid == fid):
                fgts.append(gt)
            n += len(fgts)
            fdt_idx = len(fdts) - 1
            num_pairs = 0
            num_bboxes = len(fgts)
            while fdt_idx >= 0:
                comp_dt = fdts.pop(fdt_idx)
                fgt_idx = len(fgts) - 1
                corr_iou = 0
                corr_idx = -1
                while fgt_idx >= 0:
                    comp_gt = fgts.pop(fgt_idx)
                    curr_iou = iou(comp_dt, comp_gt)
                    if (curr_iou >= percentage) and (curr_iou > corr_iou):
                        corr_iou = curr_iou
                        corr_idx= fgt_idx
                    fgts.insert(fgt_idx, comp_gt)
                    fgt_idx -= 1
                if corr_idx >= 0:
                    tp += 1
                    num_pairs += 1
                else:
                    fp += 1
                fdt_idx -= 1
            fn += (num_bboxes - num_pairs)

    flag = False
    while dt_idx < len(dt_bboxes) - 1:
        flag = True
        fp += 1
        dt_idx += 1
        dt = dt_bboxes.pop(dt_idx)
        dt_bboxes.insert(dt_idx, dt)

    if flag:
        fp += 1
    flag = False
    while gt_idx < len(gt_bboxes) - 1:
        flag = True
        n += 1
        fn += 1
        gt_idx += 1
        gt = gt_bboxes.pop(gt_idx)
        gt_bboxes.insert(gt_idx, gt)
    if flag:
        n += 1
        fn += 1

    return [fp, fn, tp, n]
