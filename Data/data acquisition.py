import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import numpy as np

def get_revenue_growth(ticker_obj):
    """Revenue Growth"""
    try:
        financials = ticker_obj.financials
        if financials is not None and not financials.empty and 'Total Revenue' in financials.index:
            revenues = financials.loc['Total Revenue'].sort_index()
            if len(revenues) >= 2:
                latest = revenues.iloc[-1]
                previous = revenues.iloc[-2]
                if previous != 0 and not pd.isna(previous) and not pd.isna(latest):
                    growth = ((latest - previous) / abs(previous)) * 100
                    return round(growth, 2)
        return None
    except:
        return None

def get_ebitda_margin(ticker_obj):
    """EBITDA Margin"""
    try:
        info = ticker_obj.info
        ebitda = info.get('ebitda', None)
        revenue = info.get('totalRevenue', None)
        if ebitda and revenue and revenue != 0:
            margin = (ebitda / revenue) * 100
            return round(margin, 2)
        return None
    except:
        return None

def get_stock_price_at_date(ticker_obj, target_date='2024-12-31'):
    """Stock Price around end of 2024"""
    try:
        hist = ticker_obj.history(start='2024-12-20', end='2025-01-10')
        
        if not hist.empty:
            return round(hist['Close'].iloc[-1], 2)
        return None
    except:
        return None

def get_beta(ticker_obj):
    """Beta value"""
    try:
        info = ticker_obj.info
        beta = info.get('beta', None)
        if beta:
            return round(beta, 3)
        return None
    except:
        return None
    
def volatility(ticker_obj):
    """Annualized Volatility based on daily returns"""
    try:
        hist = ticker.history(start="2024-01-01", end="2024-12-31")['Close']
        if not hist.empty:
            daily_returns = hist.pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252)  # Assuming 252 trading days
            return round(volatility, 2)
        return None
    except:
        return None

