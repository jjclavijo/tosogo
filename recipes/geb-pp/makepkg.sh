#!/bin/bash


mkdir src
srcdir="$(realpath ./src)"
mkdir pkg
pkgdir="$(realpath ./pkg)"

. ./PKGBUILD

echo $pkgname

_pkgfile=$srcdir/${source[0]%::*}

curl -L ${source[0]#*::} -o $_pkgfile

# Skip checks glab web is down
read checksum filename <<< $(sha256sum $_pkgfile)

if [ $checksum = ${sha256sums[0]} ]
then
  echo Checksum OK
else
  echo Checksum Failed
  exit 1
fi

prepare

build

package
