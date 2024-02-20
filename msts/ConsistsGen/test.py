import wget

import requests
url = r"https://www.bing.com/search?pglt=41&q=12627%2F+site%3Aindiarailinfo.com"

file = wget.download(url)
