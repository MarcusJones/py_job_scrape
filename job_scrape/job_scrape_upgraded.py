#  -*- coding: utf-8 -*-


# Code modified from:
#https://www.scrapehero.com/how-to-scrape-job-listings-from-glassdoor-using-python-and-lxml/

#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Add parent module
#===============================================================================
# from os import sys, path
# # Add parent to path
# if __name__ == '__main__' and __package__ is None:
#     this_path = path.dirname(path.dirname(path.abspath(__file__)))
#     sys.path.append(this_path)
#     logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================
import requests
import re
#import os
#import sys
import unicodecsv as csv
#import argparse
#import json
#from exceptions import ValueError

#===============================================================================
#--- SETUP external modules
#===============================================================================
#from lxml import html#, etree
import lxml as lxml
from lxml import html
from xml import etree
#print(lxml.etree) 
#TODO: resolve etree import error!

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.util_inspect import get_self

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- MAIN CODE
#===============================================================================

HEADERS = {    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                'referer': 'https://www.glassdoor.com/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
    }

LOCATION_HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'referer': 'https://www.glassdoor.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }



def get_place_id(place):
    logging.debug("Get place_id from a place")
    
    data = {"term": place,
            "maxLocationsToReturn": 10}
    
    location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
    
    # Getting location id for search location
    logging.debug("Fetching location details")
    location_response = requests.post(location_url, headers=LOCATION_HEADERS, data=data).json()
    logging.debug("Response: {} place entries retrieved, returning first hit".format(len(location_response)))
    place_id = location_response[0]['locationId']
    
    for entry in location_response:
        logging.debug("Entry: {}".format(entry))
    
    return place_id

def write_raw_html(response):
    raw_html_file = r"sourcefile.html"
    with open(raw_html_file, 'wb') as file:
        file.write(response.text.encode("utf-8"))



def get_next_button_link(parser):
    #--- Breaking down the tree
    #XPATH_NEXT_BUTTON = '//li[@class="next"]'
    #next_button = parser.xpath(XPATH_NEXT_BUTTON)[0]
    #print(next_button)
    #print(type(next_button))
    
    #next_link = next_button.getchildren()[0]
    #print(next_link)
    
    #--- Here it is in a one-liner!
    next_href = parser.xpath('//li[@class="next"]/a')[0]
    the_link = next_href.attrib['href']
    return the_link


def get_parser_html(url,data):
    # Form data to get job results
    
    response = requests.post(url, headers=HEADERS, data=data)
    logging.debug("Got response".format(response))
    #--- Write the raw html file
    #write_raw_html(response)
    
    #--- The parser initialized
    parser = html.fromstring(response.text)

    # Making absolute url 
    base_url = "https://www.glassdoor.com"
    parser.make_links_absolute(base_url)
    
    next_link = get_next_button_link(parser)
    #print(next_link)
    logging.debug("Returning parser {}, and next link {}".format(parser, next_link))
    
    return parser, next_link

def get_listings(parser):
    raise
def parse_place(place_id,search_city_name):
    data = {
        'clickSource': 'searchBtn',
        'sc.keyword': keyword,
        'locT': 'C',
        'locId': place_id,
        'jobType': ''
    }
    
    job_listings = []

    first_job_listing_url = 'https://www.glassdoor.com/Job/jobs.htm'
    
    #--- Get the parser and next link
    parser, next_link = get_parser_html(first_job_listing_url,data)
    
    raise   
    
    
    XPATH_ALL_JOB = '//li[@class="jl"]'
    XPATH_NAME = './/a/text()'
    XPATH_JOB_URL = './/a/@href'
    XPATH_LOC = './/span[@class="subtle loc"]/text()'
    XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
    XPATH_SALARY = './/span[@class="green small"]/text()'
    
    listings = parser.xpath(XPATH_ALL_JOB)
    
    logging.debug("Parsing {} listings".format(len(listings)))
    
    for i,job in enumerate(listings):
        
        raw_job_name = job.xpath(XPATH_NAME)
        raw_job_url = job.xpath(XPATH_JOB_URL)
        raw_lob_loc = job.xpath(XPATH_LOC)
        raw_company = job.xpath(XPATH_COMPANY)
        raw_salary = job.xpath(XPATH_SALARY)

        # Cleaning data
        job_name = ''.join(raw_job_name).encode("ascii","ignore") if raw_job_name else None
        job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
        raw_state = re.findall(",\s?(.*)\s?", job_location)
        state = ''.join(raw_state).strip()
        raw_city = job_location.replace(state, '')
        city = raw_city.replace(',', '').strip()
        company = ''.join(raw_company).encode("ascii","ignore").strip()
        salary = ''.join(raw_salary).strip()
        job_url = raw_job_url[0] if raw_job_url else None

        jobs = {
            "search_city" : search_city_name,
            "name": job_name.decode('utf-8'),
            "company": company.decode('utf-8'),
            "state": state,
            "city": city,
            "salary": salary,
            "location": job_location,
            "url": job_url
        }
        job_listings.append(jobs)

    return job_listings
# else:
#     print("location id not available")

PLACE_IDS = [
    {'city' :   'berlin',           'id':262210 },
    {'city' :   'stuttgart',        'id':2507190},
     ]


def parse_all_places(keyword):
    listings = list()
    for pl in PLACE_IDS:
        city_name = pl['city']
        place_id = str(pl['id'])
        logging.debug("Parsing location: {:<20} {:<2} {:>10}".format(city_name,'0',place_id))
        new_listings = parse_place(place_id,city_name)
        listings = listings + new_listings
        
        #break
    return listings
    
    #raise
    #parse_place(keyword)
    #parse_place()


if __name__ == "__main__":
    
    #--- Get a place_id from a city name, build up a dictionary
    place = "stuttgart"
    #get_place_id()
    
    #--- Get a job listing by keyword
    keyword = "Data Scientist"
    scraped_data = parse_all_places(keyword)
    logging.debug("Raw data over {} listings: ".format(len(scraped_data)))
    for i,el in enumerate(scraped_data):
        #print(el)
        print(i,el['city'],el['name'], el['company'])
    
    #--- Write results
    print("Writing data to output file")
    file_name = 'job-results.csv'
    with open(file_name, 'wb') as csvfile:
        fieldnames = ['search_city', 'name', 'company', 'state',
                      'city', 'salary', 'location', 'url']
        #writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for i,data in enumerate(scraped_data):
            #print(i,data)
            
            writer.writerow(data)
            
    logging.debug("Wrote {} listings to {}".format(len(scraped_data),file_name))
        

