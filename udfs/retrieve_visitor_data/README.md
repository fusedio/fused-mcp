
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_retrieve_visitor_data import retrieve_visitor_data

# Instantiate individual jobs
job_retrieve_visitor_data = retrieve_visitor_data(year=None, country=None)

# Instantiate multi-step job
job = fused.experimental.job([job_retrieve_visitor_data])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
