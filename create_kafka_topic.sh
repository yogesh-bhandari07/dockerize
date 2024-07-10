#!/bin/bash

# Check ZooKeeper readiness
echo "Waiting for ZooKeeper to be ready..."
while ! (echo ruok | nc -z zookeeper 2181 2>&1 | grep "imok" > /dev/null 2>&1); do
  echo "ZooKeeper is not ready yet..."
  sleep 10  # Increase wait time to 10 seconds
done

# Check Kafka readiness
echo "Waiting for Kafka to be ready..."
while ! kafka-broker-api-versions.sh --bootstrap-server kafka:9092 > /dev/null 2>&1; do
  echo "Kafka is not ready yet..."
  sleep 10  # Increase wait time to 10 seconds
done

# Create Kafka topic
echo "Creating Kafka topic..."
kafka-topics.sh --create --topic django_logs --bootstrap-server kafka:9092 --replication-factor 1 --partitions 1 || echo "Topic already exists"

# Execute the original entrypoint command
exec "$@"
