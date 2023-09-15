from systems import odoo


def lambda_handler(event, context):
    model = 'job.order' 
    
    odoo.execute(model, 'joborder_message_scheduler', [])
    
    return {
        "statusCode": 200,
        "body": "Successfully Executed",
    }
    