@fused.udf
def udf(number_public_udfs: int = 100):
    import pandas as pd

    public_udfs = fused.api.get_udfs(whose="public", n=number_public_udfs)
    df = pd.DataFrame()
    names = []
    codes = []
    for name, udf in public_udfs.items():
        names.append(udf.name)
        codes.append(udf.code)

    df["name"] = names
    df["code"] = codes

    print(f"{df=}")
    return df
