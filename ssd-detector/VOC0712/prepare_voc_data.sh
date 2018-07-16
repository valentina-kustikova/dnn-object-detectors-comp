#!/bin/bash

# Set default values of variables
WORKING_DIR=$PWD
DATA_DIR=$PWD
CAFFE_ROOT=$WORK_DIR/caffe
# Read options
while getopts "d:r:" option
do
  case "${option}"
  in
  d) DATA_DIR=${OPTARG};;
  r) CAFFE_ROOT=${OPTARG};;
  \?) echo "Invalid option: -${OPTARG}";;
  esac
done

# Show information
echo "Data directory: $DATA_DIR"
echo "Caffe directory: $CAFFE_ROOT"


export PYTHONPATH=$CAFFE_ROOT/python:$PYTHONPATH

# Download the model
cd $CAFFE_ROOT/models
mkdir VGGNet
cd VGGNet
wget http://cs.unc.edu/~wliu/projects/ParseNet/VGG_ILSVRC_16_layers_fc_reduced.caffemodel

# Download the data
if [ ! -d "$DATA_DIR" ]; then
  mkdir -p $DATA_DIR
fi
cd $DATA_DIR
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar

# Extract the data
tar -xvf VOCtrainval_11-May-2012.tar
tar -xvf VOCtrainval_06-Nov-2007.tar
tar -xvf VOCtest_06-Nov-2007.tar

cd $CAFFE_ROOT
# Create the trainval.txt, test.txt, and test_name_size.txt in $DATA_DIR/VOC0712/
cp $WORKING_DIR/create_list.sh ./data/VOC0712/create_list.sh
./data/VOC0712/create_list.sh -d $DATA_DIR
# Create LMDB dataset
cp $WORKING_DIR/create_data.sh ./data/VOC0712/create_data.sh
./data/VOC0712/create_data.sh -d $DATA_DIR
