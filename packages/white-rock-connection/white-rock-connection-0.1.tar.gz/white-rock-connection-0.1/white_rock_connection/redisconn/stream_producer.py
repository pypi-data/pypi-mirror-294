import json
import os
import zlib
from time import sleep
import sys
import redis
from redis.exceptions import ConnectionError, TimeoutError

class RedisStreamProducer:
    def __init__(self, stream_name, yaml_path=None):
        """
        Inicializa o produtor do stream Redis.
        
        :param stream_name: Nome do stream Redis.
        :param yaml_path: Caminho opcional para o arquivo YAML de configuração. Se for None, usa variáveis de ambiente.
        """
        self.stream_name = stream_name
        self.yaml_path = yaml_path
        self.client = None
        self.__load_settings()
        self.__connect()

    def __load_settings(self):
        if self.yaml_path is None:
            self.host = os.getenv("REDIS_HOST", "localhost")
            self.port = int(os.getenv("REDIS_PORT", 6379))
            self.ssl = os.getenv("REDIS_SSL", "False").lower() == "true"
            self.db = int(os.getenv("REDIS_DB", 0))
            self.max_retries = int(os.getenv("REDIS_MAX_RETRIES", 5))
            self.retry_delay = int(os.getenv("REDIS_RETRY_DELAY", 5))
            self.password = os.getenv("REDIS_PASSWORD", None)
        else:

            with open(self.yaml_path, 'r') as f:
                settings = yaml.safe_load(f)
                # Normaliza todas as chaves para minúsculas
                settings = {key.lower(): value for key, value in settings.items()}
                
                self.host = settings.get('redis_host', 'localhost')
                self.port = settings.get('redis_port', 6379)
                self.ssl = settings.get('redis_ssl', False)
                self.db = settings.get('redis_db', 0)
                self.max_retries = settings.get('redis_max_retries', 5)
                self.retry_delay = settings.get('redis_retry_delay', 5)
                self.password = settings.get('redis_password', None)

    def __connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db, ssl=self.ssl, decode_responses=False, password=self.password)
                self.client.ping() # Try to send a ping to check the connection
                self.__clear_stream()
                print("Connected to Redis")
                break
            except (ConnectionError, TimeoutError) as e:
                print(f"Connection to Redis failed: {e}. Retrying in {self.retry_delay} seconds...")
                retries += 1
                sleep(self.retry_delay)
        if retries == self.max_retries:
            print("Max retries reached. Could not connect to Redis.")
            raise Exception("Max retries reached. Could not connect to Redis.")

    def __clear_stream(self):
        try:
            # Obter todas as IDs das entradas no stream
            stream_entries = self.client.xrange(self.stream_name, min='-', max='+')
            entry_ids = [entry[0] for entry in stream_entries]

            if entry_ids:
                # Usar XDEL para remover todas as entradas no stream
                self.client.xdel(self.stream_name, *entry_ids)

            # Verificar o tamanho do stream após a limpeza
            stream_length = self.client.xlen(self.stream_name)

            print(f"Todas as mensagens do stream '{self.stream_name}' foram excluídas com sucesso.")
            print(f"O tamanho do stream agora é: {stream_length}")
        except Exception as e:
            print(f"Ocorreu um erro ao limpar o stream '{self.stream_name}': {e}")

    def encode_none(self, value):
        if value is None:
            value = 'None'
        return value

    def publish(self, message: dict):
        try:
            encoded_message = json.dumps(message,  separators=(',', ':'))
            byte_message = {b"message": zlib.compress(encoded_message.encode('utf8'))}
            self.client.xadd(self.stream_name, byte_message)
        except (ConnectionError, TimeoutError) as e:
            print(f"Connection lost while publishing message: {e}. Reconnecting...")
            self.__connect()
            self.publish(message)
