#!/bin/bash

. ./PKGBUILD

mkdir src
srcdir="$(realpath ./src)"
mkdir pkg
pkgdir="$(realpath ./pkg)"
echo $pkgname

curl -L ${source[0]#*::} -o ${source[0]%::*}

# Skip checks glab web is down
#read checksum filename <<< $(sha256sum ${source[0]%::*})

#if [ $checksum = ${sha256sums[0]} ]
#then
#  echo Checksum OK
#else
#  echo Checksum Failed
#  exit 1
#fi

build

package
