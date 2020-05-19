FLOOR=10;
CEILING=100;
RANGE=$(($CEILING-$FLOOR+1));


stirng = date
echo '.................

Commit Time EST: 2323232/05/2020, 00:58:29

..................' > timesOfGitCommits.txt
cat timesOfGitCommits.txt >> temp_file.txt
git add .
git commit -m string
git push