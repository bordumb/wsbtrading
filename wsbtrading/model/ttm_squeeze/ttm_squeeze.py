from wsbtrading.data_io import snapshot_daily
from wsbtrading.maths import is_in_squeeze
from wsbtrading.order import order

dict_of_df = snapshot_daily.read_snapshot()
stock_ticker_list = dict_of_df.values()

# TODO: differentiate between a positive squeeze or negative squeeze to determine if buying or selling is a good idea
for stock_ticker in stock_ticker_list:
    df = dict_of_df[stock_ticker]
    is_in_squeeze = is_in_squeeze(df=df,
                                  metric_col='Close',
                                  low_col='Low',
                                  high_col='High',
                                  rolling_window=20)

    if is_in_squeeze:
        print('value will print money!')
        order.execute_order(symbol=stock_ticker,
                            qty=100,
                            side='buy',
                            type='market',
                            time_in_force='gtc',
                            trading_type='paper_trading')

    else:
        print('This stock is junk!')
        print('Not touching it with a 10-foot stick.')
