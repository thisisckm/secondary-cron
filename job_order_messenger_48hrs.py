from systems import odoo
from datetime import datetime, timedelta

def lambda_handler(event, context):
    message = "No orders to process"
    model = 'job.order'

    date_48_dt = datetime.now() + timedelta(hours=47)
    date_48_dt_next = date_48_dt + timedelta(hours=1)
    job_ids_48 = odoo.search(model, [('engineer_id','!=',False),('state','not in',('draft','cancel')),('appointment','<',str(date_48_dt_next)),('appointment','>=',str(date_48_dt))])

    order_count = len(job_ids_48)
    if job_ids_48:    
        odoo.execute(model, 'job_order_messages', [job_ids_48, '48hrs before job'])
        message = f"{order_count} orders processed"
    
    return {
        "statusCode": 200,
        "body": message,
    }
    