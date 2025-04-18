import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def visitor_info(year: int = 2024, country: str = None):
    """
    UDF to retrieve visitor arrival information for a given year and optional country.
    Defaults to 2024 if no year is provided. If no country is specified, returns data for all countries.
    """
    import pandas as pd
    import fused
    from io import BytesIO
    import requests

    drive_url = "https://drive.google.com/uc?export=download&id=1QoookSZMXWs3eNQ-q0Bsxq4tCB_KH4ux"

    # @fused.cache
    def load_csv():
        response = requests.get(drive_url)
        response.raise_for_status()
        return pd.read_csv(BytesIO(response.content))

    # Load data
    df = load_csv()

    # Convert 'Year' column to integer type
    df['Year'] = df['Year'].astype(int)

    # Apply year filter
    result = df[df['Year'] == year]

    # Apply country filter if provided, otherwise return all countries
    if country:
        result = result[result['Country'] == country]

    # Return the filtered DataFrame or an empty DataFrame if no data is found
    return result if not result.empty else pd.DataFrame(columns=df.columns)