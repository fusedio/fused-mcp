import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def community_gardens_vancouver():
    import requests
    import geopandas as gpd
    from shapely.geometry import shape

    params = {
        "limit": -1, # setting to max of amount of request we can do
    }

    url = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/community-gardens-and-food-trees/records"
    r = requests.get(url, params=params)

    gdf = gpd.GeoDataFrame(r.json()["results"])
    gdf["geometry"] = gdf["geom"].apply(lambda x: shape(x["geometry"]))
    gdf = gdf.set_geometry("geometry")
    del gdf["geom"]

    print(f"{gdf.shape=}")



    return gdf