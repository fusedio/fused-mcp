@fused.udf
def udf(lat_start = 34.0154145, lng_start = -118.2253804, lat_end = 33.9422, lng_end = -118.4036, cost = 'auto'): 
    import time
    import pandas as pd
    import requests
    from utils import decode, compute_distance
    
    #costing options: auto, pedestrian, bicycle, truck, bus, motor_scooter


    start = time.time()
    
    # Get the route directly from Valhalla server
    url = 'https://valhalla1.openstreetmap.de/route'
    params = {
        "locations": [{"lon": lng_start, "lat": lat_start},{"lon": lng_end, "lat": lat_end}]
        ,"costing": cost 
        ,"units":"miles"
    }
    response = requests.post(url, json=params)
    result = response.json()
    
    # Extract driving instructions
    instructions = [el['instruction'] for el in result['trip']['legs'][0]['maneuvers']]
    print('Driving Instructions:', instructions)
    
    # Get the encoded shape and decode it
    encoded_shape = result['trip']['legs'][0]['shape']
    decoded_shape = decode(encoded_shape)
    
    # Create temporary GeoDataFrame to compute distance
    import geopandas as gpd
    from shapely.geometry import LineString
    gdf_route = gpd.GeoDataFrame(columns=['geometry'], geometry=[LineString(decoded_shape)], crs=4326)
    gdf_route = compute_distance(gdf_route, col_name='separation')
    
    # Extract route length
    route_length_km = gdf_route['separation'].values[0] / 1000
    print('time to create route', time.time() - start, 'sec')
    print('route length:', route_length_km, 'km')
    
    # Create a simple DataFrame with the relevant information
    route_info = {
        'start_lat': lat_start,
        'start_lng': lng_start,
        'end_lat': lat_end,
        'end_lng': lng_end,
        'transportation_mode': cost,
        'route_length_km': route_length_km,
        'computation_time_sec': time.time() - start,
        'instructions': instructions
    }
    

    return pd.DataFrame([route_info])