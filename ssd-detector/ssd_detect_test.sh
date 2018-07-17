#!/bin/bash

CAFFE_ROOT="$HOME/kustikova_v/detectors/ssd/caffe"

LABEL_MAP_FILE=$CAFFE_ROOT/data/VOC0712/labelmap_voc.prototxt
MODEL_DEF_FILE=deploy.prototxt
OUTPUT_DIR=$CAFFE_ROOT/experiments

MODEL_DIR="$CAFFE_ROOT/models/ssd_vgg"
MODEL_LIST=(
            "VOC0712_300x300"
            "VOC0712Plus_300x300"
            "VOC0712_300x300_ft"
            "VOC0712_300x300_coco"
            "VOC0712Plus_300x300_ft"
            "VOC0712_512x512"
            "VOC0712Plus_512x512"
            "VOC0712_512x512_ft"
            "VOC0712_512x512_coco"
            "VOC0712Plus_512x512_ft"
           )
CAFFE_MODELS=(
              VGG_VOC0712_SSD_300x300_iter_120000.caffemodel
              VGG_VOC0712Plus_SSD_300x300_iter_240000.caffemodel
              VGG_VOC0712_SSD_300x300_ft_iter_120000.caffemodel
              VGG_coco_SSD_300x300.caffemodel
              VGG_VOC0712Plus_SSD_300x300_ft_iter_160000.caffemodel
              VGG_VOC0712_SSD_512x512_iter_120000.caffemodel
              VGG_VOC0712Plus_SSD_512x512_iter_240000.caffemodel
              VGG_VOC0712_SSD_512x512_ft_iter_120000.caffemodel
              VGG_coco_SSD_512x512.caffemodel
              VGG_VOC0712Plus_SSD_512x512_ft_iter_160000.caffemodel
             )
IMAGE_SIZE=(300 300 300 300 300 512 512 512 512 512)

DATA_DIR="$HOME/kustikova_v/data/nnov_tracks"
TRACK_LIST=(
            imgs_MOV03478
            imgs_track_09_0-2000
            imgs_track_10_5000-7000
            imgs_track_10_7000-8000
            imgs_track_10_9000-11000
           )

while getopts "r:,l:,d:" option;
do
  case "${option}"
  in
  r) CAFFE_ROOT=${OPTARG};;
  l) LABEL_MAP_FILE=${OPTARG};;
  d) DATA_DIR=${OPTARG};;
  \?) echo "Invalid option: -${OPTARG}";;
  esac
done


for i in "${!MODEL_LIST[@]}";
do
  echo "------------------------------------------------"
  echo "Testing model: ${MODEL_LIST[${i}]}"
  model_weights=${MODEL_DIR}/${MODEL_LIST[${i}]}/${CAFFE_MODELS[${i}]}
  model_def=${MODEL_DIR}/${MODEL_LIST[${i}]}/${MODEL_DEF_FILE}
  image_size=${IMAGE_SIZE[${i}]}

  for j in "${!TRACK_LIST[@]}";
  do
    image_directory=${DATA_DIR}/${TRACK_LIST[${j}]}
    echo "Images: ${image_directory}"
    output_file=${OUTPUT_DIR}/${MODEL_LIST[${i}]}_${TRACK_LIST[${j}]}.txt
    python ssd_detect.py --gpu_id 0 --labelmap_file ${LABEL_MAP_FILE} \
      --model_def ${model_def} --image_resize ${image_size} \
      --model_weights ${model_weights} --image_directory ${image_directory} \
      --output_file ${output_file}
  done
  echo "------------------------------------------------"
done
