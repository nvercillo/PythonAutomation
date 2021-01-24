import subprocess
import os
import random


num = random.randint(1, 6)
print(num)
subprocess.check_call(["./push.sh", str(num)])


