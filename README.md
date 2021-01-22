trading is a library that handles data I/O, aggregation, 
and modeling to facilitate algorithmic trading stategies. 

# Reinforcement Learning and Automated Stock Trading
This is a pet project to try using an ensemble strategy for online, algorithmic trading.

The goal is really just to get it up and running, but let's not kid ourselves...
> We want some tendies.

This project is inspired by [this blog](https://towardsdatascience.com/deep-reinforcement-learning-for-automated-stock-trading-f1dad0126a02),
however the aim is to advance that work by adding the extending it to the following:
* Real-time trading (the original methodology made just bi-annual trading adjustments)
* Productionize to some environment (TBD, but likely using AWS)
* Placing real trades


## Abstract
Procure Tendies.

## Installation:
```shell
git clone https://github.com/bordumb/trading.git
```

### Prerequisites
TODO: Fill Out


#### Mac OS X
Installation of system packages on Mac requires [Homebrew](https://brew.sh). With Homebrew installed, run the following:
```bash
brew install cmake openmpi
```


### Create and Activate Virtual Environment (Optional but highly recommended)
cd into this repository
```bash
cd trading
```
Under folder `/trading`, create a virtual environment
```bash
conda env update -n trading3 -f reqs3.yml
```
To activate our virtual env:
```
conda activate phobos3
```

## Dependencies

The script has been tested running under **Python >= 3.6.0**, with the folowing packages installed:

```shell
pip install -r reqs3.yml
```

### Open Questions
The following are a list of topics that are not fully baked out and largely pertain to tooling choices.

### About Tensorflow 2.0
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


## Run Deep Reinforcement Learning (DRL) Ensemble Strategy
```shell
python run_DRL.py
```

## Backtesting
We will use Quantopian's [pyfolio package](https://github.com/quantopian/pyfolio) to do the backtesting.
Please install it if you haven't already:
```
pip install pyfolio
```
[Backtesting script](backtesting.ipynb)

## Status

<details><summary><b>Version History</b> <i>[click to expand]</i></summary>
<div>

* 1.0.1
	Changes: added ensemble strategy
* 0.0.1
    Simple version
</div>
</details>

## Data
Data sources are TBD

### Ensemble Strategy
Our purpose is to create a highly robust trading strategy. So we use an ensemble method to automatically select the best performing agent among PPO, A2C, and DDPG to trade based on the Sharpe ratio. The ensemble process is described as follows:
* __Step 1__. We use a growing window of 𝑛 months to retrain our three agents concurrently. In this paper we retrain our three agents at every 3 months.
* __Step 2__. We validate all 3 agents by using a 12-month validation- rolling window followed by the growing window we used for train- ing to pick the best performing agent which has the highest Sharpe ratio. We also adjust risk-aversion by using turbulence index in our validation stage.
* __Step 3__. After validation, we only use the best model which has the highest Sharpe ratio to predict and trade for the next quarter.

## Performance
<img src=figs/performance.png>
