from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from argparse import ArgumentParser
import os.path  
import sys 
import backtrader as bt

import pandas

from model import Model, PredictedSignal 

class DecisionTreeStrategy(bt.Strategy):

    params = (
        ('training_data', ''),
    )

    def log(self, txt, dt=None):
        """ Logging function fot this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self, params=None):
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val) 
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # path = "data/btc/target/btc-usd_2018-04-23_2023-04-23_target.csv"
        path = self.p.training_data
        print(f'Train model with: {path}')
        df = pandas.read_csv(path)
        self.model = Model(df)
        print('Training ended successfully!')

        # To keep track of pending orders
        self.order = None

    def create_prediction(self) -> PredictedSignal:
        ds = {
                'Open': self.datas[0].open[0],
                'High': self.datas[0].high[0],
                'Low': self.datas[0].low[0],
                'Close': self.datas[0].close[0],
                'Volume': self.datas[0].volume[0]
        }
        ds = pandas.DataFrame(ds, index=[0])
        return self.model.predict_signal(ds)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        prediction = self.create_prediction()
        if not self.position:
            if prediction == PredictedSignal.BUY:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if prediction == PredictedSignal.SELL:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == "__main__":
    parser = ArgumentParser(description='Generates model from training data and runs backtest on strategy based from model')
    parser.add_argument('-i', '--input', help='Input market and training data', required=True)
    args = parser.parse_args()

    # Create a cerebro entity and register strategy
    cerebro = bt.Cerebro()
    cerebro.addstrategy(DecisionTreeStrategy, {'training_data': args.input})

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, args.input)

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
