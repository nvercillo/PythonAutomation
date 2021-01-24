#!/bin/bash

name=$1
d=`date +%s`
log_file="./logs/log_$d.txt"

if [[ -n "$name" ]]; then
    for i in $(seq "$1")
        do
            echo "This is an automated message" > $log_file
            git -A 
            git commit -m "Automated Commit at $d" 
            git push
        done
else
    echo "argument error"
fi