import subprocess
import os
import random


num = random.randint(1, 6)
f = open("demofile2.txt", "a")
f.write("Now the file has more content!")
f.close()
print(num)
subprocess.check_call(["./push.sh", str(num)])