def get_comprehensive_data(ticker_symbol, target_date='2024-12-31'):
    """
    get ESG scores and key financial metrics for a given ticker.
    target_date: '2024-12-31'
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # === 1. company info ===
        company_name = info.get('longName', 'N/A')
        currency = info.get('currency', 'N/A')
        industry = info.get('industry', 'N/A')
        sector = info.get('sector', 'N/A')
        country = info.get('country', 'N/A')
        
        # === 2. ESG ===
        esg_scores = ticker.sustainability
        if esg_scores is not None and not esg_scores.empty:
            total_esg = esg_scores.loc['totalEsg'].values[0] if 'totalEsg' in esg_scores.index else None
            env_score = esg_scores.loc['environmentScore'].values[0] if 'environmentScore' in esg_scores.index else None
            social_score = esg_scores.loc['socialScore'].values[0] if 'socialScore' in esg_scores.index else None
            gov_score = esg_scores.loc['governanceScore'].values[0] if 'governanceScore' in esg_scores.index else None
            esg_performance = esg_scores.loc['esgPerformance'].values[0] if 'esgPerformance' in esg_scores.index else None
            highest_controversy = esg_scores.loc['highestControversy'].values[0] if 'highestControversy' in esg_scores.index else None
        else:
            total_esg = env_score = social_score = gov_score = esg_performance = highest_controversy = None
        
        # === 3. stock price ===
        stock_price = get_stock_price_at_date(ticker, target_date)
        current_price = info.get('currentPrice', None) or info.get('regularMarketPrice', None)
        
        # === 4. key financial indicators ===
        
        # valuation & size
        market_cap = info.get('marketCap', None)
        pe_ratio = info.get('trailingPE', None)
        pb_ratio = info.get('priceToBook', None)
        annual_return = info.get('52WeekChange', None)
        
        # profitibility
        revenue = info.get('totalRevenue', None)
        net_income = info.get('netIncomeToCommon', None)
        operating_margin = info.get('operatingMargins', None)
        gross_margin = info.get('grossMargins', None)
        roe = info.get('returnOnEquity', None)
        roa = info.get('returnOnAssets', None)
        profit_margin = info.get('profitMargins', None)
        ebitda_margin = get_ebitda_margin(ticker)
        eps = info.get('trailingEps', None)
        
        # risk/stability
        beta = get_beta(ticker)
        debt_to_equity = info.get('debtToEquity', None)
        current_ratio = info.get('currentRatio', None)
        cash_flow = info.get('operatingCashflow', None)
        
        # growth
        revenue_growth = get_revenue_growth(ticker)
        
        # convert ratios to percentages where applicable
        if operating_margin: operating_margin = round(operating_margin * 100, 2)
        if gross_margin: gross_margin = round(gross_margin * 100, 2)
        if roe: roe = round(roe * 100, 2)
        if roa: roa = round(roa * 100, 2)
        if profit_margin: profit_margin = round(profit_margin * 100, 2)
        if pe_ratio: pe_ratio = round(pe_ratio, 2)
        if pb_ratio: pb_ratio = round(pb_ratio, 2)
        if eps: eps = round(eps, 2)
        if current_ratio: current_ratio = round(current_ratio, 2)
        if debt_to_equity: debt_to_equity = round(debt_to_equity, 2)
        if annual_return: annual_return = round(annual_return * 100, 2)
        
        # build result dict
        result = {
            # basic info
            'Ticker': ticker_symbol,
            'Company_Name': company_name,
            'Currency': currency,
            'Data_Date': target_date,
            'Industry': industry,
            'Sector': sector,
            'Country': country,
            
            # ESG
            'Total_ESG_Score': total_esg,
            'Environmental_Score': env_score,
            'Social_Score': social_score,
            'Governance_Score': gov_score,
            'ESG_Performance': esg_performance,
            'Highest_Controversy': highest_controversy,
            
            # Stock Price
            'Stock_Price': stock_price,
            'Current_Price': current_price,
            
            # valuation & size
            'Market_Cap': market_cap,
            'PE_Ratio': pe_ratio,
            'PB_Ratio': pb_ratio,
            'Annual_Return_Pct': annual_return,
            
            # profitibility (%)
            'Revenue': revenue,
            'Net_Income': net_income,
            'Operating_Margin_Pct': operating_margin,
            'Gross_Margin_Pct': gross_margin,
            'ROE_Pct': roe,
            'ROA_Pct': roa,
            'Profit_Margin_Pct': profit_margin,
            'EBITDA_Margin_Pct': ebitda_margin,
            'EPS': eps,
            
            # risk/stability
            'Beta': beta,
            'Debt_to_Equity': debt_to_equity,
            'Current_Ratio': current_ratio,
            'Operating_Cash_Flow': cash_flow,
            
            # Growth (%)
            'Revenue_Growth_Pct': revenue_growth,
            
            # Status
            'Status': 'Success'
        }
        
        return result
        
    except Exception as e:
        return {
            'Ticker': ticker_symbol,
            'Company_Name': 'Error',
            'Currency': None,
            'Data_Date': target_date,
            'Industry': None,
            'Sector': None,
            'Country': None,
            'Total_ESG_Score': None,
            'Environmental_Score': None,
            'Social_Score': None,
            'Governance_Score': None,
            'ESG_Performance': None,
            'Highest_Controversy': None,
            'Stock_Price': None,
            'Current_Price': None,
            'Revenue': None,
            'Net_Income': None,
            'Operating_Margin_Pct': None,
            'Gross_Margin_Pct': None,
            'ROE_Pct': None,
            'ROA_Pct': None,
            'Profit_Margin_Pct': None,
            'EBITDA_Margin_Pct': None,
            'EPS': None,
            'Market_Cap': None,
            'PE_Ratio': None,
            'PB_Ratio': None,
            'Annual_Return_Pct': None,
            'Beta': None,
            'Debt_to_Equity': None,
            'Current_Ratio': None,
            'Operating_Cash_Flow': None,
            'Revenue_Growth_Pct': None,
            'Status': f'Error: {str(e)}'
        }

def read_tickers_from_file(filename):
    """read ticker symbols from a text file, ignoring comments and empty lines"""
    tickers = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    tickers.append(line)
        return tickers
    except FileNotFoundError:
        print(f"Error: File not found '{filename}'")
        return []
    except Exception as e:
        print(f"Error when reading the file: {e}")
        return []

def main():
    # === parameters ===
    input_file = 'Company List/swiss_companies.txt'
    target_date = '2024-12-31'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'esg_financial_analysis_{target_date.replace("-", "")}_{timestamp}.csv'
    
    # reading tickers
    print(f"\nReading input file: {input_file}")
    tickers = read_tickers_from_file(input_file)
    
    if not tickers:
        print("No valid ticker symbols found. Please check the input file.")
        return
    
    print(f"Successfully read {len(tickers)} tickers.")
    print("-" * 90)
    
    # store all results
    all_data = []
    
    # iterate through each ticker
    for i, ticker in enumerate(tickers, 1):
        print(f"\n[{i}/{len(tickers)}] Processing {ticker}...")
        
        # get comprehensive data
        result = get_comprehensive_data(ticker, target_date)
        all_data.append(result)
        
        # show brief result
        if result['Status'] == 'Success':
            print(f"  ✓ {result['Company_Name']}")
            print(f"    Total ESG Score: {result['Total_ESG_Score']} (E:{result['Environmental_Score']}, S:{result['Social_Score']}, G:{result['Governance_Score']})")
            print(f"    Stock Price: {result['Stock_Price']} {result['Currency']}")
            print(f"    Market Cap: {result['Market_Cap']:,.0f}" if result['Market_Cap'] else "    Market Cap: N/A")
            print(f"    ROE: {result['ROE_Pct']}% | Beta: {result['Beta']}")
        else:
            print(f"  ✗ {result['Status']}")
        
        # delay to avoid too many requests at once
        if i < len(tickers):
            time.sleep(1.5)
    
    # convert into DataFrame
    df = pd.DataFrame(all_data)
    
    # save as CSV
    print("\n" + "=" * 90)
    print(f"Saving data to: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # statistics
    print("-" * 90)
    print("Data collection completed!")
    print(f"Total companies: {len(tickers)}")
    print(f"Successful: {len(df[df['Status'] == 'Success'])}")
    print(f"Failed: {len(df[df['Status'] != 'Success'])}")
    
    # data quality checks
    print("\nData completeness check:")
    esg_complete = len(df[df['Total_ESG_Score'].notna()])
    price_complete = len(df[df['Stock_Price'].notna()])
    roe_complete = len(df[df['ROE_Pct'].notna()])
    beta_complete = len(df[df['Beta'].notna()])
    
    print(f"  ESG data complete: {esg_complete}/{len(df)} ({esg_complete/len(df)*100:.1f}%)")
    print(f"  Stock price data complete: {price_complete}/{len(df)} ({price_complete/len(df)*100:.1f}%)")
    print(f"  ROE data complete: {roe_complete}/{len(df)} ({roe_complete/len(df)*100:.1f}%)")
    print(f"  Beta data complete: {beta_complete}/{len(df)} ({beta_complete/len(df)*100:.1f}%)")
    
    print(f"\n✓ Data saved to: {output_file}")
    print("=" * 90)
    
    # preview data
    print("\nData preview (first 5 rows):")
    preview_cols = ['Ticker', 'Company_Name', 'Total_ESG_Score', 'Stock_Price', 
                    'Market_Cap', 'ROE_Pct', 'Beta', 'Status']
    print(df[preview_cols].head().to_string(index=False))

if __name__ == "__main__":
    main()