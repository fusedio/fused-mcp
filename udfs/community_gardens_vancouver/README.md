
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_community_gardens_vancouver import community_gardens_vancouver

# Instantiate individual jobs
job_community_gardens_vancouver = community_gardens_vancouver()

# Instantiate multi-step job
job = fused.experimental.job([job_community_gardens_vancouver])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
