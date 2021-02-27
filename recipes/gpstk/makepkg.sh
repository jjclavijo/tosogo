#!/bin/bash

source ./PKGBUILD

mkdir src
srcdir="$(realpath ./src)"
mkdir pkg
pkgdir="$(realpath ./pkg)"

read _tarurl <<< $(echo $source)

#git clone "$_giturl" "$srcdir/$_gitname"

pushd "$srcdir"
curl -O -J "$_tarurl"
tar xzf *.tar.gz
popd

prepare

build

package
