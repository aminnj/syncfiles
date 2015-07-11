#!/bin/bash

if [ $# -lt 1 ]; then
    echo "usage: $(basename $BASH_SOURCE) <folder name>"
    return 1
fi

dir=$1
for i in $(ls -1 $dir/*.pdf); do
    pdftopng $i &
done

wait

index=$dir/_index.php
details=$dir/details.txt
echo $details

echo "<html>" > $index
echo "<body>" >> $index
echo "<center><br>" >> $index

echo "<p align='center' style='font:12pt sans-serif'>Created on $(date) from $(pwd)/$dir" >> $index

for pic in $dir/*.png; do
    echo $pic
    basepic=$(basename $pic)
    echo "<div style='position:relative;z-index:1;display:inline;padding-left:0px;padding-right:0px'>" >> $index
    echo "<a href='${basepic%%.png}.pdf'><img src='${basepic}' width='600px'/></a>" >> $index

    # if we have details file, cat and grep for detail
    if [ -f $details ]; then
        echo "<div style='position:absolute;z-index:2;right:170px;bottom:340px;width:250px;'>" >> $index
        echo $(cat $details | grep ${basepic%%.png}.pdf | cut -d ':' -f2) >> $index
        echo "</div>" >> $index
    fi

    echo "</div>" >> $index
    echo "" >> $index
done

echo "<center>" >> $index
echo "<body>" >> $index
echo "<html>" >> $index

# wait
chmod -R a+r $dir
mkdir -p ~/public_html/dump/
cp -rp $dir ~/public_html/dump/
echo "uaf-6.t2.ucsd.edu/~$USER/dump/$index"
