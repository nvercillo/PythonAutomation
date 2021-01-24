import subprocess
import os
import random


num = random.randint(1, 6)
subprocess.check_call(["./push.sh", str(num)])


