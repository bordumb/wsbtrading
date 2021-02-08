import unittest
from unittest.mock import Mock, patch

import pytest

from wsbtrading.data_io import data_io


class TestAlpacaApiConnection(unittest.TestCase):
    @patch.object(data_io, 'alpaca_rest_api_conn')
    def test_alpaca_api_connection(self, AlpacaApiConnMock: Mock):
        alpaca_api_conn_mock = Mock()
        AlpacaApiConnMock.return_value = alpaca_api_conn_mock

        data_io.alpaca_rest_api_conn(trading_type='paper_trading')

        AlpacaApiConnMock.assert_called_with(trading_type='paper_trading')


class TestPostgresConnection(unittest.TestCase):
    @patch.object(data_io, 'postgres_conn')
    def test_postgres_conn(self, PostgresConnMock: Mock):
        postgres_conn_mock = Mock()
        PostgresConnMock.return_value = postgres_conn_mock

        data_io.postgres_conn()

        PostgresConnMock.assert_called_with()


class TestGeneratePathToWrite(unittest.TestCase):
    """Ensures path is built correctly."""
    def test_generate_path_to_write(self):
        # Unsupported lob
        with pytest.raises(ValueError):
            _ = data_io.generate_path_to_write(environment='prod',
                                               granularity='unsupported_granularity',
                                               dataset_name='test_dataset')

        # Writing to default base path
        actual = data_io.generate_path_to_write(environment='prod',
                                                granularity='daily',
                                                dataset_name='test_dataset',
                                                timestamp='2020-09-15_01-39-54')
        assert actual == '/group/wsbtrading/prod/daily/test_dataset/2020-09-15_01-39-54'

        # Write to another base path
        actual = data_io.generate_path_to_write(environment='prod',
                                                granularity='daily',
                                                dataset_name='stock_prices',
                                                root_path='/user/bdeely/',
                                                timestamp='version_1')
        assert actual == '/user/bdeely/prod/daily/stock_prices/version_1'

        # Extra slash at end of base path
        actual = data_io.generate_path_to_write(environment='prod',
                                                granularity='daily',
                                                dataset_name='stock_prices',
                                                root_path='/user/bdeely/',
                                                timestamp='version_1')
        assert actual == '/user/bdeely/prod/daily/stock_prices/version_1'

        # Spaces and caps in project name
        actual = data_io.generate_path_to_write(environment='prod',
                                                granularity='daily',
                                                dataset_name='My DaTASET Name',
                                                timestamp='job_run_v4')
        assert actual == '/group/wsbtrading/prod/daily/my_dataset_name/job_run_v4'
