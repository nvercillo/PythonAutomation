FLOOR=10;
CEILING=100;
RANGE=$(($CEILING-$FLOOR+1));


STR=$(date)
echo '.................

Commit Time EST: ' $STR'

..................' > timesOfGitCommits.txt
cat timesOfGitCommits.txt >> temp_file.txt
git add .
git commit -m "$STR"
git push