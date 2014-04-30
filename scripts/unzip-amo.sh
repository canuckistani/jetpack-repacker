#!/bin/bash

# `ftp` folder should be a clone of ftp://ftp.mozilla.org/pub/mozilla.org/addons/
# `src` will contain unzipped addons content
# `src/jetpack/` will contain all jetpack addons
# `src/xul` will contain other kind of addons

FTP_DIR=$1
SRC_DIR=$2
# AMO script only download jetpack addons
KIND=jetpack

# echo "$FTP_DIR :: $SRC_DIR"
# exit;

mkdir -p $SRC_DIR && rm -fr $SRC_DIR/* # keep it clean

for XPI in $(ls -d $FTP_DIR/*.xpi)
do
  ID=$(basename $XPI)
  DST_DIR=$SRC_DIR/$ID
  mkdir -p $DST_DIR
  # echo "unzip $XPI -d $DST_DIR"
  unzip $XPI -d $DST_DIR
done
