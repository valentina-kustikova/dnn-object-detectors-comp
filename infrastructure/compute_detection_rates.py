from data_structures import iou
from operator import attrgetter


def compute_detection_rates(gt_bboxes, dt_bboxes, percentage):
    n = 0
    fp = 0
    fn = 0
    tp = 0
    dt_idx = 0
    gt_idx = 0
    dt = dt_bboxes[dt_idx]
    gt = gt_bboxes[gt_idx]

    while True:
        while (dt_idx < len(dt_bboxes) - 1) and (dt.fid < gt.fid):
            fp += 1
            dt_idx += 1
            dt = dt_bboxes[dt_idx]
        if (dt_idx == len(dt_bboxes) - 1) and (dt.fid < gt.fid):
            fp += 1
            dt_idx = len(dt_bboxes)                
            break
        if (dt_idx == len(dt_bboxes) - 1) and (dt.fid == gt.fid):
            break

        while (gt_idx < len(gt_bboxes) - 1) and (dt.fid > gt.fid):
            n += 1
            fn += 1
            gt_idx += 1
            gt = gt_bboxes[gt_idx]
        if (gt_idx == len(gt_bboxes) - 1) and (dt.fid > gt.fid):
            n += 1
            fn += 1
            gt_idx = len(gt_bboxes)
            break
        if (gt_idx == len(gt_bboxes) - 1) and (dt.fid == gt.fid):
            break

        if dt.fid == gt.fid:
            fid = dt.fid
            fdts = []
            fgts = []
            
            while (dt_idx < len(dt_bboxes) - 1) and (dt.fid == fid):
                fdts.append(dt)
                dt_idx += 1
                dt = dt_bboxes[dt_idx]
            if (dt_idx == len(dt_bboxes) - 1) and (dt.fid == fid):
                fdts.append(dt)
            fdts = sorted(fdts, key = attrgetter('conf'), reverse = True)
            
            while (gt_idx < len(gt_bboxes) - 1) and (gt.fid == fid):
                fgts.append(gt)
                gt_idx += 1
                gt = gt_bboxes[gt_idx]
            if (gt_idx == len(gt_bboxes) - 1) and (gt.fid == fid):
                fgts.append(gt)            
            gt_status = [False for x in range(len(fgts))]
            
            n += len(fgts)
            fdt_idx = 0
            num_pairs = 0
            
            while fdt_idx < len(fdts):
                comp_dt = fdts[fdt_idx]
                fgt_idx = 0
                corr_iou = percentage
                corr_idx = -1
                
                while fgt_idx < len(fgts):
                    comp_gt = fgts[fgt_idx]
                    curr_iou = iou(comp_dt, comp_gt)
                    if (curr_iou >= corr_iou):
                        corr_iou = curr_iou
                        corr_idx= fgt_idx
                    fgt_idx += 1
                
                if (corr_idx >= 0) and (not gt_status[corr_idx]):
                    tp += 1
                    num_pairs += 1
                    gt_status[corr_idx] = True
                else:
                    fp += 1
                fdt_idx += 1
            fn += (len(fgts) - num_pairs)

    flag = False
    while dt_idx < len(dt_bboxes) - 1:
        flag = True
        fp += 1
        dt_idx += 1
        dt = dt_bboxes[dt_idx]
    if flag:
        fp += 1
    
    flag = False
    while gt_idx < len(gt_bboxes) - 1:
        flag = True
        n += 1
        fn += 1
        gt_idx += 1
        gt = gt_bboxes[gt_idx]
    if flag:
        n += 1
        fn += 1

    return [fp, fn, tp, n]
