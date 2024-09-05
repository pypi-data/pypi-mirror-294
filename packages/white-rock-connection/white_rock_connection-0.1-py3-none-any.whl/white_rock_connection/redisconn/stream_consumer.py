import json
import threading
import zlib
from time import sleep

import redis
from redis.exceptions import ConnectionError, TimeoutError
from abc import ABC, abstractmethod


class RedisStreamConsumer(ABC):

    def __init__(self, queue_name, topic_name, clear_on_start=True, env_file_path=None):
        """
        Initializes the Redis stream consumer.
        
        :param queue_name: Name of the Redis queue.
        :param topic_name: Name of the Redis topic.
        :param clear_on_start: Defines whether to clear the queue on start.
        :param env_file_path: Optional path to a YAML configuration file. If None, environment variables are used.
        """
        self.topic_name = topic_name
        self.queue_name = queue_name
        self.__clear_on_start = clear_on_start
        self.counter = 0
        self.env_file_path = env_file_path
        self.__load_settings()
        self.__connect()
        self.create_group()
        self.consuming = True

    def __load_settings(self):
        if self.env_file_path is None:
            # If no YAML file is provided, use environment variables
            self.host = os.getenv("REDIS_HOST", "localhost")
            self.port = int(os.getenv("REDIS_PORT", 6379))
            self.db = int(os.getenv("REDIS_DB", 0))
            self.max_retries = int(os.getenv("REDIS_MAX_RETRIES", 5))
            self.retry_delay = int(os.getenv("REDIS_RETRY_DELAY", 5))
            self.ssl = os.getenv("REDIS_SSL", "False").lower() == "true"
            self.password = os.getenv("REDIS_PASSWORD", None)
        else:
            # If YAML file is provided, load settings from the file
            with open(self.env_file_path, 'r') as f:
                settings = yaml.safe_load(f)
                # Normalize all keys to lowercase
                settings = {key.lower(): value for key, value in settings.items()}
                
                self.host = settings.get('redis_host', 'localhost')
                self.port = settings.get('redis_port', 6379)
                self.db = settings.get('redis_db', 0)
                self.max_retries = settings.get('redis_max_retries', 5)
                self.retry_delay = settings.get('redis_retry_delay', 5)
                self.ssl = settings.get('redis_ssl', False)
                self.password = settings.get('redis_password', None)

    def start_async(self):
        print("Starting redis  ++++++++++++++++")
        threading.Thread(target=self.__start_consuming).start()

    def start(self):
        self.__start_consuming()

    @abstractmethod
    def receive_message(self, body, message_id):
        pass


    def __connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db, ssl=self.ssl,
                                                decode_responses=False, password=self.password)
                self.client.ping()  # Try to send a ping to check the connection
                print("Connected to Redis")
                break
            except (ConnectionError, TimeoutError) as e:
                print(f"Connection to Redis failed: {e}. Retrying in {self.retry_delay} seconds...")
                retries += 1
                sleep(self.retry_delay)
        if retries == self.max_retries:
            print("Max retries reached. Could not connect to Redis.")
            raise Exception("Max retries reached. Could not connect to Redis.")

    def create_group(self):
        try:
            if self.__clear_on_start:
                self.__clear_queue()
            self.client.xgroup_create(name=self.topic_name, groupname=self.queue_name, id='$', mkstream=True)
            print(f"Group {self.queue_name} created for stream {self.topic_name}")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP Consumer Group name already exists" in str(e):
                print(f"Group {self.queue_name} already exists")
            else:
                print(f"Error creating group {self.queue_name} for stream {self.topic_name}: {e}")

    def __clear_queue(self):
        try:
            # Fetch pending messages information for the consumer group
            self.client.xgroup_destroy(self.topic_name, self.queue_name)
        except Exception as e:
            print(f"Error clearing pending messages: {e}")

    def __start_consuming(self):
        while self.consuming:
            try:
                messages = self.client.xreadgroup(groupname=self.queue_name, consumername=self.queue_name,
                                                  streams={self.topic_name: ">"}, count=30, block=5000)
                if messages:
                    for message in messages:
                        for msg_id, msg in message[1]:
                            self.process_message(msg, msg_id)
            except (ConnectionError, TimeoutError) as e:
                print(f"Connection lost while consuming messages: {e}. Reconnecting...")
                self.__connect()
            except Exception as e:
                print(f"Error consuming messages: {e}")

    def stop(self):
        print("Stopping consumer")
        self.consuming = False
        self.client.close()

    def decode_none(self, value):
        if value == 'None':
            value = None
        return value

    def decode_message(self, compressed_message: bytes) -> dict:
        decompressed_message = zlib.decompress(compressed_message)
        decoded_message = decompressed_message.decode('utf-8')
        return json.loads(decoded_message)

    def process_message(self, message, msg_id):
        try:
            self.counter += 1
            # print(f"Processing message {self.counter} on topic {self.topic_name} with ID {msg_id.decode()}", end='\r')
            # Process the message here
            decoded_message = self.decode_message(message.get(b"message"))
            self.receive_message(decoded_message, msg_id)
            self.client.xack(self.topic_name, self.queue_name, msg_id)
        except (ConnectionError, TimeoutError) as e:
            print(f"Connection lost while processing message ID {msg_id}: {e}. Reconnecting...")
            self.__connect()
        except Exception as e:
            print(
                f"Error processing message ID {msg_id}: {e} \n Error processing message ID {msg_id}: {e} \n Error processing message ID {msg_id}: {e}")

    def replace_none_with_placeholder(self, message):
        return {k: (None if v == 'None' else v) for k, v in message.items()}
