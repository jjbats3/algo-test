import yfinance as yf

# Define a list of tickers you're interested in screening
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Define your financial health criteria thresholds
criteria = {
    'ROE': 0.15,  # Return on Equity > 15%
    'ROA': 0.05,  # Return on Assets > 5%
    'CurrentRatio': 1.5,
    'QuickRatio': 1,
    'DebtToEquity': 1.0  # Debt-to-Equity < 1.0
}

# Function to fetch and filter stocks based on criteria
def screen_stocks(tickers, criteria):
    filtered_stocks = []
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        fin_stats = stock.quarterly_financials.transpose().mean()  # Average of the last 4 quarters
        balance_sheet = stock.quarterly_balance_sheet.transpose().mean()
        
        # Calculate metrics
        roe = fin_stats['Net Income'] / balance_sheet['Total Stockholder Equity']
        roa = fin_stats['Net Income'] / balance_sheet['Total Assets']
        current_ratio = balance_sheet['Total Current Assets'] / balance_sheet['Total Current Liabilities']
        quick_ratio = (balance_sheet['Total Current Assets'] - balance_sheet['Inventory']) / balance_sheet['Total Current Liabilities']
        debt_to_equity = balance_sheet['Long Term Debt'] / balance_sheet['Total Stockholder Equity']
        
        # Check if stock meets all criteria
        if roe > criteria['ROE'] and roa > criteria['ROA'] and current_ratio > criteria['CurrentRatio'] and quick_ratio > criteria['QuickRatio'] and debt_to_equity < criteria['DebtToEquity']:
            filtered_stocks.append(ticker)
    
    return filtered_stocks

# Screen the stocks
filtered_stocks = screen_stocks(tickers, criteria)
print("Filtered Stocks:", filtered_stocks)
