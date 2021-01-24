#!/bin/bash

name=$1
d=`date +%s`
log_file="./logs/log_$d.txt"

if [[ -n "$name" ]]; then

    for i in $(seq "$1")
        do
            if [ $i -eq "6" ]
            then 
                rm -rf logs
                mkdir logs
            fi
            echo "This is an automated message" > $log_file
            git add $log_file
            git commit -m "Automated Commit at $d" 
            git push
        done
else
    echo "argument error"
fi