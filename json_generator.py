import pika 
import json 
import time 
import random
import config as cfg

from config import generator_frequency



def generate_item():
    names = ['Sam', 'Robert', 'Lyn', 'Jack', 'Jonh', 'Lia', 'Margot', 'Flee', 'Victoria', 'Will']

    random_dict = {
        "id" : random.randint(1, 100)*10,
        "name" : random.choices(names),
        "age" : random.randint(0,75),
        "value" : random.randrange(18, 400, 3)           
    }

    return json.dumps(random_dict)


def send_json(item):
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=cfg.RABBIT_QUEUE)
    channel.basic_publish(exchange='',
                      routing_key=cfg.RABBIT_QUEUE,
                      body=item)
    print("[x] Sent json data to RabbitMQ", item)
    connection.close()


if __name__ == "__main__":
    while True:
        time.sleep(generator_frequency)
        item = generate_item()
        send_json(item)


