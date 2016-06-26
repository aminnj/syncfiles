#!/bin/bash

if [ $# -lt 1 ]; then
    echo "usage: $(basename $BASH_SOURCE) <folder name>"
    return 1
fi

dir=$1
outdir=$1

echo "$# args"
if [ $# -gt 1 ]; then 
    echo "Will put the stuff in $outdir instead"
    outdir=$2;
fi

for i in $(ls -1 $dir/*.pdf); do
    pdftopng $i &
    sleep 0.05
done

wait

index=$HOME/syncfiles/miscfiles/index.php

cp $index $dir/



# wait
chmod -R a+r $dir
mkdir -p ~/public_html/dump/$outdir/
if [[ $(hostname) == *uaf-* ]]; then 
    cp -rp $dir/* ~/public_html/dump/$outdir/
else
    ssh $USER@uaf-6.t2.ucsd.edu "mkdir -p ~/public_html/dump/$outdir; rm ~/public_html/dump/$outdir/*.png"
    scp -rp $dir/* $USER@uaf-6.t2.ucsd.edu:~/public_html/dump/$outdir/
fi
echo "uaf-6.t2.ucsd.edu/~$USER/dump/$outdir/"
