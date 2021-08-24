import pandas as pd
pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 200)
pd.set_option("display.max_colwidth", 2000)
import datetime
import os
import sys
import time
import requests
import json
import io
import uuid
import concurrent.futures
import pdb
import collections
import pints
import stripe
from logger import logger

longrun = concurrent.futures.ThreadPoolExecutor(max_workers=None)

PAPER_STRIPE_LITE = int(os.environ.get('PAPER_STRIPE_LITE', 0)) > 0

objs = {
    'coupons': {
        'api': stripe.Coupon,
        'expand': []
    },
    'customers': {
        'api': stripe.Customer,
        'expand': []
    },
    'subscriptions': {
        'api': stripe.Subscription,
        'expand': [],
        'all': True,
    },
    'plans': {
        'api': stripe.Plan,
        'expand': []
    },
    'events': {
        'api': stripe.Event,
        'expand': [],
        'types': [
            'customer.subscription.deleted', 
            'customer.subscription.created', 
            'invoice.payment_action_required', 
            'invoice.voided', 
            'invoice.payment_failed'
            ]
    },
    'invoices': {
        'api': stripe.Invoice,
        'expand': ['data.discounts']
    }
}

if PAPER_STRIPE_LITE:
    del objs['subscriptions']

def testKey(apiKey):
    try:
        stripe.Customer.list(limit=1, api_key=apiKey)
        return {'ok': True}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

def getAll(engine, teamId):
    apiKey = pints.postgres.getStripeApiKey(engine, teamId)
    if not apiKey:
        return False
    jobUuids = []
    for key, obj in objs.items():
        logger.info(f'getAll: {key}')
        if key == 'events':
            for t in obj['types']:
                logger.info(f'event: {t}')
                jobUuid = uuid.uuid4().hex
                jobUuids.append(jobUuid)
                longrun.submit(getObject, engine, teamId, jobUuid, key, eventType=t)
        else:
            jobUuid = uuid.uuid4().hex
            jobUuids.append(jobUuid)
            longrun.submit(getObject, engine, teamId, jobUuid, key)
    return jobUuids

def clearAll(engine, teamId):
    for key, obj in objs.items():
        table = f'stripe_{key}'
        logger.info(f'clearAll: {key} {obj} {table}')
        pints.postgres.deleteRows(engine, table, teamId)
    return True

def getObject(engine, teamId, jobUuid, obj, eventType=None):
    logger.info(f'getObject: {obj}')
    job = {
        'type': 'stripe',
        'operation': 'getObject',
        'obj': obj,
        'status': 'running'
    }
    jobId = pints.postgres.updateJob(engine, teamId, False, jobUuid, job)
    ls = []
    try:
        apiKey = pints.postgres.getStripeApiKey(engine, teamId)
        table = f'stripe_{obj}'
        getAll = objs[obj].get('all', False)
        if getAll:
            mr = False
        else:
            mr = pints.postgres.getMaxRecord(engine, table, teamId)
        logger.info(f'{obj} mr: {mr}')
        if eventType:
            logger.info(f'{obj} with mr: {mr}')
            temp = objs[obj]['api'].list(limit=100, api_key=apiKey, created={'gt': mr}, type=eventType)
        elif mr:
            logger.info(f'{obj} with mr: {mr}')
            temp = objs[obj]['api'].list(limit=100, api_key=apiKey, created={'gt': mr}, expand=objs[obj]['expand'])
        elif getAll:
            temp = objs[obj]['api'].list(limit=100, status='all', api_key=apiKey, expand=objs[obj]['expand'])
        else:
            logger.info(f'{obj} without mr: {mr}')
            temp = objs[obj]['api'].list(limit=100, api_key=apiKey, expand=objs[obj]['expand'])
        for t in temp.auto_paging_iter():
            ls.append(t)
        logger.info(f'done getting {obj}, got {len(ls)} after {mr}')
        if getAll:
            pints.postgres.deleteRows(engine, table, teamId)
            logger.info(f'done deleteRows for {obj} ({len(ls)} rows)')
        pints.postgres.insertManyRows(engine, table, ls, teamId)
        logger.info(f'done inserting rows for {obj} ({len(ls)} rows)')
    except Exception as e:
        logger.error(f'getObject error {str(e)}')
        job['status'] = 'error'
        job['error'] = str(e)
        jobId = pints.postgres.updateJob(engine, teamId, jobId, jobUuid, job)
        return job
    job['status'] = 'complete'
    job['rows'] = len(ls)
    jobId = pints.postgres.updateJob(engine, teamId, jobId, jobUuid, job)
    checkDbtRun(engine, teamId)
    return ls

def checkDbtRun(engine, teamId):
    logger.info(f'checkDbtRun {teamId}')
    running = pints.postgres.getJobSummary(engine, teamId)
    running = running[(running.status == 'running') & (running.type == 'stripe')]
    logger.info(f'checkDbtRun, {len(running)} still running...')
    if len(running) == 0:
        try:
            logger.info(f'running dbt...')
            pints.modeling.runDbt(teamId)
        except Exception as e:
            logger.error(f'checkDbtRun error {str(e)}')
    else:
        logger.info(f'not running dbt yet...')