echo '.................

Commit Time EST: 05/05/2020, 00:58:29

..................' > temp_file.txt
cat timesOfGitCommits.txt >> temp_file.txt
git add .
git commit -m "Automated commit"
git push