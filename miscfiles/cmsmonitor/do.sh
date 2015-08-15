#!/bin/bash

export SHELL=/bin/bash
export USER=namin
export LD_LIBRARY_PATH=/Users/namin/root/lib
export LIBPATH=/Users/namin/root/lib
export PATH=/Users/namin/root/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/TeX/texbin:/Users/namin/syncfiles/miscfiles/
export HOME=/Users/namin
export DYLD_LIBRARY_PATH=/Users/namin/root/lib
export PYTHONPATH=/Users/namin/root/lib:/Users/namin/syncfiles/pyfiles
export SHLIB_PATH=/Users/namin/root/lib

python /Users/namin/cron/monitor/monitor.py
scp monitor.json namin@uaf-6.t2.ucsd.edu:~/public_html/monitor.json
