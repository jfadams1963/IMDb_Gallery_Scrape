#!/usr/bin/env python
# imdb_gallery_scrape.py
"""
 This is modified from https://github.com/IvRogoz
 (License ??)
 The bulk of this code is due to a lot work on the part of
 IvRogoz (where ever you are!). I and anyone who uses this code
 owes IvRogoz a big thanks.

 I wish IvRogoz had included a license statement so that I could
 honor it as I pass this work on. My personal choice is the
 2-clause BSD license. In the mean time, this work is released
 for use free of charge or any encumberences. There are no statements
 of fitness for use, etc., etc. It comes with no warranties, etc.,
 etc. Use it at your own risk and do what ever you will with it.
 It's certainly not perfect, and could use a little work...
 
 Modified  Sep/Oct 2023 by https://github.com/jfadams1963:
 + Made changes to reflect the new structure on IMDb.
 + Added Cinemagoer functionality to specify movie|person by title|name.
 + Modifed requests to go through a scraper proxy to keep IMDb happy.
   ->Get a free API key at https://scrapeops.io/
 + Using SoupStrainer for more efficient html parsing.
 + Using settings for API_KEY (optional)
 + Usage:
     imdb_gallery_scrape.py movie <title|movieID>
     imdb_gallery_scrape.py actor|person <name|personID>

 Some things to tweak/play with:
 + start_page = 0, change this to start on the page you want.
 + paggination = 1, this give you only the first gallery page
   set it as high as you need. One page give you up to 48 images.
"""

import sys
import os
import string
import re
import shutil
import requests
from python_settings import settings
from bs4 import BeautifulSoup, SoupStrainer
from imdb import (Cinemagoer,
                    IMDbError,
                    IMDbDataAccessError)


#### Added by jfadams1963 
arg1 = sys.argv[1]
arg2 = sys.argv[2]
image_num_limit = int(10)
# You will need an APi key from https://scrapeops.io/
# Getting API_KEY via settings. Set it however works best for you. -jfadams1963
API_KEY = settings.SCRAPEOPS_API_KEY
is_person = 0
####

start_page = 0
paggination = 1
mediaview_url = "https://www.imdb.com/"

#### Cineamagoer section to get movieID or personID -jfadams1963
# Set up person|movie options
# Instantiate a Cinemagoer object
# Get a movies|persons object
bad = r'['+string.punctuation+']'
# Strip input of punctuation, set to lower case
# IMDb queries are case insensitive
arg1 = re.sub(bad,'',sys.argv[1]).lower()
arg2 = re.sub(bad,'',sys.argv[2])
# Use ID is initially false
use_id = 0
person_id = 0

if arg2.isnumeric() == True:
    use_id = 1
    person_id = 1

#allow 'actor' for person
if (arg1 == 'actor') or arg1 == ('person'):
    arg1 = 'person'
    is_person = 1

# Instantiate a Cinemagoer object
movie = ''
persons = ''
try:
    ia = Cinemagoer()
    # Set title
    if (use_id == 1) and (is_person == 0):
        title = ia.get_movie(arg2)['title']
        movies = ia.search_movie(title)
        title_words = title.split()
        title_long = title_words[0]
        for w in range(1,4):
            try:
                title_long += '_' + title_words[w]
            except:
                break
    elif (use_id == 0) and (is_person == 0):
        title = arg2
        movies = ia.search_movie(arg2)
        title_words = title.split()
        title_long = title_words[0]
        for w in range(1,10):
            try:
                title_long += '_' + title_words[w]
            except:
                break
    # Set name
    if (use_id == 1) and (is_person == 1):
        nom = ia.get_person(arg2)['name']
        persons = ia.search_person(nom)
        name_words = nom.split()
        name_long = name_words[0]
        for w in range(1,4):
            try:
                name_long += '_' + name_words[w]
            except:
                break
    elif (use_id == 0) and (is_person == 1):
        persons = ia.search_person(arg2)
        name_words = arg2.split()
        name_long = name_words[0]
        for w in range(1,4):
            try:
                name_long += '_' + name_words[w]
            except:
                break
