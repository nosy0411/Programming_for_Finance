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

##### ETF to construct portfolio 

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

##### market_model_estimation.ipynb
- Studied basic market model (linear regression, CAPM, 3 factor model) and estimated time series beta
<br>

##### performance_criterion.ipynb
- Examined performance criterion such as CAGR, MDD, correlation, r-squared, sharpe ratio, trynor ratio, sortino ratio, information ratio
<br>
  
- Parsed stock and financial data from sites that provied various types of data such as Yahoo finance, Naver finance and KRX etc, and managed stock price and financial data using DBMS  
<br>
  
##### input_and_ouput.ipynb

- Studied various ways to read, write, and store data using python such as text file, excel, csv, pickle, and HDF5
<br>
  
##### MPT.ipynb
- Computed random portfolios and efficient frontier and constructed sharp optimum portfolio and capital asset pricing model from the sharp optimum portfolio
<br>
  
##### tactical_asset_allocation.ipynb, MDP.ipynb, risk_parity.ipynb
- Implemented tactical asset allocation strategies such as Most-diversified portfolio, risk-parity portfolio using ETF
<br>

##### dual_momentum.ipynb
- Formulated Gary Antonacci's dual momentum investing strategies to reduce MDD and increase return  
<br>

### 4.Derivatives

#### binomial_modeling
- Modeled n-period binomial model of no-dividend europian call option in a risk-neutral world and visualized results using Plotly package
<br>

##### parallel_programming.ipynb
- Improved computation speed of pricing binomial model options and compared the computation time of numpy, numba packages and parallel programming
<br>

##### monte_carlo.ipynb
1. Calculated europian options which underlying stock's prices following the Wiener process were discretized using euler scheme for computer simulation
2. Used static and dynamic simulation methods and compared with benchmark values calculated by the Black-Scholes Merton valuation formula
3. Generated random numbers following standard normal distribution for simulation using variance reduction technique like momentum matching and antithetic variates
4. Designed the square-root diffusion model which is a type of mean reversion model proposed by Cox-Ingersoll-Ross for short-term interest rate model. In order to discretize to simulate, euler scheme which is called full truncation and exact scheme discretization method were used. Visulaized the simulation paths and the results at maturity as a histogram and compared the results for bias error and execution time
5. Designed stochastic volatility model like heston model and to obtain the instantaneous correlation coefficient, Cholesky decomposition was performed on the correlation matrix. Visualized the results of simulating two stochastic processes of stock price and volatility model at maturity as a histogram and stochastic volatility model paths
6. Designed jump diffusion model and visulaized the simulation paths and the results at maturity as a histogram
7. Designed monte carlo simulation on GBM and least-squares monte carlo simulation(LSM) on American options. Visulaized and compared european options and LSM Monte Carlo estimator values
<br>

##### implicit_fdm.ipynb, explicit_fdm.ipynb, crank_nicolson_fdm.ipynb
- Compared results from Finite Difference Methods such as implict, explicit and crank nicolson for the pricing of financial derivatives like European vanilla options and americane options
<br>

##### risk_measure.ipynb
1. Calculated and visualized Value-at-Risk for stock following geometric Brownian motion and jump diffusion and stock price over a certain period in the past
2. Compared VaR, CVaR and CVA for stock following GBM and european option and visualized losses due to risk-neutrally expected default as a histogram for stock and european option
<br>

#### qnantlibrary
- Used python quantlib for computing Greeks of options on stock index, future and currency and modeling implied volatility surface using KRX financial data and studied the impact on P&L
<br>

#### greeks
- Modeled basic Greeks surface and visualized using Plotly package
<br>

##### imp_vol.ipynb
1. Calculated implied volatility using newton-raphson method and weighted bisection method on european option
2. Estimated the implied volatility of options underlying on the VSTOXX volatility index based on the option implied volatility of the EURO STOXX 50 index.
3. Identified volatility smile by visualizing implied volatility values for each maturity and strike price as dots and with the same maturity and different strike prices as a single line

<br>

### Statistics

<br>

### Timeseries_study

<br>

### System trading

<br>

