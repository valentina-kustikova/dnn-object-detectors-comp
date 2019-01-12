#!/bin/bash

# Set default values of variables
WORKING_DIR=$PWD
INSTALL_DIR_NAME=install
SOURCE_DIR_NAME=dependencies
BUILD_PYTHON=0
BUILD_PYTHON_PACKAGES=0
BUILD_ON_CLUSTER_HEAD=0
# Read input arguments
while getopts "w:,i:,s:,p,r,m" option;
do
  case "${option}"
  in
  w)  WORKING_DIR=${OPTARG};;
  i)  INSTALL_DIR_NAME=${OPTARG};;
  s)  SOURCE_DIR_NAME=${OPTARG};;
  p)  BUILD_PYTHON=1;;
  r)  BUILD_PYTHON_PACKAGES=1;;
  m)  BUILD_ON_CLUSTER_HEAD=1;;
  \?) echo "Invalid option: -${OPTARG}";;
  esac
done

INSTALL_DIR=$WORKING_DIR/$INSTALL_DIR_NAME
SOURCE_DIR=$WORKING_DIR/$SOURCE_DIR_NAME
CMAKE_DIR=bin/cmake
CMAKE_EXE=$INSTALL_DIR/$CMAKE_DIR

# Show information
echo "Install directory: $INSTALL_DIR"
echo "Sources directory: $SOURCE_DIR"

# Prepare directories
echo "Prepare directories"
if [ ! -d "$WORKING_DIR" ]; then
  mkdir -p $WORKING_DIR
fi
cd $WORKING_DIR
if [ ! -d "$INSTALL_DIR_NAME" ]; then
  mkdir $INSTALL_DIR_NAME
fi
if [ ! -d "$SOURCE_DIR_NAME" ]; then
  mkdir $SOURCE_DIR_NAME
fi
cd $SOURCE_DIR_NAME

# Load modules on cluster head based on SLURM
if [ "$BUILD_ON_CLUSTER_HEAD" -eq "1" ]; then
  module load cuda/cuda-7.5
fi


# BOOST
echo "-----------------------------------------------------------"
echo "Install Boost"
echo "-----------------------------------------------------------"
wget http://sourceforge.net/projects/boost/files/boost/1.58.0/boost_1_58_0.tar.gz
tar -xzvf boost_1_58_0.tar.gz
cd boost_1_58_0/
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
$CMAKE_EXE -DGFLAGS_BUILD_SHARED_LIBS=ON \
  -DGFLAGS_BUILD_STATIC_LIBS=ON \
  -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR \
  -g make ..
make
make install
cd ../..

# ATLAS
echo "-----------------------------------------------------------"
echo "Install ATLAS"
echo "-----------------------------------------------------------"
wget http://www.netlib.org/lapack/lapack-3.4.1.tgz
tar -zxvf lapack-3.4.1.tgz

wget https://sourceforge.net/projects/math-atlas/files/Stable/3.10.3/atlas3.10.3.tar.bz2
tar -xvf atlas3.10.3.tar.bz2
mv ATLAS atlas-3.10.3
cd atlas-3.10.3
mkdir build
cd build
../configure --shared -b 64 --prefix=$INSTALL_DIR \
  --cripple-atlas-performance --with-netlib-lapack-tarfile=../../lapack-3.4.1.tgz
make
make install
cd lib
ar -x libcblas.a
gcc --shared -o libcblas.so -lgfortran -lm -lpthread *.o
ar -x liblapack.a
gcc --shared -o liblapack.so -lgfortran -lm -lpthread *.o
rm *.o
cp libcblas.so $INSTALL_DIR/lib
cp liblapack.so $INSTALL_DIR/lib
cd ../../../

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
mkdir build
cd build
$CMAKE_EXE -DBUILD_SHARED_LIBS=ON ../
make
make install DESTDIR=$INSTALL_DIR
cd ../../

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
make -j `nproc --all`
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


# NOTE: Install Python locally if required
echo "-----------------------------------------------------------"
echo "Install Python 2.7.14 (optional)"
echo "-----------------------------------------------------------"
if [ "$BUILD_PYTHON" -eq "1" ]; then
  wget https://www.python.org/ftp/python/2.7.14/Python-2.7.14.tgz
  tar -xzvf Python-2.7.14.tgz
  cd Python-2.7.14
  ./configure --enable-shared --prefix=$INSTALL_DIR
  make
  make install
  cd ../

  # Export paths to the installed Python
  export PATH=$INSTALL_DIR/bin:$PATH
  export LD_LIBRARY_PATH=$INSTALL_DIR/lib:$LD_LIBRARY_PATH
fi

#echo "-----------------------------------------------------------"
#echo "Install PIP (optional)"
#echo "-----------------------------------------------------------"
if [ "$BUILD_PYTHON_PACKAGES" -eq "1" ]; then
  # Install PIP if required and update environment variable
  wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py -O - | python - --user
  export PATH=$HOME/.local/bin:$PATH
fi

