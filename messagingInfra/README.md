docker-compose -f docker-compose.yml up

Check that the docker containers 'kafka' and 'zookepeer' are up and running using
docker ps

Creating Topics 
Start and iterative shell in the kafka container using:

docker exec -it kafka bin/sh 

in the iterative terminal,

change to the kafka installation directory
cd /opt/kafka

run the create topic .sh file with the parameters to create topic
./bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic topicname

Check that the topic was created successfully 

./bin/kafka-topics.sh --list --zookeeper zookeeper:2181