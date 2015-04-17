# enqueuer.py
# Enqueues data from CSVs to AWS SQS
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
Process CSVs and adds each row to an AWS SQS Queue as a Dictionary object
"""

##########################################################################
## Imports
##########################################################################

import os
import boto.sqs
import unicodecsv
import json
import sys

from os.path import basename
from time import sleep
from boto.sqs.message import Message

##########################################################################
## CONSTANTS
##########################################################################

QUEUE_NAME = 'rest-ingestion-course'
DATA_PATH = './data'


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

def get_files():
    '''
    convenience function to return a list of paths to all files with a
    .csv extension in the data subdirectory
    '''
    file_extension_mask = 'csv'
    return [os.path.join('.','data', f) for f in os.listdir(DATA_PATH)
        if f.endswith(file_extension_mask)]


##########################################################################
## Main Functions
##########################################################################


def enqueue(queue, files):
    '''
    loops through an array of CSV file paths in order to convert each row
    to a JSON object, and then add it to the SQS Queue
    '''
    counter = 0

    # loop through files
    for f in files:

        # create a reader for the CSV object that will provide each row as
        # a dictionary
        reader = unicodecsv.DictReader(open(f))

        # loop through rows of the CSV
        for data in reader:

            # create a json version of the csv data
            package = json.dumps(data)

            # create and submit a new message to the queue
            m = Message()
            m.set_body(package)
            queue.write(m)

            # increment counter and draw a '.' to screen to show progress
            counter += 1
            ping()

    print "\n\nExiting - End of data files.  %d rows queued.\n" % counter


##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    queue = get_queue()
    files = get_files()
    enqueue(queue, files)
