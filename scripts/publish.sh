#!/bin/bash

echo "Server needs to be running..."
if [ $# -ne 1 ]; then
    dir="../s3/storage/gdmrdigital/iiif-manifests-gdmr/ww1-tribunal"
else
    dir=$1
fi

wget -P $dir --no-host-directories --recursive http://localhost:9000/index.html
