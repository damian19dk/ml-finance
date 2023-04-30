# Machine learning in algotrading

:hammer: **Project is in early stage - don't expect fireworks!!!** :hammer:

## :moneybag: Purpose
It's quite easy to point, which moments were good to buy&sell but it's rather complicated to explain **why**. Is it because of market sentiment, social events or economic indicators? That's why I want to make model which explains, why some buys and sells should have been made. The same model might be used to predict future buy&sell signals.

The idea behind implementation is simple:
1. Get data for market you are interested in (in csv format)
2. Add columns with indicators/events which you find important
3. Mark timestamps which are good for buy&sell (add numeric column `Buy/Sell` to candle data) with custom mapping (0 - SELL, 1 - NOTHING, 2 - BUY) - example in `data/btc/target/btc-usd_2018-04-23_2023-04-23_target`
4. Pass extended data to ML algorithm (like decision tree) and pray to God for good model.

Using it we should get some correlation between input features and their importance on decision making.
Good candidates for parameters are:
- price (open,close,high,low)
- volume
- social events (like Musk buying BTC - looked kinda promising)
- TA (technical analysis, like SMA, STOCH indicators)
- on-chain analysis (NUPL for example or active adresses number)

I have no clue if it will work, I'm not ML expert - but the feature will show who was right :) 

## :page_with_curl: How to use it

### Structure
`data` keeps market data for assets like crypto, stocks, forex
- `market` contains raw data (from Yahoo without modifications)
- `target` contains data extended with social/technical/on-chain indicators and buy&sell signals - it's used as training feed
`model.py` it's responsible for training and generating model 
`backtest.py` run backtest with Backtrader

### Installation

Prepare environment and install dependencies:
```shell
python -m venv venv # to create virtual env (don't mess your python global environment)
source venv/bin/activate # activate it
pip install -r requirements.txt # install needed dependencies (pandas, matplotlib, backtrader)
```

### Generate model

Model generation takes place in `model.py` and it's called automatically from `backtest.py`. In the future some CLI will be provided to save model for later use.

### Run backtest

Below command generates decision tree (maybe in future it will have more options) from training data and run backtest:
```shell
python backtest.py -i data/btc/target/btc-usd_2018-04-23_2023-04-23_target.csv
```
if you are stuck, type to get help:
```shell
python backtest.py -h
```

## :construction: Contributing 
Please, don't waste your time on this amatour project but feel free to use techniques and data provided in this repo.
If you really want to add/change sth you can open an issue (or pull request if you see some improvements in code).
