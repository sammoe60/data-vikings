# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # The Data Vikings Producer

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mount

# COMMAND ----------

# ###### Mount Point through Oauth security.
# client_id = "5c0c63bf-b70d-461a-b3cb-fe0f9aeebe4a"
# client_secret = "TvR8Q~Fn4FAsZTFIZO.-umdb61Kd2mfQDQdZBaQW"
# tenant_id = "d4e104e3-ae7d-4371-a239-745aa8960cc9"

# storage_account = "cohort50storage"
# storage_container = "data-vikings"

# ## Name of the mount point
# mount_point = "/mnt/data-vikings"

# configs = {"fs.azure.account.auth.type": "OAuth",
#        "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
#        "fs.azure.account.oauth2.client.id": client_id,
#        "fs.azure.account.oauth2.client.secret": client_secret,
#        "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token",
#        "fs.azure.createRemoteFileSystemDuringInitialization": "true"}

# try: 
#     dbutils.fs.unmount(mount_point)
# except:
#     pass

# dbutils.fs.mount(
# source = f"abfss://{storage_container}@{storage_account}.dfs.core.windows.net/",
# mount_point = mount_point,
# extra_configs = configs)

# COMMAND ----------

display(dbutils.fs.ls("/mnt/data-vikings"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Include external configuration notebook

# COMMAND ----------

# MAGIC %run "./includes/configuration"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Data

# COMMAND ----------

state_poverty_df = spark.read.csv('/mnt/data-vikings/state_poverty.csv', header = True, inferSchema=True)

# COMMAND ----------

display(state_poverty_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Error Callback Functions

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


def acked(err, msg):
    """ 
        Error callback is used for generic issues for producer errors. 
        
        Parameters:
            err (err): Error flag.
            msg (str): Error message that was part of the callback.
    """
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Connection Strings and Imports

# COMMAND ----------

from confluent_kafka import Consumer
from time import sleep
import uuid
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
import json

# COMMAND ----------

# MAGIC %md
# MAGIC #### Create the topic

# COMMAND ----------

admin_client = AdminClient({
    'bootstrap.servers': confluentBootstrapServers,
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': confluentApiKey,
    'sasl.password': confluentSecret,
    'group.id': str(uuid.uuid1()),  # this will create a new consumer group on each invocation.
    'auto.offset.reset': 'earliest',
    'error_cb': error_cb,
})

# COMMAND ----------

topic_list = []

topic_list.append(NewTopic(confluentTopicName, 1))
futures = admin_client.create_topics(topic_list)

try:
    record_metadata = []
    for k, future in futures.items():
        # f = i.get(timeout=10)
        print(f"type(k): {type(k)}")
        print(f"type(v): {type(future)}")
        print(future.result())

except KafkaError:
    # Decide what to do if produce request failed...
    print(traceback.format_exc())
    result = 'Fail'


# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Producer

# COMMAND ----------

p = Producer({
    'bootstrap.servers': confluentBootstrapServers,
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': confluentApiKey,
    'sasl.password': confluentSecret,
    'auto.offset.reset': 'earliest',
    'error_cb': error_cb,
})

# COMMAND ----------

# MAGIC %md
# MAGIC ## DF --> JSON --> List

# COMMAND ----------

# returns RDD - resilient distributed dataset
rdd_json = state_poverty_df.toJSON()

# convert to a list
list_json = rdd_json.collect()



# COMMAND ----------

display(confluentTopicName)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Using JSON to feed the producer

# COMMAND ----------

for row in list_json:
    print(row)
    p.produce(confluentTopicName, row)
    p.flush
    sleep(2)
