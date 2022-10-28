from dependency_injector import containers, providers

from api.messaging.client import MessagingClient


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    messaging_client = providers.Factory(
        MessagingClient,
        exchange_name=config.MQ_EXCHANGE_NAME,
        mq_user=config.MQ_USER,
        mq_password=config.MQ_PASSWORD,
        mq_host=config.MQ_HOST,
        mq_port=config.MQ_PORT,
    )
