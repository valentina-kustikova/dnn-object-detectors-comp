#!/bin/bash

CAFFE_ROOT=$PWD/../../..

export PYTHONPATH=$PYTHONPATH:$CAFFE_ROOT/python
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CAFFE_ROOT/../install/lib

python ssd_pascal.py