# algotrading_sandbox
Backtesting library with basic portfolio analytics, fetches data from AlphaVantage.co (requires API key)
Refer to the AlphaVantage terms of service to make use of their API https://www.alphavantage.co/terms_of_service/

FUNCTIONS:
    
    define_envirnoment(stock_universe,initial_capital,API_key_alphavantage,Full=False,granularity="DAILY"): Must be called at the beginning of the program, downloads data and creates fundamental variables (granularity can be DAILY or INTRADAY_1M for data updated to the minute)
    
    plot_stocks(array_stock_tickers): Plots the time series of the specified stock 
    
    summary(): Prints a summary of the data (the first datapoints and some basi information and statistics)
    
    start_backtest(my_algo): Starts the trading, gets a function as input containing the trading algorithm
    
    curr_price(stock_name): Returns the current price (during trading) of the stock
    
    buy(stock_name,quantity_dollar): Buys the specified dollar amount of the stock, updates the portfolio
    
    sell(stock_name,quantity_dollar): Sells the specified dollar amount of the stock, updates the portfolio
    
    get_time_series(stock_name): Returns the time series for the specified stock as a numpy array
    
    eval_portfolio(): Returns the total value of the portfolio (cash + positions value)
    
    portfolio_performance(): Plot the performance during the period of the portfolio
    

    
