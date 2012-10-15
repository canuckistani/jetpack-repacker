=== REPACK INSTRUCTIONS ===

0/ Setup environnement and download these scripts
```
# We assume that we segregate all these repack files in '/addons' folder
$ mkdir /addons
$ cd /addons
$ git clone https://github.com/ochameau/jetpack-repacker repacker
  - or -
$ wget --no-check-certificate https://github.com/ochameau/jetpack-repacker/tarball/master -O - | tar xz
```

1/ Download xpi files
```
$ mkdir /addons/ftp
$ cd /addons/ftp
$ /addons/scripts/fetch-ftp.sh
# This script will download all xpi files. You can re-run it at anytime to download only new files.
# but note that remove files from mozilla ftp will be kept locally.
# xpi will be in /addons/ftp/ftp.mozilla.org/pub/mozilla.org/addons/
# (On 2012/07, it downloaded 17GB of files.)
```

2/ Unzip jetpack xpi files
```
$ /addons/repacker/scripts/unzip.sh /addons/ftp/ /addons/src
# This script will unzip all jetpack xpi files to /addons/src/jetpack folder
# (On 2012/07, it unpacked 770MB of data)
```

3/ Checkout all SDK released versions
```
$ mkdir /addons/sdks
$ /addons/sdks
$ /addons/repacker/scripts/clone_add_sdk_versions.sh
# It will take some time as it will checkout all tagged versions on git repo
```

4/ Compute repackability
```
$ cd /addons
$ python /addons/repacker/unpack.py --sdks /addons/sdks/ --batch repackability /addons/src/jetpack/ > repackability 2>&1
# This will process each addon source code and try to repack it against same SDK version
# and will tell for each addon, which one is safely repackable
```

5/ Compute addons list to repack
```
# remove diffs
$ cat repackability | grep -E "[0-9]+: " > t
# select only repackable and filter only path
$ cat info | grep repackable | grep -oE "^[^:]+" > to-repack
# /addons/to-repack now contains only path to repackable addons
```

4/ Repack selected addons
```
$ mkdir /addons/repacked
$ for i in `cat /addons/to-repack`; do python /addons/repacker/unpack.py repack $i --sdk /addons/sdks/1.8.2 --target /addons/repacked/ ;done
# Replace 1.8.2 with SDK version you want to repack to.
# repacked addons will be available in /addons/repacked/ folder
```

5/ Eventually compute dependencies and detailed info about each addon
```
for i in `cat /addons/to-repack`; do python /addons/repacker/unpack.py deps $i; done > /addons/repacked-info
```

