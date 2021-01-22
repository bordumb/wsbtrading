import unittest
import pandas as pd

from trading import maths


class TestDivision(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['timestamp', 'high', 'low', 'result']
        data = [
            (1, 1, 1, 1),
            (2, 1, 2, 0.5),
            (3, 3, 9, 0.33),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_division_kernel(self):
        """Ensure we can divide properly."""
        actual = maths.divide(numerator=1, denominator=1)
        assert actual == 0.5

        actual = maths.divide(numerator=3, denominator=9)
        assert actual == 0.3

        actual = maths.divide(numerator=3, denominator=0)
        assert actual == 0.3

        actual = pre_sub._is_tab_header_cta_impression_kernel(event_type=None, page_type=None, impressions=None)
        assert actual == 0

    def test_is_tab_header_cta_impression(self):
        """Ensures we can correctly divide when using a pandas DF."""
        mock_df = self.expected_df.drop('result')

        actual = maths.is_tab_header_cta_impression(df=mock_df)

        assert actual.collect() == self.expected_df.collect()
        assert actual.schema.names == self.expected_df.schema.names
