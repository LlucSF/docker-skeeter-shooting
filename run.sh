#! /bin/bash
cd "${0%/*}"

# Creating the containers with all the services and waiting for them to be running
docker-compose down --remove-orphans
docker-compose up -d --build
printf 'Waiting a bit for Kafka...\n'
sleep 5s

# Adding topics
printf '\nCreating new topics:\n'
docker exec kafka kafka-topics --create --topic skeet --bootstrap-server localhost:9092
docker exec kafka kafka-topics --create --topic shoot --bootstrap-server localhost:9092

# Attatch to skeeter
docker-compose logs -f skeeter 
