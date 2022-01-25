import json
from kafka import KafkaConsumer, KafkaProducer
from classes.utils.consumer import Consumer
import classes.utils.vars as v

consumer = KafkaConsumer(group_id="FRAUD_DETECTOR", 
    bootstrap_servers=[f"{v.kafka_endpoint}:19092", f"{v.kafka_endpoint}:29092", f"{v.kafka_endpoint}:39092"], 
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
    )

producer = KafkaProducer(bootstrap_servers=[f"{v.kafka_endpoint}:19092", f"{v.kafka_endpoint}:29092", f"{v.kafka_endpoint}:39092"], 
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

consumer.subscribe("NEW_ORDER")

for msg in consumer:
    order = Consumer.order(msg.value)

    producer.send("ORDER_CONFIRMATION", order).get()

    print(order)
