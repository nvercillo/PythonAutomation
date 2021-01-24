from crontab import CronTab
import os

path = os.environ["absPath"]

cron = CronTab(user='stefan')
job = cron.new(command='python ' + path)
job.minute.every(1)

cron.write()