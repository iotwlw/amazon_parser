
from apscheduler.schedulers.background import BackgroundScheduler
import os
import datetime
import product_detail_mysql

import logging
logging.basicConfig()

schedular = BackgroundScheduler()


@schedular.scheduled_job('cron', hour='0-10', minute=2, second=11)
def timed_job():
    print ("{}------------SHUIKU Search Engines--------RUN----------------".format(datetime.datetime.now()))
    product_detail_mysql.to_mysql()

schedular.start()
os.system('pause')
