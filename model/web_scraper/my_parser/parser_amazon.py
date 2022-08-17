import logging
from pickle import NONE
from selenium import webdriver
from bs4 import BeautifulSoup
from parse import parse 
import time 

class Parser:
    #"p13n-gridRow _cDEzb_grid-row_3Cywl"
    def __init__(self,soup_page, target_url = ''):
        if target_url is None:
            logging.error(f'Parser does not get the target url:{target_url}')
        self.target_url = target_url
        self.soup = soup_page

        self.key_attri = ("Name","Author","Print length","Price","Also purchased","Description","Review rating")

    
    def set_key(self,k):
        self.key_attri = k 

    def get_key(self):
        return self.key_attri

    def extract_info(self):

        soup = self.soup
        ## val_ attri for this url instant 
        val_attri = [-1 for i in range(len(self.key_attri))]

        # Find name 
        #soup.find()
        time.sleep(1)
        soup_found = soup.find("meta", {"name":"description"}) or soup.find("span",{"id":"productTitle"})
        if soup_found is not None: 
            soup_found = soup_found.text
        else:
            soup_found = ''
        raw_name = soup_found
        split_name = raw_name.split("on Amazon.com")
        result_name, _ = split_name
        val_attri[0] = result_name
        #<span id="productTitle" class="a-size-extra-large"> All Your Perfects: A Novel </span>

        #Find Author 
        raw_author = soup.find("a",{"class":"a-link-normal contributorNameID"})or ''
        if(raw_author !=''):
            raw_author = raw_author.text
        val_attri[1] = raw_author

        #Find Print length 

        raw_page = soup.find("div",{"class":"a-section a-spacing-none a-text-center rpi-attribute-value"}) or ''
        if (raw_page !=''):
            raw_page = raw_page.contents[1] #<span>434 pages</span>
            FORMAT = '<span>{page} pages{anyway}'
            result_page = parse(FORMAT,raw_page)
            val_attri[2] = result_page['page']
        else: 
            val_attri[2] = ''

        return {"Name":val_attri[0],"Author":val_attri[1],"Length":val_attri[2]}


        ## Description  <meta name="description" content="It Ends with Us: A Novel (1) [Hoover, Colleen] on Amazon.com. *FREE* shipping on qualifying offers. It Ends with Us: A Novel (1)">
        ## Name <meta name="title" content="It Ends with Us: A Novel (1): Hoover, Colleen: 9781501110368: Amazon.com: Books">

        #Author 
        #<a data-asin="B08BNMFT7P" class="a-link-normal contributorNameID" href="/Alex-Xu/e/B08BNMFT7P/ref=dp_byline_cont_book_1">Alex Xu</a>
        #<a data-asin="B006SKAK42" class="a-link-normal contributorNameID" href="/Colleen-Hoover/e/B006SKAK42/ref=dp_byline_cont_book_1">Colleen Hoover</a>

        ## Page 
        #<div class="a-section a-spacing-none a-text-center rpi-attribute-value"> <span>434 pages</span> </div>
        #<div class="a-section a-spacing-none a-text-center rpi-attribute-value"> <span>384 pages</span> </div>


    

    
