
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_elevation_stats import elevation_stats

# Instantiate individual jobs
job_elevation_stats = elevation_stats(lon, lat=37.7749, buffer_amount=100)

# Instantiate multi-step job
job = fused.experimental.job([job_elevation_stats])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
