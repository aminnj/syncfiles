#!/bin/bash

index=${1}/_index.php

echo "<html>" > $index
echo "<body>" >> $index
echo "<center><br>" >> $index

for pic in $1/*.pdf; do
    echo $pic; convert -density 100 -trim ${pic} ${pic%%.pdf}.png;
    basepic=$(basename $pic)
    echo "<a href='${basepic}'><img src='${basepic%%.pdf}.png' /></a>" >> $index
done

echo "<center>" >> $index
echo "<body>" >> $index
echo "<html>" >> $index


chmod -R a+r $1
scp -rp $1 namin@web.physics.ucsb.edu:~/public_html/dump/
echo "web.physics.ucsb.edu/~namin/dump/${index}"