except  (IMDbError, IMDbDataAccessError) as err:
    print(err)
    sys.exit("Exception instantiating Cinemagoer")

# Set folder name to title or actor name
if is_person == 0:
    movie_id = movies[0].movieID
    print('ID',movie_id)
    imdb_ID = 'tt'+str(movie_id)
    folder = str(title_long)
    image_tag = str(title_long)
    base_url = "https://www.imdb.com/title/" + imdb_ID + "/mediaindex/"
elif is_person == 1:
    person_id = persons[0].personID
    imdb_ID = 'nm'+str(person_id)
    folder = str(name_long)
    image_tag = str(name_long)
    base_url = "https://www.imdb.com/name/" + imdb_ID + "/mediaindex/"
#### End Cinemagoer section


# Create directory based on title or name -jfadams1963
if not os.path.exists(folder):
    os.makedirs(folder)

folder = "./" + folder + "/"
print("Created Directory:", folder)

i = 0 # For enumerating individual images -jfadams1963

# x enumerates gallery pages -jfadams1963
for x in range(start_page, paggination):
    if x > 0:
        url =base_url +"?page="+str(x)
    else:
        url = base_url
    print()
    print("Scrapping from:", url)
    
    ## use requests.get().content with scraper proxy -jfadams1963
    htmldata = requests.get(url = 'https://proxy.scrapeops.io/v1/',
                            params = {'api_key': API_KEY,
                            'url': base_url },
               timeout = 20).content
    soup = BeautifulSoup(htmldata, 'html.parser')
    images = soup.find_all(class_='media_index_thumb_list')
    links = images[0].find_all('a')
    
    print("Found:", len(links), "images")
    image_num_limit = int(input('Number of images to download:'))

    if image_num_limit >= len(links):
        print("Will download " + str(len(links)))
    else:
        print("Will download " + str(image_num_limit))

    for index, link in enumerate(links):
        i += 1
        if i > image_num_limit: # Using a limit on number of images. (optional)
            sys.exit(0)
        image_i = link['href']
        # This url gives us the mediaviewer page with image i -jfadams1963
        url = mediaview_url + image_i
        # Use proxy and requests.get().content -jfadams1963
        # This URL will contain the source URL for the large image,
        # so let's grab it and parse it -jfadams1963
        founddata = requests.get(url = 'https://proxy.scrapeops.io/v1/',
                                params = {'api_key': API_KEY,
                                          'url': url, },
                    timeout = 20).content
        # Here we get our large image URL -jfadasm1963
        meta_with_image = SoupStrainer(property="og:image")
        image_source_soup = BeautifulSoup(founddata, 'html.parser', parse_only=meta_with_image)
        image_url = image_source_soup.find('meta')['content']
        print('')
        print('Image no. ' + str(i) + ' of ' + str(image_num_limit))

        # Hmm, need to handle this condition better -jfadams1963
        if image_url is None:
            print("No image found")
            continue
        print("Downloading " + image_url)
        file_name = folder + image_url.split('/')[-1]

        try:
            # Use scrapeops proxy to download image  -jfadams1963
            res = requests.get(url = 'https://proxy.scrapeops.io/v1/',
                               params = {'api_key': API_KEY,
                                         'url': image_url, },
                  stream = True, timeout = 20)
            
            exists = False
            if res.status_code == 200:
                exists = os.path.isfile(file_name)

            g = 0
            while exists:
                print("file exists:", file_name)
                g += 1
                file_name =folder+str(index)+"_"+str(g)+"_"+ image_url.split('/')[-1]
                exists = os.path.isfile(file_name)
                    
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f) 
                # Let's get rid of rediculous file names  -jfadams1963
                file_name = os.rename(file_name,
                                      folder + image_tag + '_' + str(i) + '.jpg')

            saved = os.path.isfile(file_name)
            # Should be =>if saved<=  -jfadams1963
            if saved:
                print(">>>> ",saved)
                print('Image sucessfully Downloaded: ',file_name)
            else:
                print('Image Couldn\'t be retrieved')

        except Exception as e:
            print(e)
         
