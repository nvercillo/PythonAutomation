#!/bin/sh
perl randnum.pl
typeset -i randNum=$(cat rand.txt)
echo $randNum
for i in  $(seq 1 $randNum);
do
STR=$(date)
echo '.................

Commit Time EST: ' $STR '

..................' > timesOfGitCommits.txt
cat timesOfGitCommits.txt >> temp_file.txt
git add .
git commit -m "$STR"
git push
done