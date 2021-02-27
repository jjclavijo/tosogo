#!/bin/bash

source ./PKGBUILD

mkdir src
srcdir="$(realpath ./src)"
mkdir pkg
pkgdir="$(realpath ./pkg)"

read _gitname _giturl _gitbranch <<< $(echo $source | sed 's/::git+/ /;s/#branch=/ /')

git clone "$_giturl" "$srcdir/$_gitname"
pushd "$srcdir/$_gitname"
git checkout $_gitbranch
popd

build

package
