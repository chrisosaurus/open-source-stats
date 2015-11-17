#!/usr/bin/env bash
# run me as sudo
set -c

apt-get update
apt-get install git build-essential python3 sqlite3 python3-pip

# from http://www.pygit2.org/install.html#quick-install
wget https://github.com/libgit2/libgit2/archive/v0.23.2.tar.gz
tar xzf v0.23.2.tar.gz
cd libgit2-0.23.2/
cmake .
make
make install
cd ..

pip3 install pygit2

