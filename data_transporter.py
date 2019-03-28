import pika
import config as cfg
import xmlrpc.client
import json

def callback(ch, method, properties, body):
    data_dict = json.loads(body)
    print(" [x] Received %r" % body)
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(cfg.ODOO_URL))
        uid = common.authenticate('postgres', 'odoo', 'odoo', {})
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(cfg.ODOO_URL))
            id = models.execute_kw('postgres', uid, 'odoo', 'res.partner', 'create', [data_dict])
            print(id)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=cfg.RABBIT_QUEUE)

    channel.basic_consume(
        cfg.RABBIT_QUEUE,
        callback,
        True
    )

    channel.start_consuming()
