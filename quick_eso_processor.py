from systems import odoo


def lambda_handler(event, context):
    message = "No orders to process"
    model = 'sale.order.external' 
    ids = odoo.search(model, [['state', '=', 'ready']])

    ready_order_count = len(ids)
    if ready_order_count >= 8:    
        ids = ids[:1]
        odoo.execute(model, 'sale_order_create', [ids])
        message = f"{ready_order_count} orders are ready to process"
    
    return {
        "statusCode": 200,
        "body": message,
    }
    