# Programming_for_Finance
## Learned programming for finance from the basics of python to stocks, bonds, portfolios, and derivatives. 
### 1.Basic 

- Studied intermediate python syntax and how to use python packages better such as pandas dataframe, numpy and matplotlib in a variety of situations beyond the basics

<br>

### 2.Crawling

- Studied concept of static and dynamic crawling
- Crawled interest rates from Economic Statistics system(ECOS API), WSJ

<br>

### 3.Portfolio study

#### ETF to construct portfolio 

- SPY : SPDR S&P 500 (SPY)
- IEV : iShares Europe ETF (IEV)
- EWJ : iShares MSCI Japan ETF (EWJ)
- EEM : iShares MSCI Emerging Markets Indx (EEM)
- TLT : iShares Barclays 20+ Yr Treas.Bond (TLT)
- IEF : iShares Barclays 7-10 Year Trasry Bnd Fd (IEF)
- IYR : iShares US Real Estate ETF (IYR)
- RWX : SPDR Dow Jones Interntnl Real Estate ETF (RWX)
- GLD : SPDR Gold Shares (GLD)
- DBC : PowerShares DB Com Indx Trckng Fund (DBC)
<br>

- __market_model_estimation.ipynb__ : Studied basic market model (linear regression, CAPM, 3 factor model) and estimated time series beta
<br>

- __performance_criterion.ipynb__ : Examined performance criterion such as CAGR, MDD, correlation, r-squared, sharpe ratio, trynor ratio, sortino ratio, information ratio
<br>
  
- Parsed stock and financial data from sites that provied various types of data such as Yahoo finance, Naver finance and KRX etc, and managed stock price and financial data using DBMS  
<br>
  
- __input_and_ouput.ipynb__ : Studied various ways to read, write, and store data using python such as text file, excel, csv, pickle, and HDF5
<br>
  
- __MPT.ipynb__ : Computed random portfolios and efficient frontier and constructed sharp optimum portfolio and capital asset pricing model from the sharp optimum portfolio
<br>
  
- __tactical_asset_allocation.ipynb, MDP.ipynb, risk_parity.ipynb__ : Implemented tactical asset allocation strategies such as Most-diversified portfolio, risk-parity portfolio using ETF
<br>

- __dual_momentum.ipynb__ : Formulated Gary Antonacci's dual momentum investing strategies to reduce MDD and increase return  
<br>

### 4.Derivatives

- __binomial_modeling__ : Modeled n-period binomial model of no-dividend europian call option in a risk-neutral world and visualized results using Plotly package
<br>

- __parallel_programming.ipynb__ : Improved computation speed of pricing binomial model options and compared the computation time of numpy, numba packages and parallel programming
<br>

- __monte_carlo.ipynb__ : Calculated europian options which underlying stock's prices following the Wiener process were discretized using euler scheme for computer simulation
- Used static and dynamic simulation methods and compared with benchmark values calculated by the Black-Scholes Merton valuation formula
- Generated random numbers following standard normal distribution for simulation using variance reduction technique like momentum matching and antithetic variates
- Designed the square-root diffusion model which is a type of mean reversion model proposed by Cox-Ingersoll-Ross for short-term interest rate model. In order to discretize to simulate, euler scheme which is called full truncation and exact scheme discretization method were used. Visulaized the simulation paths and the results at maturity as a histogram and compared the results for bias error and execution time
- Designed stochastic volatility model like heston model and to obtain the instantaneous correlation coefficient, Cholesky decomposition was performed on the correlation matrix. Visualized the results of simulating two stochastic processes of stock price and volatility model at maturity as a histogram and stochastic volatility model paths
- Designed jump diffusion model and visulaized the simulation paths and the results at maturity as a histogram
- Designed monte carlo simulation on GBM and least-squares monte carlo simulation(LSM) on American options. Visulaized and compared european options and LSM Monte Carlo estimator values
<br>

- __implicit_fdm.ipynb, explicit_fdm.ipynb, crank_nicolson_fdm.ipynb__ : Compared results from Finite Difference Methods such as implict, explicit and crank nicolson for the pricing of financial derivatives like European vanilla options and americane options
<br>

- __risk_measure.ipynb__ : Calculated and visualized Value-at-Risk for stock following geometric Brownian motion and jump diffusion and stock price over a certain period in the past
- Compared VaR, CVaR and CVA for stock following GBM and european option and visualized losses due to risk-neutrally expected default as a histogram for stock and european option
<br>

- __qnantlibrary__ : Used python quantlib for computing Greeks of options on stock index, future and currency and modeling implied volatility surface using KRX financial data and studied the impact on P&L
<br>

- __greeks__ : Modeled basic Greeks surface and visualized using Plotly package
<br>

- __imp_vol.ipynb__ : Calculated implied volatility using newton-raphson method and weighted bisection method on european option
- Estimated the implied volatility of options underlying on the VSTOXX volatility index based on the option implied volatility of the EURO STOXX 50 index.
- Identified volatility smile by visualizing implied volatility values for each maturity and strike price as dots and with the same maturity and different strike prices as a single line

<br>

### Statistics

<br>

### Timeseries_study

<br>

### System trading

<br>

