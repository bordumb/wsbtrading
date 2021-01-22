import unittest
import math
import pandas as pd
from pandas._testing import assert_frame_equal

from trading import maths


class TestDivision(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['timestamp', 'high', 'low', 'result']
        data = [
            (1, 1, 1, 1),
            (2, 1, 2, 0.5),
            (3, 3, 9, 0.3333333333333333),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_division_kernel(self):
        """Ensure we can divide properly."""
        actual = maths.divide_kernel(numerator=1, denominator=1)
        assert actual == 1

        actual = maths.divide_kernel(numerator=3, denominator=9)
        assert math.isclose(actual, 0.33333333333)

        actual = maths.divide_kernel(numerator=3, denominator=0)
        assert actual == 0


    def test_is_tab_header_cta_impression(self):
        """Ensures we can correctly divide when using a pandas DF."""
        mock_df = self.expected_df.drop('result', axis=1)

        actual = maths.divide(df=mock_df, numerator_col='high', denominator_col='low')

        assert_frame_equal(actual, self.expected_df, check_dtype=True)
