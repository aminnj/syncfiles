#!/bin/bash

if [ $# -lt 1 ]; then
    echo "usage: $(basename $BASH_SOURCE) <folder name>"
    return 1
fi

dir=$1
outdir=$1

if [ $# -gt 1 ]; then 
    echo "Will put the stuff in $outdir instead"
    outdir=$2;
fi


function pdftopng {
    #sharpen not really necessary
    #convert -density 250 -trim $1 -quality 100 -sharpen 0x1.0 ${1%%.pdf}.png
    if [ $# -gt 0 ]; then
        density=125
        if [ $# -gt 1 ]; then
            density=$2
        fi
        echo "$1 ==> ${1%%.pdf}.png" 
        if [[ $HOST == *uaf-* ]]; then 
            gs -q -sDEVICE=pngalpha -o ${1%%.pdf}.png -sDEVICE=pngalpha -dUseCropBox -r${density} $1
        else
            convert -density ${density} -trim $1 -fuzz 1% ${1%%.pdf}.png
        fi
    else
        echo "Usage: pdftopng <pdf name> [optional density]"
    fi
}
export -f pdftopng

# ls -1 ${dir}/*.pdf | xargs -I%  -n 1 -P 20 sh -c "pdftopng % 75;"
# ls -1 ${dir}/*/*.pdf | xargs -I%  -n 1 -P 20 sh -c "pdftopng % 75;"
ls -1 ${dir}/*.pdf | xargs -I%  -n 1 -P 20 sh -c "pdftopng % 125;"
ls -1 ${dir}/*/*.pdf | xargs -I%  -n 1 -P 20 sh -c "pdftopng % 125;"

# for i in $(ls -1 $dir/*.pdf); do
#     pdftopng $i &
#     sleep 0.2
# done
# wait

index=$HOME/syncfiles/miscfiles/index.php

ln -s $index $dir/index.php



# wait
chmod -R a+r $dir
mkdir -p ~/public_html/dump/$outdir/
if [[ $(hostname) == *uaf-* ]] || [[ "$NOINTERNET" == "true" ]]; then
    cp -rp $dir/* ~/public_html/dump/$outdir/
else
    ssh $USER@uaf-10.t2.ucsd.edu "mkdir -p ~/public_html/dump/$outdir; rm ~/public_html/dump/$outdir/*.png"
    scp -rp $dir/* $USER@uaf-10.t2.ucsd.edu:~/public_html/dump/$outdir/
fi
echo "${HOSTNAME}/~$USER/dump/$outdir/"
