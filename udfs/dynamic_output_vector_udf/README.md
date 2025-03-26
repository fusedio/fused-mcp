
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_dynamic_output_vector_udf import dynamic_output_vector_udf

# Instantiate individual jobs
job_dynamic_output_vector_udf = dynamic_output_vector_udf(kind='data')

# Instantiate multi-step job
job = fused.experimental.job([job_dynamic_output_vector_udf])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
