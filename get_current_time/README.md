
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_get_current_time import get_current_time

# Instantiate individual jobs
job_get_current_time = get_current_time()

# Instantiate multi-step job
job = fused.experimental.job([job_get_current_time])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
