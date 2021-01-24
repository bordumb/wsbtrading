from wsbtrading.data_io import snapshot_daily
from wsbtrading.maths import is_in_squeeze

dict_of_df = snapshot_daily.read_snapshot()

for value in dict_of_df.values():
    df = dict_of_df[value]
    is_printing_tendies = maths.is_in_squeeze(df=df,
                                        metric_col='Close',
                                        low_col='Low',
                                        high_col='High',
                                        rolling_window=20)
    if is_printing_tendies:
        print('value will print tendies!')
    else:
        print('This stock is junk!')
