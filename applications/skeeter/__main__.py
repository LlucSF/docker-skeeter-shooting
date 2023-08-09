from confluent_kafka import Consumer
from confluent_kafka import Producer
import time
import socket
import os
import pandas as pd
from tabulate import tabulate

time.sleep(10)
################
c=Consumer({'bootstrap.servers':'kafka:9092','group.id':socket.gethostname(),'auto.offset.reset':'earliest'})
c.subscribe(['shoot'])
p=Producer({'bootstrap.servers':'kafka:9092','client.id': socket.gethostname()})
################

def main(c, p):
    game_cnt = 1
    while game_cnt != (int(os.environ['NUMBER_GAMES'])+1):
        print("\n*** Game "+str(game_cnt)+" ***")
        p.produce(topic='skeet', key="1", value="Skeet_"+str(game_cnt))
        p.poll(1)
        skeet_time = time.time()
        shoot_time = []
        shoot_id = []
        game_running = True


        while game_running:
            msg=c.poll(0) 

            if msg is None:
                continue
            
            if msg.error():
                print('Error: {}'.format(msg.error()))
                continue

            if msg.topic() == "shoot":
                shoot_time.append(time.time()-skeet_time)
                shoot_id.append(msg.value().decode('utf-8'))
                #print("Shoot from Shooter Id." + str(msg.value().decode('utf-8')) + " registered")
                if len(shoot_id) == int(os.environ['NUMBER_SHOOTERS']):
                    print("Game " + str(game_cnt) + " scores:")
                    for n in range(len(shoot_time)):
                        print("  - Shooter Id." +  
                            str(shoot_id[n]) + 
                            " time: " + 
                            str((shoot_time[n])))
                        
                    winner_id = shoot_time.index(min(shoot_time))
                    print(" The winner is Shooter Id." + str(shoot_id[winner_id]) + "!")

                    if game_cnt == 1:
                        id_df = pd.DataFrame(columns=['Shooter ID.', 'Total wins', 'Fastest shoot'])
                        id_df['Shooter ID.'] = shoot_id
                        for row in range(len(shoot_id)):
                            id_df['Total wins'][row] = 0
                            id_df['Fastest shoot'][row] = 999

                    id_df['Total wins'][id_df.index[id_df['Shooter ID.'] == shoot_id[winner_id]].tolist()] += 1
                    for n in range(len(shoot_id)):
                        row_id = id_df.index[id_df['Shooter ID.'] == shoot_id[n]].tolist()[0]
                        if id_df['Fastest shoot'][row_id] > shoot_time[n]:
                            id_df['Fastest shoot'][row_id] = shoot_time[n]
                        
                    game_cnt += 1
                    game_running = False
                else:
                    continue
    print( "\n +++++ Final results +++++ ")
    print(tabulate(id_df, headers = 'keys', tablefmt = 'psql'))
    print("")
    c.close()
    p.flush()

if __name__ == '__main__':
    time.sleep(5)
    main(c, p)
