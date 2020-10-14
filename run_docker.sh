#!/bin/bash
sudo docker run \
--runtime=nvidia \
--name illustrator \
-p 8891:8888 \
-it \
-v $(pwd):/workdir \
-w /workdir \
m-shiga/illustrator \
"$@"
