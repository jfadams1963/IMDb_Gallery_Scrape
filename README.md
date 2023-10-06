# IMDb_Gallery_Scrape
A tool for downloading images from IMDb galleries based on scrapeIMDB_gallery by IvRogoz

 This is modified from https://github.com/IvRogoz
 (License ??)
 The bulk of this code is due to a lot work on the part of
 IvRogoz (where ever you are!). I and anyone who uses this code
 owes IvRogoz a big thanks.

 I wish IvRogoz had included a license statement so that I could
 honor it as I pass this work on. My personal choice is the
 2-clause BSD license. If I can ever get in touch whith IvRogoz, I
 will ask them about it. In the mean time, this work is released
 for use free of charge or any encumberences. There are no statements
 of fitness for use, etc., etc. It comes with no warranties, etc.,
 etc. Use it at your own risk and do what ever you will with it.
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
