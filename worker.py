# worker.py
# Processes essages from an AWS SQS Queue.  Each message contains a
# JSON object containing a country to lookup in the Capitol Words API.
# Each return from the API is saved to disk for later processing.
#
# In order to run, you will need an AWS account and have added your
# access and secret keys to your environmental variables or boto
# config as detailed in the boto documentation.
#
# Note that this is for demonstration only and is not production ready
# code.  At a minimum this file would require exeption handling, logging,
# etc.
#
# Author:   Allen Leis
# Created:  Wed April 10 20:14:08 2015

"""
Transforms messages from an AWS SQS Queue and adds to a MongoDB database
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import json
from datetime import datetime
import re

import boto.sqs
import requests


##########################################################################
## Module Variables
##########################################################################

# enter your sunlight foundation API key below
API_KEY = ''

QUEUE_NAME = 'rest-ingestion-course'
WORDS_API_URL = 'http://capitolwords.org/api/1/phrases/legislator.json'
START_DATE = '2014-01-01'
END_DATE = '2015-04-01'
STORAGE_PATH = './store'

##########################################################################
## Helper Functions
##########################################################################

def ping():
    '''
    simple function to draw a dot to the screen every time a message is
    processed
    '''
    sys.stdout.write('.')
    sys.stdout.flush()

def get_queue():
    '''
    convenience function to return a connection to the SQS Queue
    '''
    conn = boto.sqs.connect_to_region("us-east-1")
    return conn.get_queue(QUEUE_NAME)




##########################################################################
## Main Functions
##########################################################################

def request(country):
    '''
    Helper function to perform a GET request on the Capitol Words API
    '''
    params = {
        'phrase': country,
        'per_page': 20,
        'apikey': API_KEY,
        'start_date': START_DATE,
        'end_date': END_DATE,
    }

    r = requests.get(WORDS_API_URL, params=params)
    r.raise_for_status()
    return r.text


def store(country, data):
    # create a filename and path for storing data
    filename = re.sub('[^A-Za-z0-9]+', '', country)
    filename = re.sub('\s', '_', country)
    filename = filename.lower() + '.json'
    path = os.path.join(STORAGE_PATH, filename)

    # write the data to disk as a new file
    with open(path, 'w') as f:
        f.write(data)


def work(queue):
    '''
    loops through an SQS Queue, requests data from the Capitol Words API, and
    then stores the result on the local disk
    '''
    counter = 0
    start = datetime.now()

    while True:
        # attempt to read next message
        m = queue.read()

        # check if there was no message read
        if m == None:
            # if no message then the queue must be empty and we can stop
            elapsed = datetime.now() - start
            print "\nExiting - End of Queue reached in %d seconds.  %d messages processed." % \
                (elapsed.total_seconds(), counter)
            break

        # recreate original dict from json message body
        data = json.loads(m.get_body())

        # request top legislators for country from Capitol Words API
        response = request(data['country'])

        # store API response to disk
        store(data['country'], response)

        # delete message from the queue
        res = queue.delete_message(m)

        # increment counter and draw a '.' to screen to show progress
        counter += 1
        ping()


##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    queue = get_queue()
    work(queue)
