
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_yearly_crime_amount import yearly_crime_amount

# Instantiate individual jobs
job_yearly_crime_amount = yearly_crime_amount(lon, up_to_year=2021, lat=49.2806, buffer_amount=1000)

# Instantiate multi-step job
job = fused.experimental.job([job_yearly_crime_amount])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
