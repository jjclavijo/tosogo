#!/bin/bash

. ./PKGBUILD

echo $pkgname

curl -L ${source[0]#*::} -o ${source[0]%::*}

read checksum filename <<< $(sha256sum ${source[0]%::*})

if [ $checksum = ${sha256sums[0]} ]
then
  echo Checksum OK
else
  echo Checksum Failed
  exit 1
fi

tar xzf $filename

cd gLAB

make -j $(grep -c processor /proc/cpuinfo)

cd ..

mkdir bin

cp gLAB/gLAB_linux gLAB/gLAB_linux_multithread bin/
