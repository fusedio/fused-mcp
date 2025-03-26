import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def creating_urls_udf(kind: str = "data"):
    """This UDF simply creates the URL to return a hosted version of a UDF output"""

    import pandas as pd

    # This UDF only currently supports "data" or "pydeck"
    # base_url = "https://staging.fused.io/server/v1/realtime-shared/fsh_6VwcmRjcNdEKqjAg6W6EHS/run/file?dtype_out_raster=png&dtype_out_vector=parquet&output_format"

    # Using Sina's Dynamic Output UDF
    base_url = "https://staging.fused.io/server/v1/realtime-shared/fsh_3Vg20TunmRFmUMSVDnJIvp/run/file?dtype_out_raster=png&dtype_out_vector=parquet&kind"
    base_url += f"={kind}"

    print(f"{base_url=}")
    return pd.DataFrame({"url": [base_url]})