# IMDb_Gallery_Scrape
A tool for downloading images from IMDb galleries based on scrapeIMDB_gallery by IvRogoz

 This is modified from https://github.com/IvRogoz
 
 The bulk of this code is due to a lot work on the part of
 IvRogoz. I and anyone who uses this code
 owes IvRogoz a big thanks.

 This work is released under the BSD 2-clause License. Use it at your own risk,
 and do what ever you will with it.
 It's certainly not perfect, and could use a little work...
 
 Modified  Sep/Oct 2023 by https://github.com/jfadams1963:
 + Made changes to reflect the new structure on IMDb.
 + Added Cinemagoer functionality.
 + Modifed requests to go through a scraper proxy to keep IMDb happy.
   ->Get a free API key at https://scrapeops.io/
 + Using SoupStrainer for more efficient html parsing.
 + Using settings for API_KEY (optional)
 + Usage:
   
    imdb_gallery_scrape.py movie <title|movieID>

    imdb_gallery_scrape.py actor|person <name|personID>
