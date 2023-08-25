# Manifold Strategies

This repo contains utilities for developing and backtesting algorithmic trading strategies on [Manifold Markets](https://manifold.markets). It is designed to be used with [my fork of Manifoldpy](https://github.com/jagilley/manifoldpy). I wouldn't suggest using the original Manifoldpy, as I've made changes to make it easier to work with Manifoldpy locally. You're welcome to try, though.

The main contributions of this repo are `strategy.py` and `time_utils.py`. The former contains a base class for developing and backtesting strategies, and the latter contains utilities for working with time series data.

## Installation

1. `git clone https://jagilley/manifoldpy`
2. `pip install tqdm pandas openai`

Please feel to contribute! I'm happy to answer any questions you have about the code, as it's fairly awful for now.