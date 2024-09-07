"""
mathfixer is a tool for replacing math tags in MediaWiki based wikis with MathJax (MediaWiki based wikis usually use Wikipedia to show math, which is blocked in some places.)

This tool is not a VPN-like tool. Instead, it replaces content using a proxy locally (using 127.0.0.1).

Note: Text using \( and \) might be affected
"""
from argparse import *
import os
from json import dump
def main():
    a = ArgumentParser()
    a.add_argument('-d', '--domain', help='Domain(s) of the wiki(s) for mathfixer to fix, esolangs.org by default',
                   nargs='*')
    a.add_argument('-p', '--port', help='Port for the proxy to listen (IP is 127.0.0.1), default is 8080', type=int)
    a.add_argument('-c', '--cdn', help='CDN used to load MathJax, default is gcore.jsdelivr.net',default='gcore.jsdelivr.net')
    p = a.parse_args()
    port, domain = 8080, ['esolangs.org']
    if p.port:
        port = p.port
    if p.domain:
        domain = p.domain
    cdn=p.cdn
    with open('args.json','w') as f:
        dump({'cdn':cdn,'domains':domain},f)
    os.system(f'mitmdump -s {os.path.join(os.path.dirname(__file__),"proxy.py")} --listen-host 127.0.0.1 --listen-port {port}')
if __name__=='__main__':
    main()