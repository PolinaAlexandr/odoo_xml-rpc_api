import pika 
import json 
import time 
import random
from config import generator_frequency

# def send_json():
#     connection = pika.BaseConnection(pika.ConnectionParameters('localhost'))
#     channel =  connection.channel()

#     channel.queue_declare(queue='new')
#     channel.basic_publish(exchange='', routing_key='new', body='New task!')
#     connection.close()
    
def generate_item():
    names = ['Sam', 'Lyn', 'Jack', 'Jonh', 'Lia', 'Margot', 'Flee', 'Victoria', 'Will']

    random_dict = {
        "id" : random.randint(1, 100)*10,
        "name" : random.choices(names),
        "age" : random.randint(0,75),
        "value" : random.randrange(18, 400, 3)           
    }

    return json.dumps(random_dict)


if __name__ == "__main__":
    while True:
        time.sleep(generator_frequency)

        random_json = generate_item()
        print(random_json)


