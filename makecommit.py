import os
import sys 
from datetime import datetime


f = open("timesOfGitCommits.txt", "a+")
s = []

s.append("Commit Time EST: ")
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
s.append(date_time)
s.append("\r\n") 
s = "".join(s)
f.write('..................\r\n')
f.write(s)
f.write('..................\r\n')
f.close()
os.system('cmd /k "git add * & git commit -m std_commit_message"')