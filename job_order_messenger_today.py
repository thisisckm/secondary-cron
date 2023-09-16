from systems import odoo
from datetime import datetime, timedelta

def lambda_handler(event, context):
    message = "No orders to process"
    model = 'job.order' 
 
    today_dt = datetime.now()
    next_dt = today_dt + timedelta(hours=23, minutes=59, seconds=55)
    job_ids_today = odoo.search(model, [['engineer_id','!=',False],['state','not in',('draft','cancel')],['appointment','<',str(next_dt)],['appointment','>',str(today_dt)]])
    
    order_count = len(job_ids_today)
    if job_ids_today:    
        odoo.execute(model, 'job_order_messages', [job_ids_today, 'day of nc'])
        message = f"{order_count} orders processed"
    
    return {
        "statusCode": 200,
        "body": message,
    }
    