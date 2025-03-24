
# Fused Multi-Step Job

## Get started
```python
# Import UDFs
from udf_recent_hacker_news_stories import recent_hacker_news_stories

# Instantiate individual jobs
job_recent_hacker_news_stories = recent_hacker_news_stories(story_type='top')

# Instantiate multi-step job
job = fused.experimental.job([job_recent_hacker_news_stories])

# Run locally
job.run_local(file_id=0, chunk_id=0)

# Run remotely
job.run_remote(output_table='output_table_name')
```
