import json
import os
from typing import Any

import pika


class ThreatQueuePublisher:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.port = int(os.getenv("RABBITMQ_PORT", "5672"))
        self.user = os.getenv("RABBITMQ_USER", "tm_user")
        self.password = os.getenv("RABBITMQ_PASSWORD", "tm_pass")
        self.queue_name = os.getenv("THREAT_QUEUE_NAME", "threats.ingest")

    def publish(self, message: dict[str, Any]) -> None:
        credentials = pika.PlainCredentials(self.user, self.password)
        params = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        connection = pika.BlockingConnection(params)
        try:
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message).encode("utf-8"),
                properties=pika.BasicProperties(delivery_mode=2),
            )
        finally:
            connection.close()
