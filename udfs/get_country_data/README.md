
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_get_country_data import get_country_data

# Instantiate individual jobs
job_get_country_data = get_country_data(filter_type='all')

# Instantiate multi-step job
job = fused.experimental.job([job_get_country_data])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
