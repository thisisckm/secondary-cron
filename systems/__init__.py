import os
import sys
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from .odoo import Odoo

url = os.environ['CAM_URL']
db = os.environ['CAM_DB']
username = os.environ['CAM_USERNAME']
password = os.environ['CAM_PASSWORD']
wait_sec = os.environ.get('AMAZON_UPDATE_WAIT_SEC', '60')
wait_sec = int(wait_sec)
        
odoo = Odoo(url, db, username, password)

scheduler = BackgroundScheduler()


from logging.handlers import TimedRotatingFileHandler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        TimedRotatingFileHandler("logs/secondary-cron-uk-v1.log", when='midnight'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('Secondary Cron UK v1')