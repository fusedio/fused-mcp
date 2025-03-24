import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def udf(
    lat: float=37.7749, 
    lon: float=-122.4194,
    buffer_amount: float = 100,
):  
    """
    Returning min / max / std for any collection on the Microsoft Planetary Computer
    Defaults to using 'cop-dem-glo-30', i.e. Copernicus 30m Digital Elevation Model, with worldwide coverage

    We use lat / lon / buffer_amount rather than `bounds` because it's easier for Claude to make a HTTP request with these than with `fused.types.Bounds` for now

    Arguments:
        lat
        lon
        buffer_amount: in meters, how much to buffer around the lat / lon point
    """
    import odc.stac
    import planetary_computer
    import pystac_client
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point
    from pystac.extensions.eo import EOExtension as eo

    # Hard coding the colleciton in here for now so Claude doesn't get confused
    # TODO: Create another UDF that gives Claude access to all MPC collections, then can query any collection
    collections = ["cop-dem-glo-30"]

    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    common = fused.load("https://github.com/fusedio/udfs/tree/5dda36c/public/common/").utils

    gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")

    # Project to a local UTM projection for accurate buffering in meters
    # Get UTM zone from longitude
    utm_zone = int(((lon + 180) / 6) % 60) + 1
    hemisphere = 'north' if lat >= 0 else 'south'
    utm_crs = f"+proj=utm +zone={utm_zone} +{hemisphere} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"

    gdf_utm = gdf.to_crs(utm_crs)
    gdf_utm['geometry'] = gdf_utm.buffer(buffer_amount)
    gdf_buffered = gdf_utm.to_crs("EPSG:4326")
    bounds = gdf_buffered.total_bounds

    items = catalog.search(
        collections=collections,
        bbox=bounds,
    ).item_collection()

    # Capping resolution to min 10m, the native Sentinel pixel size
    estimated_z = common.estimate_zoom(list(bounds))
    resolution = int(10 * 2 ** max(0, (15 - estimated_z)))
    print(f"{resolution=}")

    if len(items) < 1:
        print(f'No items found. Please either zoom out or move to a different area')
    else:
        print(f"Returned {len(items)} Items")

        ds = odc.stac.load(
                items,
                crs="EPSG:3857",
                resolution=resolution,
                bbox=bounds,
            ).astype(float)

        data = ds['data']

        height_stats = pd.DataFrame({
            "min": [float(np.array(data[0,:,:].min()))],
            "max": [float(np.array(data[0,:,:].max()))],
            "std": [float(np.array(data[0,:,:].std()))],
        })

        print(f"{height_stats=}")
        return height_stats