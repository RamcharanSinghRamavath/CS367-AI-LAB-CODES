import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

def get_stock_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data[['Adj Close']]


def preprocess_data(stock_data):
    stock_data['Returns'] = np.log(stock_data['Adj Close'] / stock_data['Adj Close'].shift(1))
    stock_data.dropna(inplace=True)
    
    scaler = StandardScaler()
    stock_data['Scaled Returns'] = scaler.fit_transform(stock_data[['Returns']])
    
    return stock_data

def train_hmm(stock_data, n_states):
    X = stock_data[['Scaled Returns']].values
    
    hmm_model = GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=1000)
    hmm_model.fit(X)
    
    hidden_states = hmm_model.predict(X)
    
    stock_data['Hidden States'] = hidden_states
    
    return hmm_model, stock_data

def plot_hidden_states(stock_data, ticker):
    fig, axs = plt.subplots(stock_data['Hidden States'].nunique(), figsize=(10, 8))
    fig.suptitle(f'Hidden States for {ticker}', fontsize=16)
    
    for i, state in enumerate(sorted(stock_data['Hidden States'].unique())):
        axs[i].plot(stock_data.index, stock_data['Adj Close'], color='gray', alpha=0.4)
        axs[i].scatter(stock_data[stock_data['Hidden States'] == state].index,
                       stock_data[stock_data['Hidden States'] == state]['Adj Close'],
                       label=f'State {state}', alpha=0.6)
        axs[i].legend()

    plt.tight_layout()
    plt.show()

def compare_instruments(tickers, start, end, n_states):
    for ticker in tickers:
        print(f'Analyzing {ticker}...')
        stock_data = get_stock_data(ticker, start, end)
        stock_data = preprocess_data(stock_data)
        hmm_model, stock_data = train_hmm(stock_data, n_states)
        plot_hidden_states(stock_data, ticker)

if _name_ == "_main_":
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'SPY']  
    
    start_date = '2015-01-01'
    end_date = '2023-01-01'
    
    n_states = 4
    compare_instruments(tickers, start_date, end_date, n_states)