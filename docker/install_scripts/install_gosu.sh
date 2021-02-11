#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Copy GOSU INSTALLATION from Postgres IMAGE
GOSU_VERSION=1.11

pacman -Syu --noconfirm wget ## already installed gnupg ca-certificates
pacman -Scc ## already installed gnupg ca-certificates

arch=amd64

wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-${arch}"
wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-${arch}.asc"

export GNUPGHOME="$(mktemp -d)"

test_proxy () {
if [ -z ${http_proxy+x} ]
then
    return true
else
    return false
fi
}

if test_proxy
then
	gpg --batch --keyserver-options http-proxy=$http_proxy --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
else
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
fi

gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu
{ command -v gpgconf > /dev/null && gpgconf --kill all || :; }

rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc

chmod +x /usr/local/bin/gosu
gosu nobody true
