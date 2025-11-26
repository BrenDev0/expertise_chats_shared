import pika
import threading
import os

class RabbitMqConnection:
    _connection = None
    _lock = threading.Lock()

    @classmethod
    def get_connection(cls):
        # Retrieve environment variables and raise ValueError if any are missing
        host = os.getenv("EXPERTISE_CHATS_BROKER_HOST")
        port = os.getenv("EXPERTISE_CHATS_BROKER_PORT")
        user = os.getenv("EXPERTISE_CHATS_BROKER_USER")
        password = os.getenv("EXPERTISE_CHATS_BROKER_PASSWORD")

        if not host:
            raise ValueError("Environment variable 'EXPERTISE_CHATS_BROKER_HOST' is not set.")
        if not port:
            raise ValueError("Environment variable 'EXPERTISE_CHATS_BROKER_PORT' is not set.")
        if not user:
            raise ValueError("Environment variable 'EXPERTISE_CHATS_BROKER_USER' is not set.")
        if not password:
            raise ValueError("Environment variable 'EXPERTISE_CHATS_BROKER_PASSWORD' is not set.")

        # Convert port to integer
        try:
            port = int(port)
        except ValueError:
            raise ValueError("'RABBITMQ_PORT' must be an integer.")

        credentials = pika.PlainCredentials(user, password)

        with cls._lock:
            params = pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host="/",
                heartbeat=60,
                credentials=credentials,
                blocked_connection_timeout=300,
            )

            cls._connection = pika.BlockingConnection(params)
            return cls._connection

    @classmethod
    def get_channel(cls):
        conn = cls.get_connection()
        return conn.channel()