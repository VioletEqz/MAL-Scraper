
## What is this about?
This is a Scraper that utilize Jikan API to crawl data from [MyAnimeList](https://myanimelist.net/). It serves as an introductory and educational tool for deeper analysis of the trends among the anime community.

## Explanation
As there have been lots of anime released since the first one was registered in MAL DB, it's highly recommended one utilize multi-thread approach to scrape such big data cluster. Whilst our scraper currently doesn't use the forementioned approach, it's however, multi-thread-compatible. We have also introduced a version where one can easily deploy to non-paid Cloud Application Platform such as Heroku, which will be directly linked to a Google Spreadsheet through OAuth2 with some uses of open-sourced APIs.

As for how the scraper works, it's highly recommended that one went through [JikanV4](https://docs.api.jikan.moe/) docs firsthand as it heavily rely on it. 
## Pre-scraped Data
As for those that are short on time or want to have a preview on the data, we have published Spreadsheet for those interested.
| Date |  Data |
|--|--|
| 28/05/2022 | [Spreadsheet](https://docs.google.com/spreadsheets/d/1Jltxga8HA-umRwDb2RUchbAypcDCcYs4qHg8hu0U_gM/edit?usp=sharing) |

## How to use
Example:
Start scraping a new.
```py
py src/scraping.py
```
Resuming scraping from id 100.
```py
py src/scraping.py --start 100 --resume
```
## Reference
[JikanV4](https://docs.api.jikan.moe/) which this scraper heavily relied on.

[Google OAuth2](https://developers.google.com/identity/protocols/oauth2) as the web-server authentication protocol we used.

[Google API](https://github.com/googleapis/google-auth-library-python) for server-to-server authentication mechanisms to Google API.

[Gspread](https://github.com/burnash/gspread) for a simple automatable way to access and edit Spreadsheet from server-side.

