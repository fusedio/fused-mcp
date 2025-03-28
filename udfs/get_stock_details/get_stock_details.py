import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def udf(
    symbol: str = "AAPL",  # Default to Apple stock if no symbol provided
    data_type: str = "quote", 
    time_range: str = "today"
):
    """
    Fetches stock data from Finnhub API for a given stock symbol.

    Parameters:
    -----------
    symbol : str, optional (default='AAPL')
        Stock symbol (e.g., 'AAPL' for Apple, 'GOOGL' for Google)
        Defaults to Apple (AAPL) if no symbol is provided
    data_type : str, optional (default='quote')
        Type of stock data to retrieve. Options:
        - 'quote': Current stock quote information
        - 'profile': Company profile and basic information
        - 'news': Recent news about the company
        - 'financials': Financial statements
        Defaults to 'quote' if not specified
    time_range : str, optional (default='today')
        Time range for specific data types (where applicable):
        - 'today': Data for current day
        - 'week': Data for past week
        - 'month': Data for past month
        - 'year': Data for past year
        Defaults to 'today' if not specified

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing requested stock information

    Raises:
    -------
    ValueError
        If invalid data_type or time_range is provided
    """
    import fused
    import pandas as pd
    import requests
    from datetime import datetime, timedelta

    # You would replace this with an actual Finnhub API key
    API_KEY = "cvij5p1r01qks9qar9ngcvij5p1r01qks9qar9o0"  # Note: In real implementation, use secure key management

    # Validate inputs with more lenient parsing
    valid_data_types = ["quote", "profile", "news", "financials"]
    valid_time_ranges = ["today", "week", "month", "year"]

    # Convert inputs to lowercase for case-insensitive matching
    data_type = data_type.lower()
    time_range = time_range.lower()

    if data_type not in valid_data_types:
        raise ValueError(f"Invalid data_type. Must be one of {valid_data_types}")

    if time_range not in valid_time_ranges:
        raise ValueError(f"Invalid time_range. Must be one of {valid_time_ranges}")

    # Base Finnhub API URL
    base_url = "https://finnhub.io/api/v1"

    # Prepare results DataFrame
    results = []

    try:
        if data_type == "quote":
            # Fetch current stock quote
            response = requests.get(
                f"{base_url}/quote",
                params={
                    "symbol": symbol.upper(),
                    "token": API_KEY
                }
            )
            quote_data = response.json()

            # Prepare quote data
            results.append({
                "symbol": symbol.upper(),
                "current_price": quote_data.get("c", None),
                "previous_close": quote_data.get("pc", None),
                "open_price": quote_data.get("o", None),
                "high_price": quote_data.get("h", None),
                "low_price": quote_data.get("l", None),
                "fetched_at": datetime.now()
            })

        elif data_type == "profile":
            # Fetch company profile
            response = requests.get(
                f"{base_url}/stock/profile2",
                params={
                    "symbol": symbol.upper(),
                    "token": API_KEY
                }
            )
            profile_data = response.json()

            # Prepare profile data
            results.append({
                "symbol": symbol.upper(),
                "company_name": profile_data.get("name", None),
                "industry": profile_data.get("industry", None),
                "market_cap": profile_data.get("marketCapitalization", None),
                "country": profile_data.get("country", None),
                "ipo_date": profile_data.get("ipo", None),
                "fetched_at": datetime.now()
            })

        elif data_type == "news":
            # Calculate date range based on time_range
            end_date = datetime.now()
            if time_range == "week":
                start_date = end_date - timedelta(days=7)
            elif time_range == "month":
                start_date = end_date - timedelta(days=30)
            elif time_range == "year":
                start_date = end_date - timedelta(days=365)
            else:  # today
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # Fetch news
            response = requests.get(
                f"{base_url}/company-news",
                params={
                    "symbol": symbol.upper(),
                    "from": start_date.strftime("%Y-%m-%d"),
                    "to": end_date.strftime("%Y-%m-%d"),
                    "token": API_KEY
                }
            )
            news_data = response.json()

            # Prepare news data
            for article in news_data[:10]:  # Limit to 10 most recent articles
                results.append({
                    "symbol": symbol.upper(),
                    "headline": article.get("headline", None),
                    "summary": article.get("summary", None),
                    "url": article.get("url", None),
                    "published_at": datetime.fromtimestamp(article.get("datetime", 0)) if article.get("datetime") else None,
                    "source": article.get("source", None)
                })

        elif data_type == "financials":
            # Fetch income statement
            response = requests.get(
                f"{base_url}/stock/financials",
                params={
                    "symbol": symbol.upper(),
                    "statement": "ic",  # Income Statement
                    "freq": "annual",
                    "token": API_KEY
                }
            )
            financials_data = response.json()

            # Prepare financials data
            if financials_data.get("financials"):
                for financial_entry in financials_data["financials"][:5]:  # Last 5 years
                    results.append({
                        "symbol": symbol.upper(),
                        "year": financial_entry.get("year", None),
                        "total_revenue": financial_entry.get("totalRevenue", None),
                        "net_income": financial_entry.get("netIncome", None),
                        "operating_income": financial_entry.get("operatingIncome", None),
                        "fetched_at": datetime.now()
                    })

        # Convert results to DataFrame
        df = pd.DataFrame(results)

        print(f"{df=}")
        return df

    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error