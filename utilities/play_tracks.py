import os
import argparse
import cv2
import numpy as np
from read_groundtruth import read_groundtruth
from read_detections import read_detections
from auxiliary_functions import list_images


def generate_colors(k):
    return [np.uint8(np.random.uniform(0, 255, 3)) for i in range(k)]


def read_bboxes(bboxes_file):
    bboxes = []
    try:
        bboxes = read_groundtruth(bboxes_file)
    except:
        bboxes = read_detections(bboxes_file)
    return bboxes


def read_tracks(tracks_file):
    if not os.path.isfile(tracks_file):
        raise Exception('File \'{0}\' does not exists'.format(tracks_file))

    file = open(tracks_file, 'r')
    tracks = []
    for line in file:
        ids = line.split()
        # first elements contains track lenght
        tracks.append([int(ids[i]) for i in range(1, len(ids))])
    return tracks


def set_track_ids(kbboxes, tracks):
    bbox_track_ids = [-1 for i in range(kbboxes)]
    for track_id in range(len(tracks)):
        for i in range(len(tracks[track_id])):
            bbox_track_ids[tracks[track_id][i]] = track_id
    return bbox_track_ids


def get_img_bboxes(bboxes, fid):
    img_bboxes_ids = [idx for idx in range(len(bboxes)) \
        if bboxes[idx].fid == fid]        
    return img_bboxes_ids


def play_tracks(img_dir, bboxes_file, tracks_file):
    img_list = list_images(img_dir)
    bboxes = read_bboxes(bboxes_file)    
    tracks = read_tracks(tracks_file)
    
    bbox_track_ids = set_track_ids(len(bboxes), tracks)
    track_colors = generate_colors(len(tracks))
    for img_full_name in img_list:
        img = cv2.imread(img_full_name)
        img_name = os.path.basename(img_full_name)
        img_name, img_ext = os.path.splitext(img_name)
        fid = int(img_name)
        indeces = get_img_bboxes(bboxes, fid)
        for idx in indeces:
            bbox = bboxes[idx]
            track_id = bbox_track_ids[idx]
            color_id = tuple(map(int, track_colors[track_id]))
            cv2.rectangle(img, (bbox.bbox.ltp.x, bbox.bbox.ltp.y),
                (bbox.bbox.rbp.x, bbox.bbox.rbp.y), color_id, 2)
            cv2.putText(img, str(track_id),
                (bbox.bbox.ltp.x + 7, bbox.bbox.ltp.y + 17),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_id, 2)
        cv2.imshow('Image', img)
        key = cv2.waitKey(0)
        if key == 27:
            break
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bboxes', help = 'bounding boxes (file)')
    parser.add_argument('-t', '--tracks', help = 'tracks (file)')
    parser.add_argument('-dir', '--image_directory', help = 'image directory')
    args = parser.parse_args()
    
    # play tracks
    play_tracks(args.image_directory, args.bboxes, args.tracks)
