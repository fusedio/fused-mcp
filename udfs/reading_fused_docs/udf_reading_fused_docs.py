@fused.udf
def udf(input_query: str = ''):
    # input_query is just a dumb empty arg so Claude can have an arg to pass. Always leave as ''
    import pandas as pd
    import requests
    
    response = requests.get("https://docs.fused.io/llms.txt")
    response.raise_for_status() 
    
    return pd.DataFrame({'docs': [response.text]})
