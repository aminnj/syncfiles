#!/bin/bash

job=$1
for i in {1..60} ; do
    echo "iteration $i"
    sleep 10m
    if [ $(condor_q $job | wc -l) -eq 5 ]; then 
        echo "found it"; 
    else
        echo "Did not find it" 
        echo "Job $job ended on $(date)" | mail -s "[UAFNotify] Job $job ended on $(date)" amin.nj@gmail.com
        break
    fi
done
