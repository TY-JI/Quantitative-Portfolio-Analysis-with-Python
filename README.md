# Quantitative Portfolio Analysis 

### *Using Ledoit-Wolf covariance estimation, Black-Litterman expected returns and constrained mean-variance portfolio optimization* ###

## Current Features ##

### 

* Historical market data retrieval using *yfinance*
* Data validation and preprocessing
* Ledoit-Wolf covariance matrix estimation
* Black-Litterman equilibrium returns with investor views
* Constrained MVO using projected gradient ascent
* Command-line interfacing for analytical configuration 

###

## Analysis Pipeline ##

__Parsing of Command-Line Args__ - ```parser.py```

Parses command-line arguments for use by the appropriate functions

__Market Data__ - ```data.py```

Retrieves market data and validates historical prices.

__Returns__ - ```returns.py```

Currently calculates percentage returns. Future development may include configurable transaction costs.

__Ledoit-Wolf covariance estimation__ - ```covariance.py```

Computes the Ledoit-Wolf covariance matrix according to the 2003 paper by Oliver Ledoit and Michael Wolf.

__Black-Litterman expected returns__ - ```market.py, black_litterman.py, views.py```

Incorporates user-specified investor views to compute a vector of expected returns in accordance with the Black-Litterman framework.

Market equilibrium returns, risk aversion and market weights are supplied by ```market.py```.

__Constrained MVO using Projected Gradient Ascent__ - ```optimizer.py```

Optimizes portfolio weights using the Ledoit-Wolf covariance matrix and Black-Litterman expected returns. 

Long-only constraints and fully invested portfolio weights are enforced using Projected Gradient Ascent.

###  ###

## Usage ##

__Installation__

Clone the repository and install required dependencies.

```bash
git clone https://github.com/TY-JI/Quantitative-Portfolio-Analysis-with-Python
cd Quantitative-Portfolio-Analysis
pip install -r requirements.txt
```

__Command line arguments__ 

Analysis can be configured using command-line arguments.
```
  --tickers [TICKERS ...], -T [TICKERS ...]    |    Space-separated list of stock tickers.    |

  --interval {1m,5m,15m,60m,1h,1d}, -I {1m,5m,15m,60m,1h,1d}    |    Data sampling interval.    |
                        
  --period PERIOD, -P PERIOD    |    Lookback period (e.g., 60d, 1y, 2y). Cannot be used with --start and --end.    |
                        
  --start START, -S START   |    Start date in YYYY-MM-DD format.    |

  --end END, -E END    |    End date in YYYY-MM-DD format.    |

  --view VIEW [VIEW ...], -V VIEW [VIEW ...]    |    Add a view: relative ASSET1 ASSET2 VALUE or absolute ASSET VALUE.    |

  --benchmark   |    Measures program runtime.    |
```

__Example Command-Line Arguments__

*Runs analysis using the default configurations*

```bash
python main.py
```
*Analyse a custom set of assets*
```bash
python main.py --tickers AAPL MSFT GOOGL 
```
*Specify lookback period*
```bash
python main.py --tickers AAPL MSFT GOOGL JPM XOM --period 2y
```
*Inject investor views*
```bash
python main.py --tickers AAPL MSFT GOOGL JPM XOM --view relative MSFT AAPL 0.05 --view absolute GOOGL 0.10
```
*Measure total runtime*
```bash
python main.py --benchmark
```
