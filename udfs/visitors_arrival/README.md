
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_visitors_arrival import visitors_arrival

# Instantiate individual jobs
job_visitors_arrival = visitors_arrival(year=2024, country=None)

# Instantiate multi-step job
job = fused.experimental.job([job_visitors_arrival])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
