import requests
import boto3
import pandas as pd

from os import listdir, remove
from botocore.exceptions import ClientError
from datetime import datetime, timezone, timedelta
from systems import odoo, scheduler, logger

from apscheduler.triggers.cron import CronTrigger


def amazonupdate():
    
    logger.info("Amazon Upload process - Started") 
    model = 'sale.order.external'
    for data_file in listdir('data'):
        data = pd.read_csv("data/%s" % data_file, sep='\t')
        flag_to_delete = True
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
                    logger.info(f"Order Ref {row['order-id']} of customer {row['buyer-name'].title()} not found")
                    flag_to_delete = False
                else:
                    logger.info(f"Order Ref {row['order-id']} of customer {row['buyer-name'].title()} already processed")
        if flag_to_delete:            
            remove(f"data/{data_file}")

    logger.info("Amazon Upload process - End")

scheduler.add_job(amazonupdate, CronTrigger.from_crontab('*/2 * * * *', timezone=timezone.utc))


def quick_eso_process():    
    try:
        logger.info("Started")
        model = 'sale.order.external' 
        ids = odoo.search(model, [['state', '=', 'ready']])
        if not len(ids) > 8:
            logger.info('Nothing to do')
            return
            
        id = ids[0]
        logger.info(f'{id} Oder ID in progress')
        odoo.execute('sale.order.external', 'sale_order_create', [id])
        logger.info(f'{id} Oder ID completed')
    except Exception as ex:
        logger.error(ex)
    

scheduler.add_job(quick_eso_process, CronTrigger.from_crontab('*/1 * * * *', timezone=timezone.utc))

class CheckForapi:

    def __init__(self):
        self.last_know_working = datetime.now()

        self.AWS_ACCESS_KEY_ID = 'AKIA4ACDYH6Z7VCWAVVI'
        self.AWS_SECRET_ACCESS_KEY = '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'
        
        self.ec2_client = boto3.client('ec2', region_name='eu-west-2',
                        aws_access_key_id=self.AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)
        self.channel_url = "https://chameleoncodewing.webhook.office.com/webhookb2/10fd593d-50f1-4d3e-b909-847022ac3ac3@053ba6b3-b09f-4314-94c7-c694e5f68b64/IncomingWebhook/661935be6daa4bdd80503b9ed3d93f04/0357ad5e-075f-40a4-938a-4cc7587d341f"

    def start_ec2(self, instance_ids):
        try:
            self.ec2_client.start_instances(InstanceIds=instance_ids, DryRun=False)
            return {'statusCode': 200, 'body': 'Instances %s started' % instance_ids}
        except ClientError as e:
            return {'statusCode': 400, 'body': 'Instances %s not able to started' % instance_ids}


    def reboot_ec2(self, instance_ids):
        try:
            self.ec2_client.reboot_instances(InstanceIds=instance_ids, DryRun=False)
            return {'statusCode': 200, 'body': 'Instances %s rebooted' % instance_ids}
        except ClientError as e:
            return {'statusCode': 400, 'body': 'Instances %s not able to reboot' % instance_ids}

    def stop_ec2(self, instance_ids):
        try:
            self.ec2_client.stop_instances(InstanceIds=instance_ids, DryRun=False)
            return {'statusCode': 200, 'body': 'Instances %s stopped' % instance_ids}
        except ClientError as e:
            return {'statusCode': 400, 'body': 'Instances %s not able to stop' % instance_ids}

    def is_ec3_running(self, instance_ids):
        response = self.ec2_client.describe_instance_status(InstanceIds=instance_ids, IncludeAllInstances=True)
        return response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'
        
    def channel_post(self, message):
        requests.post(self.channel_url, 
                json={"text": message})

    def check_forapi(self):
        response = requests.get("https://backend.chameleonerp.net")
        if response.status_code == 200:
            self.last_know_working = datetime.now()
        else:
            if datetime.now() > (self.last_know_working + timedelta(minutes=5)):
                logger.info('ForApi is not working')
                message = f"forapi Server is down for more than {datetime.now() -  self.last_know_working}. Trying to restart."
                
                self.channel_post(message)

                instance_ids = ["i-0096883bae6e6f0af"]
                if self.is_ec3_running(instance_ids):
                    result = self.reboot_ec2(instance_ids)
                else:
                    result = self.start_ec2(instance_ids)

                if result['statusCode'] == 400:
                    logger.error(result['body'])
                    self.channel_post("Restart failed. Will retry in a minute.")
                else:
                    self.last_know_working = datetime.now()
                    logger.info(result['body'])
                    self.channel_post("forapi Server restarted successfuly.")


check_forapi = CheckForapi()
scheduler.add_job(check_forapi.check_forapi, CronTrigger.from_crontab('*/1 * * * *', timezone=timezone.utc))
