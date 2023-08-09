from confluent_kafka import Consumer
from confluent_kafka import Producer
import socket
import time
import os 

time.sleep(10)
################
c=Consumer({'bootstrap.servers':'kafka:9092','group.id':socket.gethostname(),'auto.offset.reset':'earliest'})
c.subscribe(['skeet'])
p=Producer({'bootstrap.servers':'kafka:9092','client.id': socket.gethostname()})
################

def main(c, p):
    game_cnt = 1
    #nap_time = 0
    while  game_cnt != (int(os.environ['NUMBER_GAMES'])+1):
        #nap_time = random.randint(10,500)/1000
        #print("Sleeping for " + str(nap_time) + " ms" )
        #time.sleep(nap_time)

        msg=c.poll(0) #timeout

        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue

        if msg.topic() == 'skeet':
            print("Shoot!")
            p.produce(topic='shoot', value=str(socket.gethostname()))
            p.poll(1)
            game_cnt += 1
    c.close()
    p.flush()

if __name__ == '__main__':
    time.sleep(5)
    main(c, p)
