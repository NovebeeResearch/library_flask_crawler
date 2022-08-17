import argparse
from random import randint
import requests
import logging
import http.client
import re
from urllib.parse import urlparse, urljoin, urlsplit
from bs4 import BeautifulSoup
import time 
from my_parser import parser_amazon


DEFAULT_PHRASE = 'python'
#format="%(asctime)s %(levelname) %(message)s"
logging.basicConfig(level=logging.DEBUG,filename='my.log', filemode='w', format='%(asctime)s ---- %(levelname)s ---- %(message)s')


## Helper function 1 
def process_link(source_link):

    logging.info(f'Extracting links from {source_link}')
    parsed_source = urlsplit(source_link) ## scheme://netloc/path;parameters?query#fragment
    #print("scheme://netloc/path;parameters?query#fragment: " + parsed_source.scheme+parsed_source.netloc+parsed_source.path+parsed_source.parameters+parsed_source.query+parsed_source.fragment)
    time.sleep(randint(4,8))
    result = requests.get(source_link)
    ## headling error
    if result.status_code != http.client.OK:
        logging.error(f'Error retrieving {source_link}: {result}')
        return []

    if 'html' not in result.headers['Content-type']:
        logging.info(f'Link {source_link} is not an HTML page')
        return []
    page = BeautifulSoup(result.text, 'html.parser')

    #create one function level of list: list stack to loop through
    #create two function-return level of list; list of website and list of dictionaries
    links_list = []
    childlinks_list = []
    parsed_info = []

    links_, child_links_ = get_links(parsed_source, page)
    for child_link in child_links_:
        if child_link not in childlinks_list:
            childlinks_list.append(child_link)        
    for link_ in links_:
        if link_ not in links_list: 
            links_list.append[link_]

    i_ = 0
    while( (len(links_list)>1) and len(parsed_info)<200 ):
        parsed_source = urlsplit(links_list[0])
        time.sleep(randint(4,8))
        result = requests.get(links_list[0])
        ## headling error
        if result.status_code != http.client.OK:
            logging.error(f'Error retrieving {links_list[0]}: {result}')
            i_+=1
            links_list.pop(0)
            continue

        if 'html' not in result.headers['Content-type']:
            i_+=1
            links_list.pop(0)
            continue   
        page = BeautifulSoup(result.text, 'html.parser')     


        links_,child_links_ = get_links(parsed_source, page)

        for child_link in child_links_:
            if child_link not in childlinks_list:
                childlinks_list.append(child_link)
                link_parser = parser_amazon.Parser(page)
                parsed_info.append(link_parser.extract_info())        
        for link_ in links_: 
            if link_ not in links_list:
                links_list.append(link_)
        links_list.pop(0)
        i_+=1
    return childlinks_list, parsed_info


## Helper Function 2 
def get_links(parsed_source,page):
    '''Retrieve the links on the page'''
    links = []
    child_links =[]

    #for element in page.find_all("div", {self.class_name}):
    for element in page.find_all("a"):
        link = element.get('href')
        if not link:
            continue

        # Avoid internal, same page links
        if link.startswith('#'):
            continue

        if link.startswith('mailto:'):
            # Ignore other links like mailto
            # More cases like ftp or similar may be included here
            continue


        # Always accept local links
        if not link.startswith('http'):
            netloc = parsed_source.netloc
            scheme = parsed_source.scheme
            path = urljoin(parsed_source.path, link)
            link = f'{scheme}://{netloc}{path}'

        # Only parse links in the same domain
        bs_flag = re.search(r'ref=zg_bs',link)
        bs_flag2 = re.search(r'/Best-Sellers-Books',link)
        if parsed_source.netloc not in link:
            continue
        if (bs_flag2 is None) and (bs_flag is None):
            continue
        if (bs_flag2 is None) and (bs_flag is not None):
            child_links.append(link)
        links.append(link)
    return links, child_links







class LinksGen:
    #"p13n-gridRow _cDEzb_grid-row_3Cywl"
    def __init__(self,source_link,class_name = "_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz"):
        self.source_link = source_link
        self.class_name = class_name

        childlinks_list, parsed_info  = process_link(source_link)
        self.childlinks_list, self.parsed_info = childlinks_list, parsed_info
        time.sleep(randint(4,8))
        result = requests.get(source_link)

    def get_links(self): 
        return self.childlinks_list   

    def get_parsed_info(self):
        return self.parsed_info
    


