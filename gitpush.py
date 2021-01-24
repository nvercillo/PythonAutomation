import subprocess
import os
import random


num = random.randint(1, 6)
print(num)
subprocess.check_call(["/home/ubuntu/PythonAutomation/push.sh", str(num)])


