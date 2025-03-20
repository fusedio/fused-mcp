@fused.udf
def udf():
    import pandas as pd
    import requests

    response = requests.get("https://docs.fused.io/llms.txt")
    response.raise_for_status()

    return pd.DataFrame({"docs": [response.text]})
