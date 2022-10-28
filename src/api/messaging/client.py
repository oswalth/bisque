import json

import pika


class MessagingClient:
    def __init__(
        self,
        exchange_name: str,
        mq_user: str,
        mq_password: str,
        mq_host: str = "0.0.0.0",
        mq_port: int = 5672,
    ):
        self.exchange_name = exchange_name
        self.mq_user = mq_user
        self.mq_password = mq_password
        self.mq_host = mq_host
        self.mq_port = mq_port

    def __enter__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.mq_host,
            port=self.mq_port,
            credentials=pika.PlainCredentials(username=self.mq_user, password=self.mq_password)
        )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def send_flat_message(self, flat_id: int, type_: str):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key="",
            body=json.dumps({"flat_id": flat_id, "type_": type_}).encode()
        )


# mq = MessagingClient(exchange_name="bisque", mq_user="oswalth", mq_password="2525")
# a = 1
# with mq as client:
#     client.send_flat_message(123, "new")
#     client.send_flat_message(123, "update")
#     client.send_flat_message(321, "new")
#     client.send_flat_message(321, "delete")
#     client.send_flat_message(123, "update")
#
