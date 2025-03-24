
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_electric_vehicle_chargers_in_vancouver import electric_vehicle_chargers_in_vancouver

# Instantiate individual jobs
job_electric_vehicle_chargers_in_vancouver = electric_vehicle_chargers_in_vancouver()

# Instantiate multi-step job
job = fused.experimental.job([job_electric_vehicle_chargers_in_vancouver])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
