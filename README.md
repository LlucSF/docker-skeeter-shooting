# Skeeter Shooting between Docker Containers

Simple python project to learn how to set up containers using docker-compose and stablish a kafka network between services using confluent-kafka.
The project emulates skeeter shooting, where the service skeeter sends a messages in the topic 'skeet' and waits for messages in the topic 'shoot' from all the shooter services. Then it times the response of all shooters and the fastest between them is the winner of the round. By default 100 rounds will be played by 7 shooters. You can add more shooters or more game rounds by modifying the 'docker-compose.yml' file and tuning the 'variables.env' file accordingly. To run the game just execute the 'run.sh' script. 

At the end the game shows a resume of all the rounds by attaching to the skeeter log:

<pre>
  +++++ Final results +++++  
 +----+---------------+--------------+-----------------+ 
 |    | Shooter ID.   |   Total wins |   Fastest shoot |  
 |----+---------------+--------------+-----------------| 
 |  0 | 59f7fb102b6f  |            8 |       0.0142684 | 
 |  1 | e6a9e7a04a36  |           30 |       0.01263   | 
 |  2 | 8f65f793dc9d  |           22 |       0.0133035 |  
 |  3 | c048859f9e4f  |           18 |       0.0135169 | 
 |  4 | cdaa4d4cdadf  |           12 |       0.0132418 | 
 |  5 | 1d412df5e79a  |            3 |       0.0134087 | 
 |  6 | 76033b763350  |            7 |       0.0135131 | 
 +----+---------------+--------------+-----------------+ 
 </pre>


