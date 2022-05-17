import requests
import json
import csv
import sys
import time
import argparse
from tqdm import tqdm,trange

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=int, default='1', help='Starting index', required=False)
    parser.add_argument('-e', '--end', type=int, default='50000', help='Ending index', required=False)
    parser.add_argument('-o', '--output', type=str, default='AnimeList.csv', help='Output file name', required=False)
    # Maybe continuation?
    parser.add_argument('-r', '--resume', type=bool, default='False', help='Resuming past progress', required=False)

    return parser.parse_args()




if __name__=="__main__":
    # Get arguments if ran from command line
    opt = get_args()

    # Staging new file for writing 
    if not opt.resume:
        with open(opt.output, 'w', newline='') as csvfile:
            csvfile.write('animeID, name, season, year, genre, type, episodes, studios, source, scored, scoredBy, members\n')

    # Main loop for scraping anime from Jikan API
    # ID start from 1 to 51418 (as of 17/05/2022) for anime
    for i in range(opt.start,opt.end):
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
            print('\nError {} occured while scraping anime ID {}, retrying...'.format(page.status_code,i))
            # retry after 2 seconds
            time.sleep(2)
            apiUrl = 'http://api.jikan.moe/v4/anime/' + str(i)
            page = requests.get(apiUrl)
            
        # Data is not found
        if (page.status_code == 404):
            print('\nError {} occured while scraping anime ID {}, skipping.'.format(page.status_code,i))
            continue
            
        # Successful response
        elif(page.status_code == 200):
            while True:
                try:
                    c = page.content
                    break
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    time.sleep(1)
            # Extracting data from JSON
            # placeholder for data extracting....
            data = 'placeholder'
            with open(opt.output, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
            c = page.content
            jsonFile = json.loads(c)
            print('Successfully scraped anime ID {}'.format(i))

    csvfile.close()

