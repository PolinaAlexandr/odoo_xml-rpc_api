import pika
import config as cfg
import xmlrpc.client
import json

def callback(ch, method, properties, body):
    data_dict = json.loads(body)
    print(" [x] Received %r" % body)
    common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
    print(common.version())
    uid = common.authenticate('test_odoo', 'user@domain.com', 'odoo', {})

    # print('uid', uid)
    
    models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')
    id = models.execute_kw('test_odoo', uid, 'odoo', 'res.partner', 'create', [data_dict])
    print(id)


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=cfg.RABBIT_QUEUE)

    channel.basic_consume(callback,
                      queue=cfg.RABBIT_QUEUE,
                      no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
