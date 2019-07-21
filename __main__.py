from bs4 import BeautifulSoup as bs
from pprint import pprint
from subprocess import call
import requests

def search_string(s):
    return s.replace(" ", "+")

def get_url(v_ids, base):
    f_id = v_ids[0]

    ids = ",".join(v_ids)
    url = f"{base}/watch_videos?video_ids={ids}"
    return url

def parse_infile(file_name):
    s = open(file_name).read().strip()
    return s.split("\n")

def get_v_id(qstring):
    r = requests.get(f"{QBASE}{qstring}")

    page = r.text
    soup = bs(page,'html.parser')

    vids = soup.findAll('a', attrs={'class':'yt-uix-tile-link'})


    return vids[0]['href'].split("=")[-1] #for v in vids

BROWSER = "qutebrowser"
BASE    = "https://www.youtube.com"
QBASE   = f"{BASE}/results?search_query="
INFILE  = "queries.txt"

queries = parse_infile(INFILE)

qstrings = [search_string(s) for s in queries]

v_ids = [get_v_id(qstring) for qstring in qstrings]

url = get_url(v_ids, BASE)

call((
    BROWSER,
    url
))
