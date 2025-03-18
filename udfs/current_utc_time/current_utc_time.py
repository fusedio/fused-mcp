import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf(cache_max_age='0s')
def udf():
    """Simply return the current time in UTC"""
    import time
    import pandas as pd
    from datetime import datetime
    return pd.DataFrame({'current_utc_time': [datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')]})