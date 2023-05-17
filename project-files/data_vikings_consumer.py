# Databricks notebook source
# MAGIC %md
# MAGIC # The Data Vikings Consumer

# COMMAND ----------

# MAGIC %md
# MAGIC #### Include external configuration notebook

# COMMAND ----------

# MAGIC %run "./includes/configuration"

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### Error Callback Functions

# COMMAND ----------

def error_cb(err):
    """ The error callback is used for generic client errors. These
        errors are generally to be considered informational as the client will
        automatically try to recover from all errors, and no extra action
        is typically required by the application.
        For this example however, we terminate the application if the client
        is unable to connect to any broker (_ALL_BROKERS_DOWN) and on
        authentication errors (_AUTHENTICATION). """

    print("Client error: {}".format(err))
    if err.code() == KafkaError._ALL_BROKERS_DOWN or \
       err.code() == KafkaError._AUTHENTICATION:
        # Any exception raised from this callback will be re-raised from the
        # triggering flush() or poll() call.
        raise KafkaException(err)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Setting up Consumer

# COMMAND ----------

from confluent_kafka import Consumer
from time import sleep
import uuid
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException, TopicPartition
import json

#Kakfa Class Setup.
c = Consumer({
    'bootstrap.servers': confluentBootstrapServers,
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': confluentApiKey,
    'sasl.password': confluentSecret,
    'group.id': topic_group_id,
    'auto.offset.reset': 'earliest',
    'error_cb': error_cb,
    'batch.num.messages': 250
})
# may try commenting out
# topic_part = TopicPartition(confluentTopicName, 0)
# c.assign([topic_part])

c.subscribe([confluentTopicName])

# COMMAND ----------

# MAGIC %md
# MAGIC #### Consume the messages

# COMMAND ----------

aJson = {}

kafkaListDictionaries = []

while(True):
    try:
        msg = c.poll(timeout=1.0)
        if msg is None:
            break
        elif msg.error():
            print("Consumer error: {}".format(msg.error()))
            break
        else:
            aJson = json.loads('{}'.format(msg.value().decode('utf-8')))
            aJson['msg_timestamp'] = msg.timestamp()[1]
            display(aJson)
            kafkaListDictionaries.append(aJson)
    except Exception as e:
        print(e)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Stop if there are no messages

# COMMAND ----------

if len(kafkaListDictionaries) == 0: dbutils.notebook.exit("There are no messages to process")

# COMMAND ----------

display(kafkaListDictionaries)

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Convert Dict --> DF

# COMMAND ----------

consumer_df = spark.createDataFrame(kafkaListDictionaries)
display(consumer_df)

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Write DF to CSV

# COMMAND ----------

consumer_df.write.option("header",True).csv('/mnt/data-vikings/national_poverty_output_kafka.csv')
