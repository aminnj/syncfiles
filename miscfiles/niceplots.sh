#!/bin/bash

if [ $# -lt 1 ]; then
    echo "usage: $(basename $BASH_SOURCE) <folder name>"
    return 1
fi

dir=$1
for i in $(ls -1 $dir/*.pdf); do
    pdftopng $i &
    sleep 0.1
done

wait

index=$HOME/syncfiles/miscfiles/index.php

cp $index $dir/



# wait
chmod -R a+r $dir
mkdir -p ~/public_html/dump/
if [[ $(hostname) == *uaf-* ]]; then 
    cp -rp $dir ~/public_html/dump/
else
    scp -rp $dir namin@uaf-6.t2.ucsd.edu:~/public_html/dump/
fi
echo "uaf-6.t2.ucsd.edu/~$USER/dump/$dir/"
