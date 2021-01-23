import unittest
from datetime import datetime
import pandas as pd
from pandas._testing import assert_frame_equal

from trading.utils import dates


class TestConvertUnixTimestampToDate(unittest.TestCase):
    def setUp(self) -> None:
        # yapf: disable
        schema = ['idx', 'timestamp', 'eventDate']
        data = [
            (0, 1593556445000, '2020-06-30'),
            (1, 1592951645000, '2020-06-23'),
            (2, 1592778845000, '2020-06-21'),
            (3, 1593641161682, '2020-07-01'),
            (4, 1583715763996, '2020-03-09'),
            (5, 1593640898412, '2020-07-01'),
        ]
        # yapf: enable
        self.expected_df_no_time = pd.DataFrame(data=data, columns=schema)

        schema = ['idx', 'timestamp', 'eventDateTime']
        data = [
            (0, 1593556445000, '2020-06-30 22:34:05'),
            (1, 1592951645000, '2020-06-23 22:34:05'),
            (2, 1592778845000, '2020-06-21 22:34:05'),
            (3, 1593641161682, '2020-07-01 22:06:01'),
            (4, 1583715763996, '2020-03-09 01:02:43'),
            (5, 1593640898412, '2020-07-01 22:01:38'),
        ]
        self.expected_df_with_time = pd.DataFrame(data=data, columns=schema)

    def test_convert_unix_timestamp_to_date_kernel(self):
        """Ensures the correct timestamp to date conversion"""
        # no time
        timestamp = 1593556445000
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=False)
        assert actual == '2020-06-30'

        timestamp = 1593642847059
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=False)
        assert actual == '2020-07-01'

        timestamp = 1593641161682
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=False)
        assert actual == '2020-07-01'

        timestamp = 1593640898412
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=False)
        assert actual == '2020-07-01'

        timestamp = 1583715763996
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=False)
        assert actual == '2020-03-09'

        timestamp = 1583715789701
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=False)
        assert actual == '2020-03-09'

        # with time
        timestamp = 1583715789701
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=True)
        assert actual == '2020-03-09 01:03:09'

        timestamp = 1583715763996
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=True)
        assert actual == '2020-03-09 01:02:43'

        timestamp = 1593640898412
        actual = dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=True)
        assert actual == '2020-07-01 22:01:38'

    def test_convert_unix_timestamp_to_date_kernel_udf(self):
        """Ensures the correct UDF implementation for unix_timestamp_to_date"""
        # no time
        actual = self.expected_df_no_time[['idx', 'timestamp']]
        actual['eventDateTime'] = actual['timestamp']\
            .apply(lambda x: dates.convert_unix_timestamp_to_date_kernel(timestamp=x, output_time=True))

        assert_frame_equal(actual, self.expected_df_with_time, check_dtype=True)

        # with time
        actual = self.expected_df_with_time[['idx', 'timestamp']]
        actual['eventDateTime'] = actual['timestamp']\
            .apply(lambda x: dates.convert_unix_timestamp_to_date_kernel(timestamp=x, output_time=True))

        assert_frame_equal(actual, self.expected_df_with_time, check_dtype=True)


class TestParseDateFromString(unittest.TestCase):
    def test_parse_date_from_string(self):
        """Proper date object is constructed."""
        actual = dates.parse_date_from_string('2020-04-20')
        expected = datetime.strptime('%s 00:00:00' % '2020-04-20', '%Y-%m-%d %H:%M:%S')

        assert actual == expected


class TestBuildDateRange(unittest.TestCase):
    def test_build_date_range(self):
        """Proper date range is constructed."""
        actual = dates.build_date_range(start_date='2020-04-01', end_date='2020-04-03')
        expected = ['2020-04-01', '2020-04-02', '2020-04-03']

        assert actual == expected

        # end of year
        actual = dates.build_date_range(start_date='2019-12-30', end_date='2020-01-01')
        expected = ['2019-12-30', '2019-12-31', '2020-01-01']

        assert actual == expected

        # leap year
        actual = dates.build_date_range(start_date='2020-02-28', end_date='2020-03-02')
        expected = ['2020-02-28', '2020-02-29', '2020-03-01', '2020-03-02']

        assert actual == expected


class TestDateRangeToUnixRange(unittest.TestCase):
    def test_date_range_to_unix_range(self):
        """Date range is converted to a unix range."""
        actual = dates.date_range_to_unix_range(date_range=['2020-04-01', '2020-04-02', '2020-04-03'])
        expected = '{2020-04-01,2020-04-02,2020-04-03}'

        assert actual == expected


class TestDateSlider(unittest.TestCase):
    def test_date_slider(self):
        """Checks sliding by a positive number of days."""
        actual = dates.date_slider(date='2020-01-01', days_to_add=7)
        expected = '2020-01-08'

        assert actual == expected

        # zero days
        actual = dates.date_slider(date='2020-01-01', days_to_add=0)
        expected = '2020-01-01'

        assert actual == expected

        # negative days
        actual = dates.date_slider(date='2020-01-01', days_to_add=-2)
        expected = '2019-12-30'

        assert actual == expected
