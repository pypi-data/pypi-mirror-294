from mitmproxy import ctx,http
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
import json
with open('args.json','r') as f:
    content=json.load(f)
cdn,domains=content['cdn'],content['domains']
def response(flow):
    url=flow.request.url
    if urlparse(url).netloc in domains: # Only replace for specified domains
        try:
            soup=bs(flow.response.content.decode())
            body=soup.find('body')
            flag=0
            for i in soup.find_all('img'): # Iterate through images and look for math
                if 'en.wikipedia.org/api' in i['src'] and ('alt' in i.attrs):
                    i.replaceWith(f'\\({i["alt"]}\\)')
                    flag=1
            if not flag:
                return
            jax = bs(
                f'<script id="MathJax-script" async src="https://{cdn}/npm/mathjax@3/es5/tex-mml-chtml.js"></script>')
            body.insert(0, jax.find('script'))
            flow.response.content=str(soup).encode()
        except:
            pass