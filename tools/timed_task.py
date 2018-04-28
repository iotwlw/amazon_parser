
from apscheduler.schedulers.background import BackgroundScheduler
import os
import datetime
import product_detail_mysql

import logging
logging.basicConfig()

schedular = BackgroundScheduler()


@schedular.scheduled_job('cron', hour='0,2,4,6,8,9', minute=32, second=45)
def timed_job():
    print ("{}------------SHUIKU Search Engines--------RUN----------------".format(datetime.datetime.now()))
    product_detail_mysql.product_detail_to_mysql()


@schedular.scheduled_job('cron', hour='0,2,4,6,8,9', minute=40, second=45)
def timed_job():
    print ("{}------------SHUIKU UK Search Engines--------RUN----------------".format(datetime.datetime.now()))
    product_detail_mysql.product_detail_to_mysql("UK")

schedular.start()
os.system('pause')
