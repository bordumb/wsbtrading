![alt text](https://github.com/bordumb/wsbtrading/blob/main/images/WallStreetBets.png)

# Wall Street Bets Algorithmic Trading
This is a pet project to try using an ensemble strategy for online, algorithmic trading.

``wsbtrading`` is a library that handles data I/O, aggregation, 
and modeling to facilitate algorithmic trading stategies. 

### The goal is simple: tendies, tendies, tendies

This project is inspired by [this project](https://github.com/bordumb/Deep-Reinforcement-Learning-for-Automated-Stock-Trading-Ensemble-Strategy-ICAIF-2020),
however the aim is to advance that work by adding the extending it to the following:
* Real-time trading (the original methodology made just bi-annual trading adjustments)
* Productionize to some environment (TBD, but probably AWS)
* Placing real, automated trades

# User Guide
## Installation
This project is registered on [PyPi](https://pypi.org/project/wsbtrading/), so just install it like anything else you would:
```bash
pip install wsbtrading
```

If you have both python 2.7 and 3.x, you may get an error like below:
```bash 
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. pip 21.0 will drop support for Python 2.7 in January 2021. More details about Python 2 support in pip can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support pip 21.0 will remove support for this functionality.
Defaulting to user installation because normal site-packages is not writeable
ERROR: Could not find a version that satisfies the requirement wsbtrading (from versions: none)
ERROR: No matching distribution found for wsbtrading
```
If you get this, just explicitly install under python 3.x as follows:
```bash
python3 -m pip install --user wsbtrading
```

## Basic Usage
Let's say we have a time series like below:
```
Date        High  Low  Close
2017-01-03    22   20     20
2017-01-04    32   20     31
2017-01-05    42   32     40
2017-01-06    52   45     51
```
We can quickly apply various financial analysis. 
In the example below, we calculate the [lower and upper keltner channels](https://www.investopedia.com/terms/k/keltnerchannel.asp).
```python
from wsbtrading import maths

ROLLING_WINDOW = 2
CLOSE = 'Close'
LOW = 'Low'
HIGH = 'High'

lower_band_df = maths.lower_band(df=df, 
                                 metric_col=CLOSE, 
                                 rolling_window=ROLLING_WINDOW)

upper_band_df = maths.upper_band(df=df, 
                                 metric_col=CLOSE, 
                                 rolling_window=ROLLING_WINDOW)

lower_keltner_df = maths.lower_keltner(df=df, 
                                       metric_col=CLOSE, 
                                       low_col=LOW, 
                                       high_col=HIGH,
                                       rolling_window=ROLLING_WINDOW)

upper_keltner_df = maths.upper_keltner(df=df, 
                                       metric_col=CLOSE, 
                                       low_col=LOW, 
                                       high_col=HIGH,
                                       rolling_window=ROLLING_WINDOW)
```
After this, we end up with a much richer dataset:
```
         Date  High  Low  Close  2sma   2stddev  lower_band  upper_band  true_range   ATR  lower_keltner  upper_keltner
0  2017-01-03    22   20     20   NaN       NaN         NaN         NaN           2   NaN            NaN            NaN
1  2017-01-04    32   20     31  25.5  7.778175    9.943651   41.056349          12   7.0          15.00          36.00
2  2017-01-05    42   32     40  35.5  6.363961   22.772078   48.227922          10  11.0          19.00          52.00
3  2017-01-06    52   45     51  45.5  7.778175   29.943651   61.056349           7   8.5          32.75          58.25
```
Just for edification, this quick example constitutes the building blocks of a technical strategy, known as a ttm squeeze. 
[Here is a good article](https://tickertape.tdameritrade.com/tools/fearless-technician-ttm-squeeze-indicator-15072) on the topic, albeit from a pretty antiquated company.

You can see a simple implementation of this strategy in [wsbtrading/model/ttm_squeeze here](https://github.com/bordumb/wsbtrading/blob/main/wsbtrading/model/ttm_squeeze/ttm_squeeze.py).

Please note, the majority of analytical functionality overlaps with the technical analysis ``ta-lib``
So rather than recreate the wheel, it may be good to [read up on the library here](https://ta-lib.org/) as it will be
used quite a bit.

Going forward, the main focus on the ``maths`` module will be to add AI-related functionality and various strategies 
for automated trading. The goal is really to take the emotion out of making tendies.



# Developer Guide
## Installation
```shell
git clone https://github.com/bordumb/wsbtrading.git
```

## Development Rules
* Always create a new branch for any new changes
* Write code that adheres to [pep8](https://www.python.org/dev/peps/pep-0008/)
* Write tests for every function

#### Mac OS X
Installation of system packages on Mac requires [Homebrew](https://brew.sh). With Homebrew installed, run the following:
```bash
brew install cmake openmpi
```
If you're on Windows, use at your own risk and please note that we will not be supporting it in any way, shape, or form.
In fact if you're on Windows, it's a miracle you even found this page...

### Create and Activate Virtual Environment
cd into this repository
```bash
cd wsbtrading
```
From that root directory `/wsbtrading`, create a virtual environment
```bash
conda env update -n trading3 -f reqs3.yml
```
To activate our virtual env:
```
conda activate trading3
```

### Pushing updates to PyPi
Anytime any changes are made to the ``wsbtrading`` library, a new wheel package must be made and updates.

1. Delete all files in the `/dist` folder and the entire `build` directory
```bash
cd dist
rm -rf *
cd .. 
rm -rf build
```
2. Update the ``__version`` in the ``wsbtrading/__init__.py`` file, by increasing the number 1 integer higher 
```bash
cd wsbtrading
open __init__.py
```
3. Rebuild the wheel
```bash
python3 setup.py sdist bdist_wheel
```
4. Upload this latest package to PyPi
```bash 
twine upload dist/*
```
5. Updating your local package
```bash 
pip install wsbtrading --upgrade
```

# Open Questions
The following are a list of topics that are not fully baked out and largely pertain to tooling choices.

## About Tensorflow 2.0
This module will utilize Tensorflow, so if you don't have that, please install it below
```bash
pip install tensorflow
 ```

If you have questions regarding Stable-baselines package, please refer to [Stable-baselines installation guide](https://github.com/hill-a/stable-baselines). Install the Stable Baselines package using pip:
```
pip install stable-baselines[mpi]
```

This includes an optional dependency on MPI, enabling algorithms DDPG, GAIL, PPO1 and TRPO. If you do not need these algorithms, you can install without MPI:
```
pip install stable-baselines
```

Please read the [documentation](https://stable-baselines.readthedocs.io/) for more details and alternatives (from source, using docker).

## Backtesting
We will use Quantopian's [pyfolio package](https://github.com/quantopian/pyfolio) to do the backtesting.
Please install it if you haven't already:
```
pip install pyfolio
```
[Backtesting script](backtesting.ipynb)

## Data Sources
Data sources are TBD
### Crypto
* TBD

### Stocks Trading
* [Alpaca](https://github.com/alpacahq/alpaca-trade-api-python)

### Options Trading
* TBD


## Trading Platforms
Trading platforms are TBD
### Crypto
* [Shrimpy](https://blog.shrimpy.io/blog/binance-crypto-trading-bots-with-python)
* [Binance](https://github.com/binance/binance-spot-api-docs)

### Stocks Trading
* [Alpaca](https://github.com/alpacahq/alpaca-trade-api-python)

### Options Trading
* [Lightspeed Trading](https://www.lightspeed.com/trading-api/)

## Ensemble Strategy
Our purpose is to create a highly robust trading strategy. So we use an ensemble method to automatically select the best performing agent among PPO, A2C, and DDPG to trade based on the Sharpe ratio. The ensemble process is described as follows:
* __Step 1__. We use a growing window of 𝑛 months to retrain our three agents concurrently. In this paper we retrain our three agents at every 3 months.
* __Step 2__. We validate all 3 agents by using a 12-month validation- rolling window followed by the growing window we used for train- ing to pick the best performing agent which has the highest Sharpe ratio. We also adjust risk-aversion by using turbulence index in our validation stage.
* __Step 3__. After validation, we only use the best model which has the highest Sharpe ratio to predict and trade for the next quarter.

## Performance
TODO: Add performance reporting