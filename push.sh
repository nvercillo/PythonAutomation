#!/bin/bash

name=$1


if [[ -n "$name" ]]; then

    for i in $(seq "$1")
        do
            if [ $i -eq "6" ]
            then 
                rm -rf logs
                mkdir logs
            fi
            d=`date +%s`
            log_file="./logs/log_$d.txt"
            echo "This is an automated message" > $log_file
            git add -A
            git commit -m "Automated Commit at $d" 
            git push
        done
else
    echo "argument error"
fi