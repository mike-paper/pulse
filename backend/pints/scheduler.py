import pints
from logger import logger
import datetime
import random
import sqlalchemy
import json
import pytz
import uuid
import os
import time
import pandas as pd
import traceback
from metrics import metrics
from app import app, db
import concurrent.futures

longrun = concurrent.futures.ThreadPoolExecutor(max_workers=None)

PAPER_DO_NOT_START_SCHEDULER = int(os.environ.get('PAPER_DO_NOT_START_SCHEDULER', 0)) > 0


def startScheduler():
    logger.info(f'startScheduler? {(not PAPER_DO_NOT_START_SCHEDULER)}')
    if PAPER_DO_NOT_START_SCHEDULER:
        # runWeekly()
        logger.info(f'not starting scheduler...')
        return False
    logger.info(f'starting scheduler...')
    pints.postgres.deleteIncompleteJobs(db.engine)
    longrun.submit(runScheduler)

def runScheduler():
    runningScheduler = True
    while runningScheduler:
        try:
            checkForScheduledJobs()
        except Exception as e:
            logger.error(f'error in checkForScheduledJobs: {str(e)}')
            logger.error(f'error in checkForScheduledJobs traceback: {traceback.format_exc()}')
        try:
            checkQueue()
        except Exception as e:
            logger.error(f'error in checkQueue: {str(e)}')
            logger.error(f'error in checkQueue traceback: {traceback.format_exc()}')
            
        time.sleep(60)
    return True

def runHourlyTeam(team):
    logger.info(f'runHourlyTeam...')
    with app.app_context():
        logger.info(f"team {team['id']}...")
        settings = pints.postgres.getSettings(db.engine, team['id'])
        jobUuids = fullRefresh(db.engine, team['id'])
        if not jobUuids:
            return False
        slackOn = settings['notifications'].get('alerts', {}).get('slack', False)
        slackChannel = settings['notifications'].get('slackChannel', False)
        if slackOn and slackChannel:
            dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')
            details = {
                'status': 'pending',
                'dependencies': jobUuids,
                'type': 'sendNotifications',
                'maxCreatedOn': dt,
                'maxCanceledOn': dt,
            }
            jobUuid = uuid.uuid4().hex
            targetId = pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
            messageId = pints.postgres.addMessage(db.engine, team['id'], targetId, details, jobUuid)
            logger.info(f'runHourly slack messageId... {messageId}')
        if settings.get('sheets', {}).get('spreadsheetId', False):
            spreadsheetId = settings.get('sheets', {}).get('spreadsheetId', False)
            dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')
            details = {
                'status': 'pending',
                'dependencies': jobUuids,
                'type': 'updateSheets',
                'maxCreatedOn': dt,
                'maxCanceledOn': dt,
            }
            logger.info(f'runHourly sheet... {spreadsheetId}')
            jobUuid = uuid.uuid4().hex
            targetId = pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
            messageId = pints.postgres.addMessage(db.engine, team['id'], targetId, details, jobUuid)
            logger.info(f'runHourly sheet messageId... {messageId}')
    return True

def runWeekly():
    teams = pints.postgres.getTeams(db.engine)
    for team in teams:
        runWeeklyTeam(db.engine, team['id'])

def runWeeklyTeam(engine, teamId):
    logger.info(f'runWeeklyTeam... {teamId}')
    settings = pints.postgres.getSettings(engine, teamId)
    logger.info(f'runWeeklyTeam settings... {settings}')
    if settings['notifications'].get('weekly', {}).get('slack', False):
        toSlack = metrics.getSlackMsg(engine, teamId)
        slackInfo = pints.postgres.getSlackInfo(engine, teamId)
        pints.slack.weekly(toSlack, slackInfo['bot_token'])
    return True

def runMonthly(engine):
    return True

def fullRefresh(engine, teamId):
    logger.info(f'fullRefresh...')
    jobUuids = pints.stripe.getAll(engine, teamId)
    logger.info(f'fullRefresh jobUuids: {jobUuids}')
    return jobUuids
    
def do_some_work(jobRow):
    logger.info(f'do_some_work... {jobRow}')
    if random.choice([True, False]):
        logger.info(f'do_some_work failed... {jobRow}')
        raise Exception
    else:
        logger.info(f'do_some_work SUCCESS... {jobRow}')

def testSched():
    logger.info(f'testSched...')
    return True

