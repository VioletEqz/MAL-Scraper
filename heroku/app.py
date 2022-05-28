import requests
import json
import csv
import sys
import time
import yaml

import gspread
import json
from google.oauth2 import service_account

# load config from yaml
with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
start, end = cfg['start'], cfg['end']

# Specify scopes for OAUth2
scope = [
    'https://spreadsheets.google.com/feeds', 
    'https://www.googleapis.com/auth/drive'
    ]

# Read JSON cred
with open('client_secret.json') as f:
    json_cred = json.load(f)
    credentials = service_account.Credentials.from_service_account_info(
        json_cred)

scoped_credentials = credentials.with_scopes(scope)

# Connect to Google Sheet API
client = gspread.authorize(scoped_credentials)
sheet = client.open('CrawledAnimeList').sheet1

def extract_data(jsonData : dict) -> list:
    # Extracting data from json file
        jsonData = jsonData['data']
        dataLabel = ['mal_id','title','type','source','episodes','status',
                     'duration','rating','score','scored_by','rank','popularity',
                     'members','favorites','season','year']
        animeID,title,type,source,episodes,status,duration,rating,score,scored_by,rank,popularity,members,favorites,season,year = [jsonData[i] for i in dataLabel]
        producerList = []
        for j in range(0, len(jsonData['producers'])):
                    producerList.append(jsonData['producers'][j]['name'])
        studioList = []
        for j in range(0, len(jsonData['studios'])):
                    studioList.append(jsonData['studios'][j]['name'])
        genreList = []
        for j in range(0, len(jsonData['genres'])):
                    genreList.append(jsonData['genres'][j]['name'])
        themeList = []
        for j in range(0, len(jsonData['themes'])):
                    themeList.append(jsonData['themes'][j]['name'])
        # Return after appending to a list
        return [
            animeID, title, type, source,
            episodes, status, duration, rating,
            score, scored_by, rank, popularity,
            members, favorites, season, year,
            ', '.join(producerList),
            ', '.join(studioList),
            ', '.join(genreList),
            ', '.join(themeList)]

# Create first row
row = 'ID, title, type, source,\
    episodes, status, duration, rating,\
    score, scored_by, rank, popularity,\
    members, favorites, season, year,\
    producers, studios, genres, themes'.split(', ')
row = [x.strip() for x in row]
sheet.update('A1:T1', [row])

# Start writing data after the first row (A2)
row_count = 2

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
            
            # Write data to sheet
            sheet.update('A'+str(row_count)+':T'+str(row_count), data)
            row_count += 1

            # Report to console
            print('Successfully scraped anime ID {}'.format(i))

