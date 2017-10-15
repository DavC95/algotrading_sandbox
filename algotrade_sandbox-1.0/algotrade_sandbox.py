#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import os,sys
import shutil
import time
from matplotlib import pyplot as plt
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET

__init_cap=0
__s_universe=[]
__positions_array={}
__close_matrix=pd.DataFrame()
__curr_epoch=0
__portfolio_value=[]

def define_environment(stock_universe,initial_capital,API_key_alphavantage,Full=False,granularity="DAILY"):
    #data retrieval
    print("\nDOWNLOADING STOCK DATA ...\n")
    global __init_cap,__s_universe,__positions_array,__portfolio_value
    __init_cap=initial_capital
    __portfolio_value.append(__init_cap)
    __s_universe=stock_universe
    shutil.rmtree("csv_files")
    os.makedirs("csv_files")
    for i in stock_universe:
        try:

            if Full==False and granularity=="DAILY":
                url_addr="https://www.alphavantage.co/query?function=TIME_SERIES_"+granularity+"&symbol="+str(i)+"&apikey=" + API_key_alphavantage+ "&datatype=csv"
            elif Full==True and granularity=="DAILY":
                url_addr="https://www.alphavantage.co/query?function=TIME_SERIES_"+granularity+"&symbol="+str(i)+"&apikey="+API_key_alphavantage+ "&datatype=csv"+"&outputsize=full"
            if granularity=="INTRADAY_1_MINUTE":
                url_addr="https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"+"&symbol="+str(i)+"&apikey="+API_key_alphavantage + "&datatype=csv"+"&outputsize=full"+"&interval=1min"

            urlretrieve(url_addr,"csv_files/"+str(i)+".csv")

            print(str(i)+" DATA SUCCESSFULLY DOWNLOADED")
        except: print("\nError downloading data: check internet connection")
    print("\n")
    __hist_closing_matrix()


def __hist_closing_matrix():
    df_final=pd.DataFrame()
    global __s_universe
    global __close_matrix
    for j in __s_universe:
        try:
            df=pd.read_csv("csv_files/"+str(j)+".csv")
            df_final[str(j)]=df["close"]
        except:
            print("\nDATA NOT VALID: CHECK THE CSV FILE FOR ALPHAVANTAGE TROUBLESHOOTING INFO")
            sys.exit()
    df_final["TIMESTAMP"]=df["timestamp"]
    __close_matrix=df_final


def plot_stocks(arr_stocks):
    plt.style.use("dark_background")
    for j in arr_stocks:
        plt.plot(__close_matrix[j])
    #plt.xticks(np.linspace(0,len(__close_matrix["TIMESTAMP"]),10))
    plt.xlabel("Time")
    plt.legend()
    #plt.grid()
    plt.show()


def summary():
    print("------"*int(len(__s_universe)/2)+"DATA SUMMARY"+"------"*int(len(__s_universe)/2))
    print("DATA FROM: "+ __close_matrix["TIMESTAMP"].iloc[-1] +" TO: "+ __close_matrix["TIMESTAMP"].iloc[0])
    print("\n")
    print("    "*int(len(__s_universe)+1)+"DATA HEAD\n")
    print(__close_matrix.head(20))
    print("----------"*int(len(__s_universe)+1))
    print("    "*int(len(__s_universe)+1)+"DATA DESCRIPTION\n")
    print(__close_matrix.describe())


def start_backtest(trade_algo):
    global __curr_epoch
    global __positions_array
    global __s_universe
    for i in __s_universe:
        __positions_array[i]=0
    print("\n-------- STARTING TRADING ---------")
    for i in range(0,len(__close_matrix)):
        trade_algo()
        eval_portfolio()
        __curr_epoch+=1

def curr_price(stock_n):
    res=__close_matrix.iloc[::-1]
    return res[str(stock_n)].iloc[__curr_epoch]

def __eval_positions():
    global __s_universe
    global __positions_array
    port_value={}
    for i in __s_universe:
        port_value[i]=(__positions_array[i]*curr_price(i))
    return port_value

def buy(stock_name,quantity_curr):
    global __positions_array
    global __close_matrix
    global __s_universe
    global __init_cap
    __positions_array[stock_name]+=int(quantity_curr/curr_price(stock_name))
    __init_cap-=int(quantity_curr/curr_price(stock_name))*curr_price(stock_name)
    print("BUYING "+ str("%.6s" % stock_name)+ " AT " + str("%.2f" % curr_price(stock_name)) + "        CURRENT CASH: "+str("%.2f" % np.round(__init_cap,2)) +"       PORTFOLIO VALUE: " + str(__portfolio_value[-1])+ "        CURRENT POSITIONS: " + str(__eval_positions()))

def sell(stock_name,quantity_curr):
    global __positions_array
    global __close_matrix
    global __s_universe
    global __init_cap
    __positions_array[stock_name]-=int(quantity_curr/curr_price(stock_name))
    __init_cap+=int(quantity_curr/curr_price(stock_name))*curr_price(stock_name)
    print("SELLING "+ str("%.6s" % stock_name)+ " AT " + str("%.2f" % curr_price(stock_name)) +"        CURRENT CASH: "+str("%.2f" % np.round(__init_cap,2)) +  "       PORTFOLIO VALUE: " + str(__portfolio_value[-1]) + "        CURRENT POSITIONS: " + str(__eval_positions()))

def get_time_series(stck_nam):
    return __close_matrix[stck_nam]

def eval_portfolio():
    global __portfolio_value
    __portfolio_value.append(__init_cap+sum([__eval_positions()[i] for i in __s_universe]))

def portfolio_performance():
    plt.style.use("dark_background")
    plt.plot(__portfolio_value)
    plt.title("PORTFOLIO PERFORMANCE: " + __close_matrix["TIMESTAMP"].iloc[-1] +" - "+ __close_matrix["TIMESTAMP"].iloc[0])
    plt.show()
