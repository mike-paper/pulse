import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, String, inspect
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.elements import quoted_name
import json
import os
import io
import uuid
from logger import logger
import pints

teamSettings = {
    'notifications': {
        'alerts': {
            'slack': True,
            'email': False,
            },
        'weekly': {
            'slack': True,
            'email': True,
            },
        'monthly': {
            'slack': True,
            'email': True,
            },
        },
    'sheets': {}
    }

def createReadOnlyUser(engine, teamId):
    userName = f"team_{teamId}_readonly"
    logger.info(f'createReadOnlyUser, creating {userName}...')
    readonlyPassword = os.environ.get('PAPER_READONLY_PASSWORD')
    with engine.connect() as con:
        try:
            trans = con.begin()
            schemaName = f"team_{teamId}_stripe"
            sql = f"CREATE SCHEMA IF NOT EXISTS {schemaName}"
            con.execute(sql)
            sql = f"create user {userName} PASSWORD '{readonlyPassword}';"
            con.execute(sql)
            sql = f"grant usage on schema {schemaName} to {userName};"
            con.execute(sql)
            sql = f"grant select on all tables in schema {schemaName} to {userName};"
            con.execute(sql)
            sql = f"alter user {userName} set search_path = {schemaName};"
            con.execute(sql)
            sql = f'''
            ALTER DEFAULT PRIVILEGES IN SCHEMA {schemaName} 
                GRANT SELECT ON TABLES TO {userName};
            '''
            con.execute(sql)
            trans.commit()
        except Exception as e:
            {'ok': False, 'error': str(e)}
    return {'ok': True, 'userName': userName}

def insertRows(engine, table, rows, teamId):
    with engine.connect() as con:
        totalRows = len(rows)
        for idx, row in enumerate(rows):
            d = {
                "team_id": teamId,
                "details": json.dumps(row)
                }
            sql = f'''
            INSERT INTO {table} (team_id, details) 
            VALUES(:team_id, :details)
            '''
            statement = sqlalchemy.sql.text(sql)
            res = con.execute(statement, **d)
            if idx % 100 == 0:
                logger.info(f'inserted row {idx} of {totalRows}.')

def insertManyRows(engine, table, rows, teamId):
    totalRows = len(rows)
    if totalRows == 0:
        logger.info(f'insertManyRows, no rows...')
        return True
    logger.info(f'insertManyRows, inserting {totalRows} into {table}...')
    cols = ['team_id', 'details']
    data = io.StringIO()
    for idx, row in enumerate(rows):
        data.write('|'.join(
            [
                str(teamId),
                json.dumps(row),
            ]
        ) + '\n')
    data.seek(0)
    raw = engine.raw_connection()
    curs = raw.cursor()
    curs.copy_from(data, table, columns=cols, sep='|')
    curs.connection.commit()

def getMaxRecord(engine, table, teamId):
    with engine.connect() as con:
        sql = f'''
        select max(t.details ->> 'created') 
        from "public".{table} as t
        where t.team_id = {teamId}
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()[0]
        return res

def getMaxJobRun(engine, teamId, schedule):
    with engine.connect() as con:
        sql = f'''
        select j.created_on
        from "public".jobs as j
        where j.team_id = {teamId}
        and j.details ->> 'type' = '{schedule}'
        order by j.id desc
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if res:
            return res[0]
        else:
            return False

