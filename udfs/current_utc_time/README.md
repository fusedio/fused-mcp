
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from current_utc_time import current_utc_time

# Instantiate individual jobs
job_current_utc_time = current_utc_time()

# Instantiate multi-step job
job = fused.experimental.job([job_current_utc_time])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
