
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_internet_speeds_for_lat_lon import internet_speeds_for_lat_lon

# Instantiate individual jobs
job_internet_speeds_for_lat_lon = internet_speeds_for_lat_lon(lon, bounds=None, lat=37.7749)

# Instantiate multi-step job
job = fused.experimental.job([job_internet_speeds_for_lat_lon])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