def deleteRows(engine, table, teamId):
    with engine.connect() as con:
        sql = f'''
        delete from "public".{table} as t
        where t.team_id = {teamId}
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement)
        return res


def insertUser(engine, email, data):
    with engine.connect() as con:
        d = { "email": email, "details": json.dumps(data) }
        sql = '''
        INSERT INTO users(email, details) 
        VALUES(:email, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        userId = res.fetchone()[0]
        return userId

def insertTeam(engine, domain):
    with engine.connect() as con:
        teamUuid = uuid.uuid4().hex
        d = { "public_uuid": teamUuid, "domain": domain, "details": json.dumps(teamSettings) }
        sql = '''
        INSERT INTO teams(public_uuid, domain, details) 
        VALUES(:public_uuid, :domain, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        teamId = res.fetchone()[0]
        return teamId

def insertTeamMember(engine, teamId, userId):
    with engine.connect() as con:
        teamMembershipUuid = uuid.uuid4().hex
        d = { 
            "team_id": teamId,
            "user_id": userId,
            "public_uuid": teamMembershipUuid, 
            "role": "admin", 
            "details": json.dumps({}) 
            }
        sql = '''
        INSERT INTO team_membership(team_id, user_id, public_uuid, role, details) 
        VALUES(:team_id, :user_id, :public_uuid, :role, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        teamMembershipId = res.fetchone()[0]
        return teamMembershipId

def updateSettings(engine, teamId, details):
    with engine.connect() as con:
        d = { 
            "details": json.dumps(details),
            "team_id": teamId,
            }
        sql = '''
        UPDATE public.teams
        SET details = :details
        WHERE id = :team_id
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        return True

def getSettings(engine, teamId):
    with engine.connect() as con:
        sql = f'''
        select t.details
        from "public".teams as t
        where t.id = {teamId}
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if res:
            return res[0]
        else:
            return False

def getTeams(engine):
    sql = f'''
    with last_job as (
        select 
        j.team_id,
        max(j.created_on) as created_on,
        max(case when j.details ->> 'type' = 'hourly' then j.created_on end) as last_hourly,
        max(case when j.details ->> 'type' = 'weekly' then j.created_on end) as last_weekly,
        max(case when j.details ->> 'type' = 'sendNotifications' then j.created_on end) as last_notifications
        from "public".jobs as j
        where 1=1
        and j.status = 'complete'
        group by 1
    )

    select 
    t.id, 
    t.domain, 
    t.details as settings,
    lj.last_hourly,
    lj.last_weekly,
    lj.last_notifications
    from 
    "public".teams as t left join 
    last_job as lj on t.id = lj.team_id
    '''
    df = pd.read_sql(sql, engine)
    return df.to_dict(orient='records')

def createSecrets(engine, teamId):
    with engine.connect() as con:
        d = { 
            "team_id": teamId,
            "details": json.dumps({}) 
            }
        sql = '''
        INSERT INTO public.secrets(team_id, details) 
        VALUES(:team_id, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        secretId = res.fetchone()[0]
        return secretId

def getSecrets(engine, teamId):
    with engine.connect() as con:
        sql = f'''
        select details
        from "public".secrets as s
        where s.team_id = {teamId}
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            logger.info(f'no secrets, creating...')
            createSecrets(engine, teamId)
            return {}
        return res[0]

def updateSecrets(engine, teamId, details):
    with engine.connect() as con:
        d = { 
            "details": json.dumps(details),
            "team_id": teamId,
            }
        sql = '''
        UPDATE public.secrets
        SET details = :details
        WHERE team_id = :team_id
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        return True

def getStripeApiKey(engine, teamId):
    with engine.connect() as con:
        sql = f'''
        select details
        from "public".secrets as s
        where s.team_id = {teamId}
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            return False
        res = res[0]
        if res.get('stripeApiKey', False):
            return pints.utils.decrypt(res['stripeApiKey'])
        return False

def getSlackInfo(engine, teamId):
    with engine.connect() as con:
        sql = f'''
        select details
        from "public".secrets as s
        where s.team_id = {teamId}
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            return False
        res = res[0]
        if not res.get('slack', False):
            return False
        res = res['slack']
        if res.get('bot_token', False):
            res['bot_token'] = pints.utils.decrypt(res['bot_token'])
            return res
        return False

def getRawTableCount(engine, teamId, table):
    with engine.connect() as con:
        schema = 'public'
        sql = f'''
        select
        count(1) as ct
        from "{schema}"."stripe_{table}"
        where team_id = {teamId}
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            return {'ok': False}
        return res[0]

def getRawTableCounts(engine, teamId):
    schema = 'public'
    tables = ['customers', 'coupons']
    for index, table in enumerate(tables):
        sql += f'''
        select
        '{table}' as "table",
        'raw' as "type",
        count(1) as ct
        from "{schema}"."stripe_{table}"
        where team_id = {teamId}
        '''
        if index < len(tables)-1:
            sql+= 'union all\n'
    logger.info(f'getTableCounts {sql}...')
    df = pd.read_sql(sql, engine)
    df = df.to_json(date_format = 'iso', orient='values', default_handler=str)
    return json.loads(df)

def getDbtTableCounts(engine, teamId):
    tables = ['customers', 'subscriptions', 'mrr_facts']
    sql = ''
    schema = f'team_{teamId}_stripe'
    for index, table in enumerate(tables):
        sql += f'''
        select
        '{table}' as "table",
        'modeled' as "type",
        count(1) as ct
        from "{schema}"."{table}"
        '''
        if index < len(tables)-1:
            sql+= 'union all\n'
    df = pd.read_sql(sql, engine)
    df = df.to_json(date_format = 'iso', orient='values', default_handler=str)
    return json.loads(df)

def getJobSummary(engine, teamId):
    sql = f'''
    select 
	team_id,
	details ->> 'obj' as obj,
	details ->> 'status' as "status",
    details ->> 'type' as "type",
	count(1) as ct,
	max(j.id) as id
	from "public".jobs as j
	where 1=1
	and team_id = {teamId}
	group by
	1, 2, 3, 4
    '''
    df = pd.read_sql(sql, engine)
    return df

def getRecentJobs(engine, teamId):
    sql = f'''
    with jobs2 as (
        select 
        details ->> 'obj' as obj,
        count(1) as ct,
        max(j.id) as id
        from "public".jobs as j
        where details ->> 'status' = 'complete'
        and team_id = {teamId}
        group by
        1
    )

    select 
    j.public_uuid::text as public_uuid,
    details as job
    from jobs2 as j2 inner join
    "public".jobs as j on j.id = j2.id
    '''
    df = pd.read_sql(sql, engine)
    df = df.set_index('public_uuid')
    df = df.to_dict(orient='index')
    return df

def getSchedulerRow(engine):
    sql = '''
    SELECT *
    FROM 
    public.aps_scheduler
    '''
    try:
        df = pd.read_sql(sql, engine)
        return len(df) > 0
    except:
        return False

def truncateTable(engine, table):
    with engine.connect() as con:
        sql = f'''
        TRUNCATE "public".{table}
        '''
        statement = sqlalchemy.sql.text(sql)
        try:
            res = con.execute(statement)
            return res
        except Exception as e:
            return False

def updateJob(engine, teamId, jobId, jobUuid, details):
    logger.info(f'updateJob {jobId} {jobUuid}...')
    with engine.connect() as con:
        d = { 
            "details": json.dumps(details),
            "team_id": teamId,
            "job_id": jobId,
            "public_uuid": jobUuid,
            "status": details['status']
            }
        
        if jobId:
            sql = '''
            UPDATE public.jobs
            SET details = :details,
                status = :status
            WHERE id = :job_id
            '''
            statement = sqlalchemy.sql.text(sql)
            res = con.execute(statement, **d)
            return jobId
        else:
            sql = '''
            INSERT INTO public.jobs(team_id, public_uuid, details) 
            VALUES(:team_id, :public_uuid, :details)
            RETURNING id;
            '''
            statement = sqlalchemy.sql.text(sql)
            res = con.execute(statement, **d).fetchone()
            logger.info(f'updateJob INSERT {res}...')
            return res[0]

def updateJobStatus(engine, jobId, status, error=None, details=None):
    with engine.connect() as con:
        d = { 
            "jobId": jobId,
            "status": status,
            "error": error,
            }
        sql = '''
        UPDATE jobs 
        SET status = :status,
        details = jsonb_set(details, '{status}', to_jsonb((:status)::text))
        where id = :jobId;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        if error:
            sql = '''
            UPDATE jobs 
            SET details = jsonb_set(details, '{error}', to_jsonb((:error)::text))
            where id = :jobId;
            '''
            statement = sqlalchemy.sql.text(sql)
            res = con.execute(statement, **d)
        if details:
            for k, v in details.items():
                logger.info(f'details.items {k} {v}...')
                d2 = {
                    'k': k,
                    'v': v,
                    'jobId': jobId,
                }
                sql = f'''
                UPDATE jobs 
                SET details = jsonb_set(details, '{{{k}}}', to_jsonb('{v}'::text))
                where id = {jobId};
                '''
                res = con.execute(sql)
        logger.info(f'updated job id {jobId}...')
        return True

def getJob(engine, jobUuid):
    with engine.connect() as con:
        sql = f'''
        select details, updated_on
        from public.jobs as j
        where public_uuid = '{jobUuid}'
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            return {'ok': False}
        ret = res[0]
        ret['updated_on'] = res[1].timestamp()
        return {'ok': True, 'job': ret}

def getLastJob(engine, teamId, jobType):
    with engine.connect() as con:
        sql = f'''
        select * 
        from "public".jobs as j
        where j.details ->> 'type' = '{jobType}'
        and j.team_id = {teamId}
        and j.status = 'complete'
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        return res

def addJob(engine, teamId, details, jobUuid):
    with engine.connect() as con:
        d = { 
            "details": json.dumps(details),
            "team_id": teamId,
            "status": details['status'],
            "public_uuid": jobUuid
            }
        sql = '''
        INSERT INTO public.jobs(team_id, public_uuid, status, details) 
        VALUES(:team_id, :public_uuid, :status, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d).fetchone()
        logger.info(f'addJob res {res}...')
        return res[0]

def addMessage(engine, teamId, targetId, message, jobUuid):
    with engine.connect() as con:
        d = { 
            "target_id": targetId,
            "team_id": teamId,
            "details": json.dumps(message),
            "public_uuid": jobUuid
        }
        sql = '''
        INSERT INTO public.message_queue(target_id, team_id, public_uuid, details) 
        VALUES(:target_id, :team_id, :public_uuid, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d).fetchone()
        logger.info(f'addMessage res {res}...')
        return res[0]

def deleteIncompleteJobs(engine):
    with engine.connect() as con:
        sql = '''
        DELETE FROM public.jobs
        WHERE "status" != 'complete'
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement)
        return res

def getMessages(engine):
    with engine.connect() as con:
        trans = con.begin()
        sql = '''
        with q as (
            select 
            jsonb_array_elements_text(mq.details -> 'dependencies')::text as dependency, 
            mq.target_id,
            mq.id
            from public.message_queue as mq 
            where 1=1
        ), c as (
            select j.public_uuid::text, j.status
            from public.jobs as j
        ), q2 as (
            select 
            q.dependency, 
            q.target_id,
            q.id,
            case when c.status = 'complete' then 1 else 0 end as complete
            from
            q inner join  
            c as c on q.dependency = c.public_uuid
        ), q3 as (
            select 
            id,
            count(1) as jobs, 
            sum(complete) as complete
            from q2
            group by 1
            having 
            count(1) = sum(complete)
        )

        DELETE FROM public.message_queue 
        WHERE id = (
        SELECT mq.id
        FROM public.message_queue as mq inner join
        q3 on mq.id = q3.id
        ORDER BY mq.id ASC 
        FOR UPDATE SKIP LOCKED
        LIMIT 1
        )
        RETURNING *;
        '''
        queueRow = con.execute(sql).fetchone()
        trans.commit()
        if queueRow:
            logger.info(f"message_queue process queue id: {queueRow['id']} and target_id: {queueRow['target_id']}...")
            sql = '''
            SELECT * 
            FROM public.jobs as j
            WHERE j.id = %s 
            AND j.status = 'pending' 
            FOR UPDATE;
            '''
            jobRow = con.execute(sql, (queueRow['target_id'],)).fetchone()
            if jobRow:
                logger.info(f"jobRow id: {jobRow['id']}...")
                return jobRow, queueRow
        return False, False

def getAlerts(engine, teamId, lastJob):
    sql = f'''
    select 
    mrr.email, 
    mrr.customer_created_on,
    to_char(mrr.customer_created_on::date, 'Mon dd, yyyy') as customer_created_on2,
    current_date - mrr.customer_created_on::date as created_days_ago,
    mrr.mrr,
    mrr.prev_mrr,
    mrr.mrr_status,
    mrr.mrr_rank,
    mrr.percent_off_precise,
    case
    when mrr.canceled_dt > '{lastJob['details']['maxCanceledOn']}' then 'canceled'
    else 'new'
    end as alert_type
    from team_{teamId}_stripe.mrr_facts as mrr 
    where 
    mrr.current_month = 1
    and (
        mrr.customer_created_on > '{lastJob['details']['maxCreatedOn']}'
        or mrr.canceled_dt > '{lastJob['details']['maxCanceledOn']}'
    )
    order by mrr.created_on desc
    '''
    df = pd.read_sql(sql, engine)
    return df.to_dict(orient='records')