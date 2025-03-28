import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def udf(filter_type: str = "all"):
    """
    Fetches country data from REST Countries API.

    Parameters:
    filter_type (str): Type of filter to apply. Options:
                       - "all": Fetch all countries (default)
                       - "region": Fetch countries by specific region
                       - "language": Fetch countries by specific language

    Returns:
    pandas.DataFrame: DataFrame containing country information with columns:
                      name, capital, region, population, languages, etc.
    """
    import fused
    import pandas as pd
    import requests
    from datetime import datetime
    # Validate input
    valid_filter_types = ["all", "region", "language"]
    if filter_type not in valid_filter_types:
        raise ValueError(f'Invalid filter_type. Must be one of {valid_filter_types}')

    try:
        # Fetch country data
        if filter_type == "all":
            response = requests.get("https://restcountries.com/v3.1/all")
        else:
            # Placeholder for more specific filtering
            # In a real implementation, you'd add parameters for region or language
            raise NotImplementedError("Specific filtering not implemented in this version")

        # Check if request was successful
        response.raise_for_status()
        countries_data = response.json()

        # Process the data
        processed_countries = []
        for country in countries_data:
            try:
                # Extract relevant information
                processed_country = {
                    "name": country.get("name", {}).get("common", "N/A"),
                    "official_name": country.get("name", {}).get("official", "N/A"),
                    "region": country.get("region", "N/A"),
                    "subregion": country.get("subregion", "N/A"),
                    "population": country.get("population", 0),
                    "capital": country.get("capital", ["N/A"])[0],
                    "languages": ", ".join(country.get("languages", {}).values()) if country.get("languages") else "N/A",
                    "currency": ", ".join([cur for cur in country.get("currencies", {}).keys()]) if country.get("currencies") else "N/A",
                    "independent": country.get("independent", False)
                }
                processed_countries.append(processed_country)
            except Exception as e:
                print(f"Error processing country: {e}")

        # Convert to DataFrame
        df = pd.DataFrame(processed_countries)

        # Add a timestamp for when the data was fetched
        df["fetched_at"] = datetime.now()

        # Print the DataFrame for logging
        print(f"{df=}")

        return df

    except requests.RequestException as e:
        print(f"Error fetching country data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error