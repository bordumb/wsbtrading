import unittest
import math
import pandas as pd
from pandas._testing import assert_frame_equal

from trading import maths


class TestDivision(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['timestamp', 'low', 'high', 'low_perc_high']
        data = [
            (1, 1, 1, 1),
            (2, 1, 2, 0.5),
            (3, 3, 9, 0.3333333333333333),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_divide_kernel(self):
        """Ensure we can divide properly."""
        actual = maths.divide_kernel(numerator=1, denominator=1)
        assert actual == 1

        actual = maths.divide_kernel(numerator=3, denominator=9)
        assert math.isclose(actual, 0.33333333333)

        actual = maths.divide_kernel(numerator=3, denominator=0)
        assert actual == 0


    def test_divide(self):
        """Ensures we can correctly divide when using a pandas DF."""
        mock_df = self.expected_df.drop('low_perc_high', axis=1)

        actual = maths.divide(df=mock_df, numerator_col='low', denominator_col='high')

        assert_frame_equal(actual, self.expected_df, check_dtype=True)
