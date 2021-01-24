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


class TestSma(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', '2sma']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 30, 25.0),
            ('2017-01-05', 42, 32, 40, 35.0),
            ('2017-01-06', 52, 45, 50, 45.0),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_sma(self):
        """Ensures we correctly calculate the simple moving average (SMA)."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.sma(df=mock_df, metric_col='Close', rolling_window=2)

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestStandardDeviation(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', '2stddev']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 31, 7.778175),
            ('2017-01-05', 42, 32, 40, 6.363961),
            ('2017-01-06', 52, 45, 51, 7.778175),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_rolling_stddev(self):
        """Ensures we correctly calculate the simple moving average (SMA)."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.rolling_stddev(df=mock_df, metric_col='Close', rolling_window=2)

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestLowerBand(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', 'lower_band']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 31, 9.943651),
            ('2017-01-05', 42, 32, 40, 22.772078),
            ('2017-01-06', 52, 45, 51, 29.943651),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_lower_band(self):
        """Ensures we correctly calculate the lower band."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.lower_band(df=mock_df, metric_col='Close', rolling_window=2).drop(['2sma', '2stddev'], axis=1)

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestUpperBand(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', 'upper_band']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 31, 41.056349),
            ('2017-01-05', 42, 32, 40, 48.227922),
            ('2017-01-06', 52, 45, 51, 61.056349),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_upper_band(self):
        """Ensures we correctly calculate the upper band."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.upper_band(df=mock_df, metric_col='Close', rolling_window=2).drop(['2sma', '2stddev'], axis=1)

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestTrueRange(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', 'true_range']
        data = [
            ('2017-01-03', 22, 20, 20, 2),
            ('2017-01-04', 32, 20, 31, 12),
            ('2017-01-05', 42, 32, 40, 10),
            ('2017-01-06', 52, 45, 51, 7),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_true_range(self):
        """Ensures we correctly calculate the true range."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.true_range(df=mock_df, low_col='Low', high_col='High')

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestAtr(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', 'ATR']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 31, 7.0),
            ('2017-01-05', 42, 32, 40, 11.0),
            ('2017-01-06', 52, 45, 51, 8.5),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_avg_true_range(self):
        """Ensures we correctly calculate the average true range."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.avg_true_range(df=mock_df, low_col='Low', high_col='High', rolling_window=2)\
            .drop(['true_range'], axis=1)

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestLowerKeltner(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', 'lower_keltner']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 31, 15.00),
            ('2017-01-05', 42, 32, 40, 19.00),
            ('2017-01-06', 52, 45, 51, 32.75),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_lower_keltner(self):
        """Ensures we correctly calculate the lower Keltner."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.lower_keltner(df=mock_df, metric_col='Close', low_col='Low', high_col='High', rolling_window=2) \
            .drop(['2sma', 'true_range', 'ATR'], axis=1)

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestUpperKeltner(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', 'upper_keltner']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 31, 36.00),
            ('2017-01-05', 42, 32, 40, 52.00),
            ('2017-01-06', 52, 45, 51, 58.25),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_upper_keltner(self):
        """Ensures we correctly calculate the upper Keltner."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.upper_keltner(df=mock_df, metric_col='Close', low_col='Low', high_col='High', rolling_window=2) \
            .drop(['2sma', 'true_range', 'ATR'], axis=1)

        assert_frame_equal(actual, self.expected_df, check_dtype=True)


class TestIsInSqueeze(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['Date', 'High', 'Low', 'Close', 'upper_keltner']
        data = [
            ('2017-01-03', 22, 20, 20, None),
            ('2017-01-04', 32, 20, 31, 36.00),
            ('2017-01-05', 42, 32, 40, 52.00),
            ('2017-01-06', 52, 45, 51, 58.25),
        ]
        # yapf: enable
        self.expected_df = pd.DataFrame(data=data, columns=schema)

    def test_is_in_squeeze(self):
        """Ensures we correctly calculate when a stock is squeezing."""
        mock_df = self.expected_df[['Date', 'High', 'Low', 'Close']]

        actual = maths.is_in_squeeze(df=mock_df, metric_col='Close', low_col='Low', high_col='High', rolling_window=2)

        assert actual is False

#
#
# import math
# import pandas as pd
# from pandas._testing import assert_frame_equal
#
# from trading import maths
#
# schema = ['Date', 'High', 'Low', 'Close', 'lower_keltner']
# data = [
#             ('2017-01-03', 22, 20, 20, None),
#             ('2017-01-04', 32, 20, 31, 15.00),
#             ('2017-01-05', 42, 32, 40, 19.00),
#             ('2017-01-06', 52, 45, 51, 32.75),
#         ]
# # yapf: enable
# expected_df = pd.DataFrame(data=data, columns=schema)
#
# mock_df = expected_df[['Date', 'High', 'Low', 'Close']]
#
# metric_col='Close'
# low_col='Low'
# high_col='High'
# rolling_window=2
# lower_band_df = maths.lower_band(df=df, metric_col=metric_col, rolling_window=rolling_window)
# upper_band_df = maths.upper_band(df=lower_band_df, metric_col=metric_col, rolling_window=rolling_window)
# lower_keltner_df = maths.lower_keltner(df=upper_band_df, metric_col=metric_col, low_col=low_col, high_col=high_col,
#                                  rolling_window=rolling_window)
# upper_keltner_df = maths.upper_keltner(df=lower_keltner_df, metric_col=metric_col, low_col=low_col, high_col=high_col,
#                                  rolling_window=rolling_window)
#
# def is_squeeze(df):
#     return df['lower_band'].iloc[-3] > df['lower_keltner'].iloc[-3] and df['upper_band'].iloc[-3] < df['upper_keltner'].iloc[-3]
#
# is_squeeze(df=upper_keltner_df)
#
# actual = maths.is_in_squeeze(df=mock_df, metric_col='Close', low_col='Low', high_col='High', rolling_window=2)
# actual
#
#
#
