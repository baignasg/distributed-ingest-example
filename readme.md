# Overview

This project contains demonstration scripts for the Consuming REST Services course at [http://statistics.com](http://statistics.com).  These scripts simulate the basics of a distributed ingestion system using an Amazon Queue ([AWS SQS](http://aws.amazon.com/sqs/faqs/)) to enable multiple worker processes to ingest data and store the results locally.

## Disclaimer

This project is only meant to illustrate the scenario of using a queue object to distribute work to multiple workers.  In a real production environment, you would store the results in a WORM store and would have to contend with other issues such as API rate limiting.

Additionally, the code provided would need to be enhanced (at a minimum) with proper exception handling, logging, and configuration data management (to remove the API key from source code).  These features were left out in order to focus on the core functionality for demonstration purposes.

Should you require this type of distributed task system, I would recommended you look into [Celery](http://celery.readthedocs.org/en/latest/), a distributed task queue written in Python.


# Setup

There are several steps for setup of this demonstration.  The user will need to:

* Install required libraries
* Create an Amazon Web Services Account
* Download and configure AWS keys
* Create an SQS Queue


## Install Libraries

To install the required libraries, use pip install and the provided requirements.txt file.

	pip install -r requirements.txt

## Create an Amazon Web Services account

An account for AWS can be created at [http://aws.amazon.com/](http://aws.amazon.com/).

## Download and configure security keys

The easiest way to configure your scripts for secure access to AWS will be to create an Access Key ID and Secret Access Key.  To do so visit [your account security credentials](https://console.aws.amazon.com/iam/home?#security_credential) page, open up the "Access Keys" section, and click on "Create New Access Key".  You may download the new key file depending on how you choose to supply Boto with your credentials.

It's recommended that you setup secure access to AWS according to the [Boto documentation](http://boto.readthedocs.org/en/latest/boto_config_tut.html).

## Create AWS SQS Queue

Visit the [AWS SQS](https://console.aws.amazon.com/sqs/) page to manage SQS Queues.  Click on "Create New Queue", supply a "Queue Name", and then use the provided default values.

The name you enter will need to be added to both enqueuer.py and worker.py as the value for `QUEUE_NAME`.

Note: At the time of this documentation, API requests to SQS were free up to the first one million requests per month and 50 cents per million afterwards.

## Register for a Sunlight Foundation API key

Visit the Sunlight Foundation [registration page](http://sunlightfoundation.com/api/accounts/register/) to signup for an API key.  Registration is free and your key will be emailed to you.

Your API key will need to be added to worker.py as the value for `API_KEY`.

# enqueuer.py

This script will read in all CSV files within the `./data` directory, loop through each row, and send a JSON version to the SQS queue.  To activate the script, use the following command:

	python enqueuer.py

Do not attempt to run multiple copies of the `enqueuer.py` file concurrently.

# worker.py

This script will download one message at a time from the SQS Queue, use the data to make a request of the Sunlight Foundation Capitol Words API, and then save the results to the local disk.  To activate the script, use the following command:

	python worker.py

For a more accurate demonstration you will want to run multiple copies of this script concurrently.  To do so, you may use the following command which will create 4 running copies of the script and background the processes.  Doing so will simulate four separate computers, each running the script separately.

    python worker.py & python worker.py & python worker.py & python worker.py &


