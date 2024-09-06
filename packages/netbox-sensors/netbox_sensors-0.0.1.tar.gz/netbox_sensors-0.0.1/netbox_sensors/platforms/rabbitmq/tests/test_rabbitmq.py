from vcr_unittest import VCRTestCase

from netbox_sensors.platforms.rabbitmq.rabbitmq import RabbitMQManagement
from netbox_sensors.platforms.rabbitmq.rabbitmq_cli import RabbitmqCli


class TestRabbitmq(VCRTestCase):
    def setUp(self):
        super().setUp()

    def test__init(self) -> None:
        actions = RabbitMQManagement(queue="s3dp.DATA")
        assert actions._queue == "s3dp.DATA"
        assert isinstance(actions._cli, RabbitmqCli)
        assert actions._cli.name == "rabbitmq"

    def test_create_user(self) -> None:
        actions = RabbitMQManagement(queue="s3dp.DATA")
        pass
