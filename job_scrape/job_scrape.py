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

def parse(keyword, place):
    logging.debug("Running on {} {}".format(keyword,place))

    headers = {    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                'referer': 'https://www.glassdoor.com/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
    }

    location_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'referer': 'https://www.glassdoor.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    data = {"term": place,
            "maxLocationsToReturn": 10}

    location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"

    
    # Getting location id for search location
    logging.debug("Fetching location details")
    
    location_response = requests.post(location_url, headers=location_headers, data=data).json()
    place_id = location_response[0]['locationId']
    logging.debug("place_id:{}".format(place_id))
    
    job_litsting_url = 'https://www.glassdoor.com/Job/jobs.htm'
    # Form data to get job results
    data = {
        'clickSource': 'searchBtn',
        'sc.keyword': keyword,
        'locT': 'C',
        'locId': place_id,
        'jobType': ''
    }

    job_listings = []
    
    if place_id:
        
        response = requests.post(job_litsting_url, headers=headers, data=data)
        # extracting data from
        # https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=andr&sc.keyword=android+developer&locT=C&locId=1146821&jobType=
        #print(response)
        #raise
        
        parser = html.fromstring(response.text)
        # Making absolute url 
        base_url = "https://www.glassdoor.com"
        parser.make_links_absolute(base_url)
        
        XPATH_ALL_JOB = '//li[@class="jl"]'
        XPATH_NAME = './/a/text()'
        XPATH_JOB_URL = './/a/@href'
        XPATH_LOC = './/span[@class="subtle loc"]/text()'
        XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
        XPATH_SALARY = './/span[@class="green small"]/text()'

        listings = parser.xpath(XPATH_ALL_JOB)
        for job in listings:
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
                "Name": job_name,
                "Company": company,
                "State": state,
                "City": city,
                "Salary": salary,
                "Location": job_location,
                "Url": job_url
            }
            job_listings.append(jobs)

        return job_listings
    else:
        print("location id not available")


if __name__ == "__main__":

    ''' eg-:python 1934_glassdoor.py "Android developer", "new york" '''

    #argparser = argparse.ArgumentParser()
    #argparser.add_argument('keyword', help='job name', type=str)
    #argparser.add_argument('place', help='job location', type=str)
    #args = argparser.parse_args()
    #keyword = args.keyword
    #place = args.place
    keyword = "Data Scientist"
    place = "berlin"
    print("Fetching job details")
    scraped_data = parse(keyword, place)
    
    for el in scraped_data:
        print(el)
    #print(scraped_data)
    raise
    print("Writing data to output file")

    with open('%s-%s-job-results.csv' % (keyword, place), 'w')as csvfile:
        fieldnames = ['Name', 'Company', 'State',
                      'City', 'Salary', 'Location', 'Url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
        writer.writeheader()
        if scraped_data:
            for data in scraped_data:
                writer.writerow(data)
        else:
            print ("Your search for %s, in %s does not match any jobs"%(keyword,place))


