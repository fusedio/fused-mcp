import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def get_visitor_data(year: int = None, country: str = None):
    """
    UDF to retrieve visitor arrival data with optional filters.
    We've simply hosted a CSV file on Google Drive for the sake of simplicity for this example.

    Parameters:
    - year (int): Filter by specific year (e.g., 2023)
    - country (str): Filter by specific country name (e.g., 'Thailand')

    Returns:
    A DataFrame with the following columns:
    - Country
    - Purpose_of_visit_to_Japan
    - Year
    - Growth Rate(%)
    - Visitor Arrivals
    """
    import pandas as pd
    import fused
    from io import BytesIO
    import requests

    drive_url = "https://drive.google.com/uc?export=download&id=1OQkx2fLA6oQ3fzNL-aiCFqDr65bp-nAL"

    @fused.cache
    def load_csv():
        response = requests.get(drive_url)
        response.raise_for_status()
        return pd.read_csv(BytesIO(response.content), encoding='utf-8')

    df = load_csv()
    df.rename(columns={"Country/Area": "Country"}, inplace=True)

    # Cleaning up
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    if year is not None:
        df = df[df['Year'] == year]
    if country:
        df = df[df['Country'] == country]

    # Columns to return
    columns = [
        'Country',
        'Purpose_of_visit_to_Japan',
        'Year',
        'Growth Rate(%)',
        'Visitor Arrivals'
    ]

    return df[columns] if not df.empty else pd.DataFrame(columns=columns)