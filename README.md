# Comparison of DNN-based object detectors

## Structure

- `infrastructure` contains scripts to estimate detection/tracking quality
  and to perform visual inspection:

  - `average_precision.py` to calculate average precision (AP)
    and draw precision-recall curve.
  - `true_positive_rate.py` to compute true positive rate (TPR).
  - `false_detection_rate.py` to calculate false detection rate (FDR).
  - `false_positives_per_frame.py` to compute number of false
    positives per frame/image.
  - `play_bboxes.py` to show groundtruth and detections simultaneously.
  - `play_tracks.py` to show constructed tracks.
  - auxiliary scripts required for AP, TPR and FDR computation.

- `ssd-detector` contains scripts to install and to execute SSD.

## References

1. Liu W., Anguelov D., Erhan D., Szegedy C., Reed S., Fu Ch.-Y., Berg A.C. SSD: Single Shot MultiBox Detector. 2016. [https://arxiv.org/abs/1512.02325].
1. Sources of SSD [https://github.com/weiliu89/caffe/tree/ssd].
