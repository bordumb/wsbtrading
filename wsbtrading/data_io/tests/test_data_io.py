import unittest
from unittest.mock import Mock, patch

from wsbtrading.data_io import data_io


class TestAlpacaApiConnection(unittest.TestCase):
    @patch.object(data_io, 'alpaca_rest_api_conn')
    def test_alpaca_api_connection(self, AlpacaApiConnMock: Mock):
        alpaca_api_conn_mock = Mock()
        AlpacaApiConnMock.return_value = alpaca_api_conn_mock

        data_io.alpaca_rest_api_conn(trading_type='paper_trading')

        AlpacaApiConnMock.assert_called_with(trading_type='paper_trading')
