FLOOR=10;
CEILING=100;
RANGE=$(($CEILING-$FLOOR+1));

string1 = "................."

string2 = "Commit Time EST: "
string3 = date 
string4 = ".................." 
$string1$string2$string3$string4> timesOfGitCommits.txt
cat timesOfGitCommits.txt >> temp_file.txt
git add .
git commit -m "Automated commit"
git push