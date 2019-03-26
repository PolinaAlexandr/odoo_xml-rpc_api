import pika
import config as cfg

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=cfg.RABBIT_QUEUE)

    channel.basic_consume(callback,
                      queue=cfg.RABBIT_QUEUE,
                      no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
