from bs4 import BeautifulSoup
import urllib3
import requests
import re

from sexmachine.detector import Detector as gender

'''
Determines whether user is verified from profile url
Easily modifiable for similar lookups

Ex:
verified('https://twitter.com/intent/user?user_id=793887941709991936')

'''
def verified(lookup_url):
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    url = str(lookup_url)
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data,'html.parser')
    #print(soup.prettify())

    # search html
    nametag = soup.find('a',{'class':'fn url alternate-context'})
    if nametag:
        print(nametag.text)
    else:
        print('---')
    #if soup.findAll(class='Verified'):
    if soup.find("li", { "class" : "verified" }):
        #print('Verified')
        return True
    else:
        return False


def guess_gender(namestring):
    #strip
    pattern = re.compile('([^a-zA-Z_])+')
    stripped = pattern.sub('', namestring)
    stripped = str(stripped)
    #stripped = stripped.decode('utf-8')
    print(stripped)
    d = gender(case_sensitive=False)
    print(d.get_gender(stripped))


# guess_gender('sharon')
