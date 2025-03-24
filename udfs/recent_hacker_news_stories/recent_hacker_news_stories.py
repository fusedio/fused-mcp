import fused
from fused.models.udf import Header
from fused.models import Schema

@fused.udf
def udf(story_type: str = "top"):
    """
    Fetches top posts from Hacker News as a dataframe.

    Parameters:
    story_type (str): Type of stories to fetch. Options are:
                      - "top" for top stories
                      - "newest" for latest stories

    Returns:
    pandas.DataFrame: DataFrame containing HN posts with columns:
                     id, title, url, score, by (author), time, descendants (comments)
    """
    import pandas as pd
    import requests
    import time
    from datetime import datetime

    # Validate input
    if story_type not in ["top", "newest"]:
        raise ValueError('Invalid story_type. Must be "top" or "newest"')

    # Map story_type to the appropriate HN API endpoint
    endpoint_map = {
        "top": "topstories",
        "newest": "newstories"
    }

    endpoint = endpoint_map[story_type]

    # Fetch the list of top or newest story IDs
    response = requests.get(f"https://hacker-news.firebaseio.com/v0/{endpoint}.json")
    story_ids = response.json()

    # Only doing 5 stories for now
    story_ids = story_ids[:5]

    # Fetch details for each story ID
    stories = []
    for story_id in story_ids:
        try:
            # Get the story details
            story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
            story = story_response.json()

            # Skip if not a story or missing key fields
            if not story or story.get('type') != 'story' or 'title' not in story:
                continue

            # Add to our list
            stories.append({
                'id': story.get('id'),
                'title': story.get('title'),
                'url': story.get('url', ''),
                'score': story.get('score', 0),
                'by': story.get('by', ''),
                'time': datetime.fromtimestamp(story.get('time', 0)),
                'descendants': story.get('descendants', 0)
            })

            # Brief pause to avoid overloading the API
            time.sleep(0.1)

        except Exception as e:
            print(f"Error fetching story {story_id}: {e}")

    # Convert the list of stories to a DataFrame
    df = pd.DataFrame(stories)

    # Add a timestamp for when the data was fetched
    df['fetched_at'] = datetime.now()
    print(f"{df=}")

    return df