# Caffe
echo "-----------------------------------------------------------"
echo "Install Caffe utilities for SSD Detector"
echo "-----------------------------------------------------------"
cd ../
git clone https://github.com/weiliu89/caffe
cd caffe
git checkout ssd
# path to Caffe
export PYTHONPATH=`pwd`:$PYTHONPATH
# path to protoc
export PATH=$INSTALL_DIR/bin:$PATH
# path to libraries
export LD_LIBRARY_PATH=$INSTALL_DIR/lib:$LD_LIBRARY_PATH
# NOTE: Install all requirements if required
if [ "$BUILD_PYTHON_PACKAGES" -eq "1" ]; then
  cd python
  pip2 install --user -r requirements.txt
  cd ../
fi
mkdir build
cd build

if [ "$BUILD_PYTHON" -eq "1" ]; then
  $CMAKE_EXE \
    -DCUDA_ARCH_NAME=Kepler \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_python=ON \
    -DCMAKE_CXX_FLAGS='-std=c++11' \
    -DLMDB_INCLUDE_DIR=$SOURCE_DIR/lmdb/libraries/liblmdb \
    -DLMDB_LIBRARIES=$SOURCE_DIR/lmdb/libraries/liblmdb/liblmdb.so \
    -DLevelDB_INCLUDE=$SOURCE_DIR/leveldb/include \
    -DLevelDB_LIBRARY=$SOURCE_DIR/leveldb/build/libleveldb.so  \
    -DSnappy_INCLUDE_DIR=$SOURCE_DIR/snappy \
    -DSnappy_LIBRARIES=$SOURCE_DIR/snappy/build/libsnappy.so \
    -DGLOG_INCLUDE_DIR=$INSTALL_DIR/include \
    -DGLOG_LIBRARY=$INSTALL_DIR/lib/libglog.so \
    -DOpenCV_DIR=$INSTALL_DIR/share/OpenCV \
    -DGFLAGS_INCLUDE_DIR=$INSTALL_DIR/include \
    -DGFLAGS_LIBRARY=$INSTALL_DIR/lib/libgflags.so \
    -DProtobuf_INCLUDE_DIR=$INSTALL_DIR/include \
    -DAtlas_CBLAS_INCLUDE_DIR=$SOURCE_DIR/atlas-3.10.3/include \
    -DAtlas_CLAPACK_INCLUDE_DIR=$SOURCE_DIR/atlas-3.10.3/include \
    -DAtlas_BLAS_LIBRARY=$INSTALL_DIR/lib/libsatlas.so \
    -DAtlas_CBLAS_LIBRARY=$SOURCE_DIR/atlas-3.10.3/build/lib/libcblas.so \
    -DAtlas_LAPACK_LIBRARY=$SOURCE_DIR/atlas-3.10.3/build/lib/liblapack.so \
    -DPYTHON_INCLUDE_DIR=$INSTALL_DIR/include/python2.7 \
    -DPYTHON_LIBRARY=$INSTALL_DIR/lib/libpython2.7.so \
    -DPYTHON_EXECUTABLE=$INSTALL_DIR/bin/python \
    ..
else
  $CMAKE_EXE \
    -DCUDA_ARCH_NAME=Kepler \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_python=ON \
    -DCMAKE_CXX_FLAGS='-std=c++11' \
    -DLMDB_INCLUDE_DIR=$SOURCE_DIR/lmdb/libraries/liblmdb \
    -DLMDB_LIBRARIES=$SOURCE_DIR/lmdb/libraries/liblmdb/liblmdb.so \
    -DLevelDB_INCLUDE=$SOURCE_DIR/leveldb/include \
    -DLevelDB_LIBRARY=$SOURCE_DIR/leveldb/build/libleveldb.so  \
    -DSnappy_INCLUDE_DIR=$SOURCE_DIR/snappy \
    -DSnappy_LIBRARIES=$SOURCE_DIR/snappy/build/libsnappy.so \
    -DGLOG_INCLUDE_DIR=$INSTALL_DIR/include \
    -DGLOG_LIBRARY=$INSTALL_DIR/lib/libglog.so \
    -DOpenCV_DIR=$INSTALL_DIR/share/OpenCV \
    -DGFLAGS_INCLUDE_DIR=$INSTALL_DIR/include \
    -DGFLAGS_LIBRARY=$INSTALL_DIR/lib/libgflags.so \
    -DProtobuf_INCLUDE_DIR=$INSTALL_DIR/include \
    -DAtlas_CBLAS_INCLUDE_DIR=$SOURCE_DIR/atlas-3.10.3/include \
    -DAtlas_CLAPACK_INCLUDE_DIR=$SOURCE_DIR/atlas-3.10.3/include \
    -DAtlas_BLAS_LIBRARY=$INSTALL_DIR/lib/libsatlas.so \
    -DAtlas_CBLAS_LIBRARY=$SOURCE_DIR/atlas-3.10.3/build/lib/libcblas.so \
    -DAtlas_LAPACK_LIBRARY=$SOURCE_DIR/atlas-3.10.3/build/lib/liblapack.so \
    ..
fi

make -j `nproc --all`
