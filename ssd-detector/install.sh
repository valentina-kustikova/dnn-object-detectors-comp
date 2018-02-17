#!/bin/bash

module load cuda/cuda-7.5

# Set variables
WORKING_DIR=$PWD
INSTALL_DIR_NAME=install
INSTALL_DIR=$WORKING_DIR/$INSTALL_DIR_NAME
SOURCE_DIR_NAME=dependencies
SOURCE_DIR=$WORKING_DIR/$SOURCE_DIR_NAME
CMAKE_DIR=bin/cmake
CMAKE_EXE=$INSTALL_DIR/$CMAKE_DIR


# Prepare directories
echo "Prepare directories"
cd $WORKING_DIR
mkdir $INSTALL_DIR_NAME
mkdir $SOURCE_DIR_NAME
cd $SOURCE_DIR_NAME



# BOOST
echo "-----------------------------------------------------------"
echo "Install Boost"
echo "-----------------------------------------------------------"
wget https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz
tar -xzvf boost_1_65_1.tar.gz
cd boost_1_65_1/
./bootstrap.sh --prefix=$INSTALL_DIR
./b2 install --with=all
cd ..

# GLOG
echo "-----------------------------------------------------------"
echo "Install Glog"
echo "-----------------------------------------------------------"
git clone https://github.com/google/glog
cd glog/
./autogen.sh
./configure --prefix=$INSTALL_DIR
make
make install
cd ..

# CMAKE
echo "-----------------------------------------------------------"
echo "Install CMake"
echo "-----------------------------------------------------------"
wget https://cmake.org/files/v3.9/cmake-3.9.4.tar.gz
tar -xzvf cmake-3.9.4.tar.gz
cd cmake-3.9.4/
./bootstrap --prefix=$INSTALL_DIR
make
make install
cd ..

# GFLAGS
echo "-----------------------------------------------------------"
echo "Install GFlags"
echo "-----------------------------------------------------------"
git clone https://github.com/gflags/gflags
cd gflags/
mkdir build
cd build
$CMAKE_EXE -DGFLAGS_BUILD_SHARED_LIBS=ON -DGFLAGS_BUILD_STATIC_LIBS=ON -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR -g make ..
make
make install
cd ../..

# ATLAS
echo "-----------------------------------------------------------"
echo "Install ATLAS"
echo "-----------------------------------------------------------"
wget http://www.netlib.org/lapack/lapack-3.4.1.tgz
tar -zxvf lapack-3.4.1.tgz

wget https://sourceforge.net/projects/math-atlas/files/Stable/3.10.2/atlas3.10.2.tar.bz2
tar -xvf atlas3.10.2.tar.bz2
mv ATLAS atlas-3.10.2
cd atlas-3.10.2
mkdir build
cd build
../configure --shared -b 64 --prefix=$INSTALL_DIR --with-netlib-lapack-tarfile=../../lapack-3.4.1.tgz
make
make install
cd ../../

# HDF5
echo "-----------------------------------------------------------"
echo "Install HDF5"
echo "-----------------------------------------------------------"
wget https://www.hdfgroup.org/package/gzip/\?wpdmdl=4301\&refresh=59d73056f3c771507274838
mv index.html\?wpdmdl\=4301\&refresh=59d73056f3c771507274838 hdf5-1.10.1.tar.gz
tar -zxvf hdf5-1.10.1.tar.gz
cd hdf5-1.10.1
./configure --prefix=$INSTALL_DIR --enable-build-all=yes --enable-fortran=yes --enable-cxx=yes
make
make check
make install
cd ../

# LevelDB
echo "-----------------------------------------------------------"
echo "Install LevelDB"
echo "-----------------------------------------------------------"
git clone https://github.com/google/leveldb
cd leveldb/
make
cd ../

# LMDB
echo "-----------------------------------------------------------"
echo "Install LMDB"
echo "-----------------------------------------------------------"
git clone https://github.com/LMDB/lmdb
cd lmdb/libraries/liblmdb/
make
make install
cd ../../../

# SNAPPY
echo "-----------------------------------------------------------"
echo "Install SNAPPY"
echo "-----------------------------------------------------------"
git clone https://github.com/google/snappy
cd snappy/
mkdir build
cd build/
$CMAKE_EXE -DBUILD_SHARED_LIBS=ON ../
make
make install DESTDIR=$INSTALL_DIR
cd ../../

# OpenCV
echo "-----------------------------------------------------------"
echo "Install OpenCV"
echo "-----------------------------------------------------------"
wget https://github.com/opencv/opencv/archive/3.3.0.zip
unzip 3.3.0
cd opencv-3.3.0
mkdir build
cd build
$CMAKE_EXE -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=$INSTALL_DIR ..
make -j 16
make install
cd ../../

# PROTOBUF
echo "-----------------------------------------------------------"
echo "Install Protobuf"
echo "-----------------------------------------------------------"
git clone https://github.com/google/protobuf
cd protobuf
libtoolize
aclocal
autoheader
autoconf
automake --add-missing
./autogen.sh
./configure --prefix=$INSTALL_DIR
make
make install
cd ../



# Caffe
echo "-----------------------------------------------------------"
echo "Install Caffe utilities for SSD Detector"
echo "-----------------------------------------------------------"
cd ../
git clone https://github.com/weiliu89/caffe
cd caffe
git checkout ssd
mkdir build
cd build
# path to protoc
export PATH=$PATH:$INSTALL_DIR/bin
$CMAKE_EXE \
   -DCUDA_ARCH_NAME=Kepler \
   -DBUILD_SHARED_LIBS=ON \
   -DBUILD_python=ON \
   -DLMDB_INCLUDE_DIR=$SOURCE_DIR/lmdb/libraries/liblmdb \
   -DLMDB_LIBRARIES=$SOURCE_DIR/lmdb/libraries/liblmdb/liblmdb.so \
   -DLevelDB_INCLUDE=$SOURCE_DIR/leveldb/include \
   -DLevelDB_LIBRARY=$SOURCE_DIR/leveldb/out-shared/libleveldb.so  \
   -DSnappy_INCLUDE_DIR=$SOURCE_DIR/snappy \
   -DSnappy_LIBRARIES=$SOURCE_DIR/snappy/build/libsnappy.so \
   -DGLOG_INCLUDE_DIR=$INSTALL_DIR/include \
   -DGLOG_LIBRARY=$INSTALL_DIR/lib/libglog.so \
   -DOpenCV_DIR=$INSTALL_DIR/share/OpenCV \
   -DGFLAGS_INCLUDE_DIR=$INSTALL_DIR/include \
   -DGFLAGS_LIBRARY=$INSTALL_DIR/lib/libgflags.so \
   -DProtobuf_INCLUDE_DIR=$INSTALL_DIR/include \
   -DHDF5_LIBRARIES=$INSTALL_DIR/lib/libhdf5.so \
   -DHDF5_INCLUDE_DIRS=$INSTALL_DIR/include \
   ..
make -j 16
