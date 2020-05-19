git add .

echo 'Enter the commit message:'
read commitMessage

git commit -m "$commitMessage"

echo 'Your git pushing the current branch, make sure its not master'
# read branch
# git push origin $branch
git push

read
