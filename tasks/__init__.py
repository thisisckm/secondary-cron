import pandas as pd
import requests
import json
import os

from os import listdir, remove
from datetime import timezone
from systems import odoo, scheduler, logger

from apscheduler.triggers.cron import CronTrigger

SALES_CHANNEL_URL = os.environ.get("SALES_CHANNEL_URL")
class TeamsWebhookException(Exception):
    pass

def post_message(message: str) -> None:
    payload = {"text": message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(SALES_CHANNEL_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code != 200:
        raise TeamsWebhookException(response.reason)

def amazonupdate() -> None:
    
    logger.info("Amazon Upload process - Started") 
    model = 'sale.order.external'
    for data_file in listdir('data'):
        data = pd.read_csv("data/%s" % data_file, sep='\t')
        for i, row in data.iterrows():            
            ids = odoo.search(model, [['external_order_reference', '=', row['order-id']], ['state', '=', 'exception']])            
            if ids:
                logger.info(f"Order Ref {row['order-id']} of customer {row['buyer-name'].title()} found")
                odoo.write(model, ids,  {
                                            'external_customer_name': row['buyer-name'].title() if type(row['buyer-name']) != float else False,
                                            'external_customer_delivery_name': row['buyer-name'].title() if type(row['buyer-name']) != float else False,
                                            'external_customer_street1': row['ship-address-1'],
                                            'external_customer_street2': row['ship-address-2'] if type(row['ship-address-2']) != float else False,
                                            'external_customer_phone': str(row['buyer-phone-number']),
                                            'external_customer_email': row['buyer-email'],
                                            'external_customer_delivery_street1': row['ship-address-1'],
                                            'external_customer_delivery_street2': row['ship-address-2'] if type(row['ship-address-2']) != float else False,
                                            'external_customer_delivery_phone': str(row['buyer-phone-number']),
                                            'external_customer_delivery_email': row['buyer-email'],
                                            'state': 'received'
                                        })
                                        
            else:                
                ids = odoo.search(model, [['external_order_reference', '=', row['order-id']]])
                if not ids:
                    message = f"Order Ref {row['order-id']} of customer {row['buyer-name'].title()} not found"
                    logger.info(message)
                    post_message(message)
                else:
                    logger.info(f"Order Ref {row['order-id']} of customer {row['buyer-name'].title()} already processed")
        
        remove(f"data/{data_file}")

    logger.info("Amazon Upload process - End")

scheduler.add_job(amazonupdate, CronTrigger.from_crontab('*/2 * * * *', timezone=timezone.utc))


def quick_eso_process() -> None:    

    try:

        logger.info("Started")
        model = 'sale.order.external' 
        ids = odoo.search(model, [['state', '=', 'ready']])

        if len(ids) >= 8:    
            id = ids[0]
            logger.info(f'{id} Oder ID in progress')
            odoo.execute('sale.order.external', 'sale_order_create', [id])
            logger.info(f'{id} Oder ID completed')
        else:
            logger.info('Nothing to do')

    except Exception as ex:
        logger.error(ex)
    

scheduler.add_job(quick_eso_process, CronTrigger.from_crontab('*/1 * * * *', timezone=timezone.utc))

