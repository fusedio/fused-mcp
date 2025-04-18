
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_visitors_purpose import visitors_purpose

# Instantiate individual jobs
job_visitors_purpose = visitors_purpose(year=None, country=None)

# Instantiate multi-step job
job = fused.experimental.job([job_visitors_purpose])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
