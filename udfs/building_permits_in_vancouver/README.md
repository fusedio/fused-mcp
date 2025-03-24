
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_building_permits_in_vancouver import building_permits_in_vancouver

# Instantiate individual jobs
job_building_permits_in_vancouver = building_permits_in_vancouver()

# Instantiate multi-step job
job = fused.experimental.job([job_building_permits_in_vancouver])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
