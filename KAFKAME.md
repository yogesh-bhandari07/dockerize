# create a new topic 
docker exec -it <kafka_container_id> /bin/bash

# exec into kafka conatiner to create a topics 
kafka-topics --create --topic project1_logs --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# exec into kafka conatiner to see list of topics created 
kafka-topics --list --bootstrap-server localhost:9092

# exec into kafka conatiner to see logs of topic
docker exec <kafka-conatiner-id> kafka-console-consumer --topic <topic-name> --bootstrap-server localhost:9092 --from-beginning
docker exec kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic <topic-name> --from-beginning

