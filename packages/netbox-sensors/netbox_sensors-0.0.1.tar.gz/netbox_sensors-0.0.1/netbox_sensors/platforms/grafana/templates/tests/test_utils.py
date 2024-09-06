from unittest import TestCase

from netbox_sensors.platforms.grafana.templates import db_base_1, ds_test
from netbox_sensors.platforms.grafana.templates.utils import (
    adapt_dashboard_with_datasources,
)


class TestUtils(TestCase):
    def setUp(self) -> None:
        pass

    def test_adapt_dashboard_with_datasources(self):
        """adapt dashboard with datasources."""
        result = adapt_dashboard_with_datasources(datasources=ds_test, dash=db_base_1)
        pass
