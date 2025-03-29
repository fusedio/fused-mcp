
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_get_stock_details import get_stock_details

# Instantiate individual jobs
job_get_stock_details = get_stock_details(symbol='AAPL', data_type='quote', time_range='today')

# Instantiate multi-step job
job = fused.experimental.job([job_get_stock_details])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
