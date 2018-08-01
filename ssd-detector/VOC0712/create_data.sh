#!/bin/bash

# Base version of this script is placed
# in the official repository
# https://github.com/weiliu89/caffe/tree/ssd/data/VOC0712

cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
root_dir=$cur_dir/../..

cd $root_dir

redo=1
data_root_dir="$HOME/Documents/data/VOCdevkit"
while getopts "d:" option;
do
  case "${option}"
  in
  d)  data_root_dir=${OPTARG};;
  \?) echo "Invalid option: -${OPTARG}";;
  esac
done
dataset_name="VOC0712"
mapfile="$root_dir/data/$dataset_name/labelmap_voc.prototxt"
echo "Data root directory: ${data_root_dir}"
echo "Map file: ${mapfile}"

anno_type="detection"
db="lmdb"
min_dim=0
max_dim=0
width=0
height=0

extra_cmd="--encode-type=jpg --encoded"
if [ $redo ]
then
  extra_cmd="$extra_cmd --redo"
fi
for subset in test trainval
do
  python $root_dir/scripts/create_annoset.py --anno-type=$anno_type \
    --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim \
    --resize-width=$width --resize-height=$height --check-label \
    $extra_cmd $data_root_dir $root_dir/data/$dataset_name/$subset.txt \
    $data_root_dir/$dataset_name/$db/$dataset_name"_"$subset"_"$db \
    examples/$dataset_name
done
