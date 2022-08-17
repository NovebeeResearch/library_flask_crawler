import argparse
import configparser
import csv
import json
import pandas

from selenium import webdriver
from bs4 import BeautifulSoup
from my_parser import parser_amazon, crawling_amazon

def list2txt(list_,path_):
    with open(path_,"w") as file:
        for ele_list in list_:
            file.write(ele_list)
            file.write('\n')
        file.close

def listDict_to_csv(listDict,csv_columns,file_path_):
    try:
        with open(file_path_, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in listDict:
                writer.writerow(data)
    except IOError:
        print("I/O error")

def buildParser_getJson(base_url,output):
    links_generater = crawling_amazon.LinksGen(base_url,class_name = '_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')
    myLinks = links_generater.get_links()  ##For the updated version, myLinks is equal to links
    web_parser = links_generater.get_parser()
    parsed_info = links_generater.get_parsed_info()

    info_df = pandas.DataFrame(parsed_info)
    info_df.to_csv('data/out.csv', index = False, encoding='utf-8')

    with open('data/data.json', 'w') as fp:
        json.dump(parsed_info, fp)

    return 0

def main(base_url, output):
    #URL = 'https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers'
    links_generater = crawling_amazon.LinksGen(base_url,class_name = '_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')
    parsed_info = links_generater.get_parsed_info ##For the updated version, myLinks is equal to links

    ## keys attributes for each website object
    #key_attri = ("Name","Author","Print length","Price","Also purchased","Description","Review rating")


    info_df = pandas.DataFrame(parsed_info)
    info_df.to_csv('data/out.csv', index = False, encoding='utf-8')


    with open('data/data.json', 'w') as fp:
        json.dump(parsed_info, fp)

    #file_pa = "model/web_scraper/data"
    #csv_col = ['Name','Author','Length']
    #listDict_to_csv(listDict_to_csv ,csv_col,file_pa)



"""
import csv
csv_columns = ['Name','Author','Length']
csv_file = "out.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in info_list:
            writer.writerow(data)
except IOError:
    print("I/O error")
"""





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n1', dest='target_url', type=str,help='Base URL', default='https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_nav_0')
    parser.add_argument('--config', '-c', type=argparse.FileType('r'),
                        help='config file')
    parser.add_argument('-o', dest='output', type=argparse.FileType('w'),
                        help='output file',
                        default="my_output.txt")
    args = parser.parse_args()
    if args.config:
        config = configparser.ConfigParser()
        config.read_file(args.config)
        # Transforming values into integers
        args.target_url = config['ARGUMENTS']['target_url']
        args.output = config['ARGUMENTS']['output_file']

    print("The target_url: "+ args.target_url)
    main(args.target_url, args.output)
