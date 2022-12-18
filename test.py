import pandas as pd
import json
from pandas import json_normalize
import requests

variables = {
  'username': 'HidekiGQ',
  'type': 'ANIME'
}

url = 'https://graphql.anilist.co'

query = '''
query ($username: String, $type: MediaType) {
MediaListCollection(userName: $username, type: $type) {
    lists {
    name
    entries {
        id
        status
        score(format: POINT_10)
        progress
        notes
        repeat
        media {
        chapters
        volumes
        idMal
        episodes
        title { romaji }
        }
    }
    name
    isCustomList
    isSplitCompletedList
    status
    }
}
}
'''

response = requests.post(url, json={'query': query, 'variables': variables})
jsonData = response.json()
completed_entries = jsonData['data']['MediaListCollection']['lists'][0]['entries']
michael_df = json_normalize(completed_entries)
print(michael_df)
'L bozo cringe'