def checkForScheduledJobs():
    logger.info(f'checkForScheduledJobs...')
    teams = pints.postgres.getTeams(db.engine)
    totalRan = 0
    for team in teams:
        runHourlyNow = False
        runWeeklyNow = False
        if pd.isnull(team['last_hourly']):
            runHourlyNow = True
        else:
            dt = datetime.datetime.utcnow()
            diff = (dt - team['last_hourly'])
            totalSeconds = diff.total_seconds()
            minutes = totalSeconds / 60
            logger.info(f'checkForScheduledJobs minutes: {minutes}')
            if minutes > 60:
                runHourlyNow = True
        if pd.isnull(team['last_weekly']):
            runWeeklyNow = True
        else:
            dt = datetime.datetime.utcnow()
            diff = (dt - team['last_weekly'])
            totalSeconds = diff.total_seconds()
            minutes = totalSeconds / 60
            minutesInWeek = 7*24*60
            if minutes > minutesInWeek:
                runWeeklyNow = True
        logger.info(f"checkForScheduledJobs (now is {dt}): {team['id']}, {team['last_hourly']}, {runHourlyNow}")
        if runHourlyNow:
            totalRan+=1
            logger.info(f'runHourlyNow...')
            details = {
                'type': 'hourly',
                'status': 'complete',
            }
            jobUuid = uuid.uuid4().hex
            pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
            runHourlyTeam(team)
        if runWeeklyNow:
            totalRan+=1
            logger.info(f'runWeeklyNow...')
            details = {
                'type': 'weekly',
                'status': 'complete',
            }
            jobUuid = uuid.uuid4().hex
            pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
            runWeeklyTeam(db.engine, team['id'])
    logger.info(f'done checkForScheduledJobs, totalRan: {totalRan}')
    return True

def checkQueue():
    logger.info(f'checkQueue...')
    gettingJobs = True
    while gettingJobs:
        jobRow, queueRow = pints.postgres.getMessages(db.engine)
        if jobRow:
            logger.info(f"checkQueue jobRow: {jobRow}")
            try:
                if jobRow['details']['type'] == 'sendNotifications':
                    logger.info(f'sendNotifications...')
                    lastJob = pints.postgres.getLastJob(db.engine, jobRow['team_id'], 'sendNotifications')
                    if not lastJob:
                        logger.info(f'adding first lastJob...')
                        dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')
                        details = {
                            'maxCreatedOn': dt,
                            'maxCanceledOn': dt,
                            'type': 'sendNotifications',
                            'status': 'complete',
                        }
                        jobUuid = uuid.uuid4().hex
                        pints.postgres.addJob(db.engine, jobRow['team_id'], details, jobUuid)
                        lastJob = pints.postgres.getLastJob(db.engine, jobRow['team_id'], 'sendNotifications')
                    logger.info(f'sendNotifications lastJob: {lastJob}')
                    alerts = pints.postgres.getAlerts(db.engine, jobRow['team_id'], lastJob)
                    logger.info(f'sendNotifications alerts: {alerts}')
                    for alert in alerts:
                        logger.info(f'sendNotifications alert: {alert}')
                        # TODO send alert
                        # pints.postgres.updateMessage(db.engine, alert['message_id'], {'status': 'sent'})
                        settings = pints.postgres.getSettings(db.engine, jobRow['team_id'])
                        d = {
                            'email': alert['email'],
                            'mrr': alert['mrr'],
                            'prev_mrr': alert['prev_mrr'],
                            'msg': f"Originally signed up on {alert['customer_created_on2']} ({alert['created_days_ago']} days to convert)",
                            'slackChannel': settings['notifications']['slackChannel']
                        }
                        slackInfo = pints.postgres.getSlackInfo(db.engine, jobRow['team_id'])
                        if alert['alert_type'] == 'canceled':
                            pints.slack.churnAlert(d, slackInfo['bot_token'])
                        else:
                            pints.slack.customerAlert(d, slackInfo['bot_token'])
                    dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')
                    details = {
                        'maxCreatedOn': dt,
                        'maxCanceledOn': dt,
                    }
                    pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'complete', None, details)
                if jobRow['details']['type'] == 'updateSheets':
                    logger.info(f'updateSheets...')
                    settings = pints.postgres.getSettings(db.engine, jobRow['team_id'])
                    spreadsheetId = settings.get('sheets', {}).get('spreadsheetId', False)
                    if not spreadsheetId:
                        logger.info(f'updateSheets no spreadsheetId...')
                        pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'error', 'No Spreadsheet ID', None)
                        return False
                    mrrFacts = metrics.getMrrFacts(db.engine, jobRow['team_id'])
                    d = {
                        'df': mrrFacts['df'],
                        'spreadsheetId': spreadsheetId,
                        'startCell': 'A1',
                        'sheet': 'pulse_mrr_facts'
                    }
                    pints.sheets.push(d)
            except Exception as e:
                logger.error(f'checkQueue error: {str(e)}')
                pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'error', str(e), None)
                raise e
                # if we want the job to run again, insert a new item to the message queue with this job id
                # con.execute(sql, (queue_item['target_id'],))
        else:
            logger.info(f'no jobs to run...')
            gettingJobs = False
        return True