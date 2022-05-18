import requests
import json
import csv
import sys
import time
import yaml


# load config from yaml
with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
start, end = cfg['start'], cfg['end']

def extract_data(jsonData : dict) -> list:
    # Extracting data from json file
        jsonData = jsonData['data']
        dataLabel = ['mal_id','title','type','source','episodes','status',
                     'duration','rating','score','scored_by','rank','popularity',
                     'members','favorites','season','year']
        animeID,title,type,source,episodes,status,duration,rating,score,scored_by,rank,popularity,members,favorites,season,year = [jsonData[i] for i in dataLabel]
        producers = []
        for j in range(0, len(jsonData['producers'])):
                    producers.append(jsonData['producers'][j]['name'])
        studios = []
        for j in range(0, len(jsonData['studios'])):
                    studios.append(jsonData['studios'][j]['name'])
        genres = []
        for j in range(0, len(jsonData['genres'])):
                    genres.append(jsonData['genres'][j]['name'])
        themes = []
        for j in range(0, len(jsonData['themes'])):
                    themes.append(jsonData['themes'][j]['name'])
        # append all into a list
        return [animeID, title, type, source, episodes, status, duration, rating, score, scored_by, rank, popularity, members, favorites, season, year, producers, studios, genres, themes]

with open(cfg['output'], 'w', newline='') as csvfile:
            # ID, title, type, source, episodes, status, duration, rating, score, scored_by, rank, popularity, members, favorites, season, year, producers, studios, genres, themes
            csvfile.write('ID, title, type, source, episodes, status, duration, rating, score, scored_by, rank, popularity, members, favorites, season, year, producers, studios, genres, themes\n')
for i in range(start,end):
        # Jikan REST API call method:
        # https://api.jikan.moe/v4/anime/{id}
        # for more info about Jikan API visit:
        # https://docs.api.jikan.moe/
        apiUrl = 'http://api.jikan.moe/v4/anime/' + str(i)
        page = requests.get(apiUrl)
        # HTTP Responses
        # 200: OK
        # 400: Bad Request
        # 404: Not Found
        # 429: Too Many Request
        # 500: Internal Server Error
        
        # Rate limited by Jikan API
        while page.status_code == 429:
            # Jikan API rate limit is 60 requests per minute, 3 requests per second
            # Code 429 is usually returned when the rate limit is reached
            # We can wait for 1 second to avoid rate limit, here we wait for 2 seconds.
            print('Error {} occured while scraping anime ID {}, retrying...'.format(page.status_code,i))
            # retry after 2 seconds
            time.sleep(2)
            page = requests.get(apiUrl)
        # Data is not found
        if (page.status_code == 404):
            print('Error {} occured while scraping anime ID {}, skipping.'.format(page.status_code,i))
            # Skip this anime
            continue
            
        # Successful response
        if(page.status_code == 200):
            #print(page.status_code)
            #print('We are in the matrix now.')
            while True:
                try:
                    c = page.content
                    break
                except:
                    print("Unexpected error: ", sys.exc_info()[0])
                    time.sleep(1)
            # Load JSON
            c = page.content
            jsonData = json.loads(c)
            try:
                # catch 404 in json
                jsonData['data']
            except:
                print('Error 404 occured while scraping anime ID {}, skipping.'.format(i))
                continue
            # Get data from JSON
            data = extract_data(jsonData)
            data = [data]
            
            # Write data to CSV
            with open(cfg['output'], 'a', newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
            print('Successfully scraped anime ID {}'.format(i))

