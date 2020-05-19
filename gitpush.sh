FLOOR=10;
CEILING=21;
perl -e 'print int(rand(15) +12)'
for i in {1..5}
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