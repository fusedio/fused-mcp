
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_hundred_parks_in_vancouver import hundred_parks_in_vancouver

# Instantiate individual jobs
job_hundred_parks_in_vancouver = hundred_parks_in_vancouver()

# Instantiate multi-step job
job = fused.experimental.job([job_hundred_parks_in_vancouver])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
