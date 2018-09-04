
from apscheduler.schedulers.background import BackgroundScheduler
import os
import datetime
import product_detail_mysql

import logging
logging.basicConfig()

schedular = BackgroundScheduler()


@schedular.scheduled_job('cron', hour='22,23,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21', minute=16, second=55)
def timed_job():
    print ("{}------------SHUIKU Search Engines--------RUN----------------".format(datetime.datetime.now()))
    product_detail_mysql.product_detail_to_mysql()


@schedular.scheduled_job('cron', hour='22,23,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21', minute=40, second=36)
def timed_job():
    print ("{}------------SHUIKU UK Search Engines--------RUN----------------".format(datetime.datetime.now()))
    product_detail_mysql.product_detail_to_mysql("UK")

schedular.start()
os.system('pause')
# product_detail_mysql.product_detail_to_mysql()
