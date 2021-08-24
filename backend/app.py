from flask import Flask
import flask

import json
import os
import sys
import uuid
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
import sqlalchemy
import pandas as pd
import yaml
import subprocess

from magic_admin import Magic
from magic_admin.error import DIDTokenError
from magic_admin.error import RequestError

from logger import logger


SQLALCHEMY_DATABASE_URI = os.environ.get('PAPER_SQLALCHEMY_DATABASE_URI')
PAPER_MAGIC_SECRET_KEY = os.environ.get('PAPER_MAGIC_SECRET_KEY')
PAPER_API_KEY = os.environ.get('PAPER_API_KEY', False)
# SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

session_options = {
    'autocommit': True
}
db = SQLAlchemy(app, session_options=session_options)

import pints
from metrics import metrics

# dbUser = pints.postgres.createReadOnlyUser(db.engine, 10)
pints.stripe.getAll(db.engine, 23)

pints.scheduler.startScheduler()

# pints.sheets.test('1JoXzCGI61dTfWohBJmlW7kBXexNl2ws863MvfFUpvLU')

def getTeamDomain(email):
    return email.split('@')[1]

def checkForTeam(engine, email, userId):
    domain = getTeamDomain(email)
    sql = '''
    SELECT 
    u.id as user_id, t.id as team_id
    FROM 
    public.users as u inner join
    public.team_membership as tm on u.id = tm.user_id inner join
    public.teams as t on tm.team_id = t.id
    WHERE 
    t.domain = '{domain}'
    order by u.created_on desc
    '''.format(domain = domain)
    df = pd.read_sql(sql, db.engine)
    if len(df) > 0:
        logger.info(f'already team for {domain}')
    else:
        logger.info(f'no team for {domain}, creating...')
        teamId = pints.postgres.insertTeam(engine, domain)
        logger.info(f'adding user to team {teamId}...')
        teamMembershipId = pints.postgres.insertTeamMember(engine, teamId, userId)
        logger.info(f'teamMembershipId: {teamMembershipId}.')
        dbUser = pints.postgres.createReadOnlyUser(engine, teamId)
        logger.info(f'dbUser user {dbUser}...')
    return True

@app.route('/ping', methods=["GET"])
def ping():
    j = {'ok': True}
    return json.dumps(j), 200, {'ContentType':'application/json'}

@app.route('/get_stripe', methods=["GET", "POST"])
def get_stripe():
    data = flask.request.get_json()
    logger.info(f'get_stripe: {data}')
    user = getUser(data)
    jobIds = pints.stripe.getAll(db.engine, user['team_id'])
    return json.dumps({'ok' : True, 'jobIds': jobIds}), 200, {'ContentType':'application/json'}

@app.route('/get_dbt', methods=["GET", "POST"])
def get_dbt():
    data = flask.request.get_json()
    logger.info(f'get_dbt: {data}')
    user = getUser(data)
    d = pints.modeling.getDbt()
    return json.dumps({'ok' : True, 'data': d}), 200, {'ContentType':'application/json'}

@app.route('/get_raw_counts', methods=["GET", "POST"])
def get_raw_counts():
    data = flask.request.get_json()
    logger.info(f'get_raw_counts: {data}')
    user = getUser(data)
    counts = pints.postgres.getRawTableCounts(db.engine, user['team_id'])
    return json.dumps({'ok' : True, 'counts': counts}), 200, {'ContentType':'application/json'}

@app.route('/run_dbt', methods=["GET", "POST"])
def run_dbt():
    data = flask.request.get_json()
    logger.info(f'run_dbt: {data}')
    user = getUser(data)
    dbtLogs, dbtErrors = pints.modeling.runDbt(user['team_id'])
    return json.dumps({
        'ok' : True, 
        'dbtLogs': dbtLogs, 
        'dbtErrors': dbtErrors
        }), 200, {'ContentType':'application/json'}

@app.route('/run_analysis', methods=["GET", "POST"])
def run_analysis():
    data = flask.request.get_json()
    user = getUser(data)
    logger.info(f'run_analysis...')
    if data['analysis']['mode'] == 'search':
        dbtModel = pints.yaml2sql.dbt2Sql(data['dbt'], f"team_{user['team_id']}_stripe")
        sql = dbtModel['sql']
        userEngine = db.engine
    else:
        sql = data['analysis']['code']
        userPass = os.environ.get('PAPER_READONLY_PASSWORD')
        db_url = f"postgresql://team_{user['team_id']}_readonly:{userPass}@oregon-postgres.render.com/paperdb"
        # logger.info(f'db_url: {db_url}')
        userEngine = sqlalchemy.create_engine(db_url, connect_args={'options': f"-csearch_path=team_{user['team_id']}_stripe"})
        dbtModel = {'sql': sql}
    logger.info(f'run_analysis sql: {sql}')
    
    try:
        df = pd.read_sql(sql, userEngine)
    except Exception as e:
        logger.error(f'run_analysis error: {e}')
        return {
            'ok': False,
            'error': str(e),
            'sql': dbtModel,
        }
    logger.info(f'run_analysis df: {df.head()}')
    cols = df.columns.tolist()
    
    if data['analysis']['mode'] == 'search':
        cols2 = pints.modeling.getCols(dbtModel, cols)
    else:
        cols2 = [{'name': col, 'format': ''} for col in cols]
    df = df.to_json(date_format = 'iso', orient='values',
        default_handler=str)
    return json.dumps(
        {
            'ok' : True,
            'sql': dbtModel,
            'rows': json.loads(df, strict=False),
            'cols': cols2,
        }), 200, {'ContentType':'application/json'}

def getUser(data):
    logger.debug(f'getUser: {data}')
    publicAddress = data['user'].get('publicAddress', False)
    if not publicAddress:
        logger.error(f'no publicAddress: {data}')
        d = {
            'ok': False,
            'reason': 'noPublicAddress'
        }
        return d
    sql = '''
    SELECT 
    u.id as user_id, u.email, u.details, tm.team_id as team_id
    FROM 
    public.users as u left join
    public.team_membership as tm on u.id = tm.user_id
    WHERE 
    u.details ->> 'publicAddress' = '{publicAddress}'
    order by tm.created_on desc
    limit 1
    '''.format(publicAddress = publicAddress)
    df = pd.read_sql(sql, db.engine)
    if len(df) == 0:
        d = {
            'ok': False,
            'reason': 'noUser'
        }
        return d
    else:
        return json.loads(df.to_json(orient='records'))[0]


@app.route('/update_settings', methods=["GET", "POST"])
def update_settings():
    data = flask.request.get_json()
    logger.info(f"update_settings: {data}")
    user = getUser(data)
    pints.postgres.updateSettings(db.engine, user['team_id'], data['user']['settings'])
    ret = {'ok': True}
    return json.dumps(ret), 200, {'ContentType':'application/json'} 

@app.route('/update_secret', methods=["GET", "POST"])
def update_secret():
    data = flask.request.get_json()
    logger.info(f"update_secret: {data}")
    if data['type'] == 'stripe':
        user = getUser(data)
        keyTest = pints.stripe.testKey(data['stripeApiKey'])
        if keyTest['ok']:
            secrets = pints.postgres.getSecrets(db.engine, user['team_id'])
            secrets['stripeApiKey'] = pints.utils.encrypt(data['stripeApiKey'])
            pints.postgres.updateSecrets(db.engine, user['team_id'], secrets)
            jobIds = pints.stripe.getAll(db.engine, user['team_id'])
            keyTest['jobIds'] = jobIds
        return json.dumps(keyTest), 200, {'ContentType':'application/json'} 
    elif data['type'] == 'sheets':
        logger.info(f"update_secret sheets...")
        user = getUser(data)
        logger.info(f"update_secret sheets...")
        secrets = pints.postgres.getSecrets(db.engine, user['team_id'])
        sheets = pints.utils.encrypt(data['secret'])
        secrets['sheets'] = sheets
        pints.postgres.updateSecrets(db.engine, user['team_id'], secrets)
        logger.info(f"update_secret slackAuth success...")
    elif data['type'] == 'slack':
        logger.info(f"update_secret slack...")
        user = getUser(data)
        slackAuth = pints.slack.getToken(data['code'])
        logger.info(f"update_secret slackAuth...")
        if slackAuth.get('bot_token', False):
            logger.info(f"update_secret slackAuth has token...")
            secrets = pints.postgres.getSecrets(db.engine, user['team_id'])
            slackAuth['bot_token'] = pints.utils.encrypt(slackAuth['bot_token'])
            secrets['slack'] = slackAuth
            pints.postgres.updateSecrets(db.engine, user['team_id'], secrets)
            logger.info(f"update_secret slackAuth success...")
    return json.dumps({'ok': True}), 200, {'ContentType':'application/json'} 

@app.route('/get_recent_jobs', methods=["GET", "POST"])
def get_recent_jobs():
    data = flask.request.get_json()
    user = getUser(data)
    jobs = pints.postgres.getRecentJobs(db.engine, user['team_id'])
    for key, job in jobs.items():
        logger.info(f'get_recent_jobs job: {job}')
        logger.info(f'get_recent_jobs job: {key}')
        if 'job' in job and 'obj' in job['job']:
            job['jobId'] = str(key)
            logger.info(f'job: {job}')
            job['job']['count'] = pints.postgres.getRawTableCount(db.engine, 
                user['team_id'], job['job']['obj'])
            jobs[key] = job['job']
    return json.dumps({'ok': True, 'jobs': jobs}), 200, {'ContentType':'application/json'}

@app.route('/get_job', methods=["GET", "POST"])
def get_job():
    data = flask.request.get_json()
    job = pints.postgres.getJob(db.engine, data['jobId'])
    if job['ok'] and job['job']['status'] == 'complete' and job['job']['type'] == 'stripe':
        user = getUser(data)
        job['job']['count'] = pints.postgres.getRawTableCount(db.engine, 
                    user['team_id'], job['job']['obj'])
    return json.dumps(job), 200, {'ContentType':'application/json'}

@app.route('/login', methods=["GET", "POST"])
def login():
    logger.info(f'login...')
    data = flask.request.get_json()
    email = data.get('email', None)
    apiKey = data.get('apiKey', None)
    did_token = data.get('idToken', None)
    if not did_token and not apiKey:
        d = {
            'ok': False,
            'new': False,
            'error': 'noAuth'
        }
        return json.dumps(d), 200, {'ContentType':'application/json'}
    magic = Magic(api_secret_key=PAPER_MAGIC_SECRET_KEY)
    if PAPER_API_KEY and apiKey == PAPER_API_KEY:
        logger.info(f'using apiKey...')
        publicAddress = data['publicAddress']
        issuer = 'api'
    else:
        try:
            magic.Token.validate(did_token)
            issuer = magic.Token.get_issuer(did_token)
            publicAddress = data['publicAddress']
        except DIDTokenError as e:
            logger.error(f'DID Token is invalid: {e}')
            d = {
                'ok': False,
                'new': False,
                'error': 'DID Token is invalid'
            }
            return json.dumps(d), 200, {'ContentType':'application/json'}
        except RequestError as e:
            logger.error(f'RequestError: {e}')
            d = {
                'ok': False,
                'new': False,
                'error': 'noAuth'
            }
            return json.dumps(d), 200, {'ContentType':'application/json'}
    sql = '''
    SELECT 
    u.id as user_id, 
    u.email, 
    u.details,
    t.details as settings,
    case when s.details ->> 'stripeApiKey' is not null then 1 else 0 end as has_stripe,
    (SELECT EXISTS (
	   SELECT FROM information_schema.tables 
	   WHERE  table_schema = 'team_'|| tm.team_id || '_stripe'
	   AND    table_name   = 'mrr_facts'
	)) as has_mrr_facts
    FROM 
    public.users as u left join
    public.team_membership as tm on u.id = tm.user_id left join
    public.teams as t on tm.team_id = t.id left join
    public.secrets as s on tm.team_id = s.team_id
    WHERE 
    u.details ->> 'publicAddress' = '{publicAddress}'
    order by u.created_on desc
    limit 1
    '''.format(publicAddress = publicAddress)
    df = pd.read_sql(sql, db.engine)
    if len(df) > 0:
        user = df.details[0]
        email = df.email[0]
        validIssuer = user['issuer'] == issuer
        if not validIssuer and not issuer == 'api':
            logger.info(f'Invalid issuer: {email} {issuer}')
            d = {
                'ok': False,
                'new': False,
                'user': False,
                'error': 'invalid_issuer'
                }
            return json.dumps(d), 200, {'ContentType':'application/json'}
        logger.info(f'issuer {issuer} is valid? {validIssuer}')
        user['settings'] = df.settings[0]
        user['hasStripe'] = bool(df.has_stripe[0] > 0)
        user['hasMrrFacts'] = bool(df.has_mrr_facts[0])
        d = {
            'ok': True,
            'new': False,
            'user': user
        }
    else:
        userId = pints.postgres.insertUser(db.engine, email, data)
        checkForTeam(db.engine, email, userId)
        d = {
            'ok': True,
            'new': True
        }
    return json.dumps(d), 200, {'ContentType':'application/json'}

@app.route('/get_funders', methods=["GET", "POST"])
def get_funders():
    data = flask.request.get_json()
    sql = '''
    SELECT 
    f.public_id,
    f.name,
    f.domain,
    f.max_loan_amount,
    f.min_loan_amount,
    f.min_annual_revenue,
    f.paper_rank,
    f.focus,
    f.max_mrr_multiple,
    f.loan_type,
    f.payment_details,
    f.saas_focus,
    f.warrants,
    f.region,
    f.personal_guarantor,
    f.days_to_close,
    cb."data"
    FROM 
    public.funders as f left join
    public.clearbit as cb on f."domain" = cb."domain"
    WHERE f.active = '1'
    and f.loan_type != 'Shared Earnings'
    order by f.paper_rank desc
    ;
    '''.format(active = 1)
    df = pd.read_sql(sql, db.engine)
    cols = json.loads(df.dtypes.to_json())
    d = {
        'ok': True, 
        'data': json.loads(df.to_json(orient='records')),
        'columns': cols
    }
    return json.dumps(d), 200, {'ContentType':'application/json'}

@app.route('/update_user_data', methods=["GET", "POST"])
def update_user_data():
    data = flask.request.get_json()
    logger.info(f'update_user_data: {data}')
    publicAddress = data['user'].get('publicAddress', False)
    if not publicAddress:
        d = {
            'ok': False,
            'reason': 'noUser'
        }
        return json.dumps(d), 200, {'ContentType':'application/json'}
    sql = '''
    SELECT 
    u.id as user_id, u.email, u.details, ud.details as user_data
    FROM 
    public.users as u left join
    public.user_data as ud on u.id = ud.user_id
    WHERE 
    u.details ->> 'publicAddress' = '{publicAddress}'
    order by u.created_on desc
    '''.format(publicAddress = publicAddress)
    df = pd.read_sql(sql, db.engine)
    if len(df) == 0:
        d = {
            'ok': False,
            'reason': 'noUser'
        }
        return json.dumps(d), 200, {'ContentType':'application/json'}
    with db.engine.connect() as con:
        d = { "user_id": int(df.user_id[0]), "details": json.dumps(data['userData']) }
        sql = '''
        INSERT INTO public.user_data(user_id, details) 
        VALUES(:user_id, :details)
        ON CONFLICT (user_id) DO UPDATE
        SET details = :details
        '''
        statement = sqlalchemy.sql.text(sql)
        con.execute(statement, **d)
    return json.dumps(d), 200, {'ContentType':'application/json'}

# CREATE TABLE public.applications (
#     id    SERIAL PRIMARY KEY,
#     public_uuid uuid DEFAULT uuid_generate_v1(),
#     user_id integer,
#     created_on timestamp DEFAULT current_timestamp,
#     updated_on timestamp DEFAULT current_timestamp,
#     details JSONB
# );

@app.route('/get_events', methods=["GET", "POST"])
def get_events():
    data = flask.request.get_json()
    logger.info(f'get_events: {data}')
    user = getUser(data)
    logger.info(f'get_events user: {user}')
    sql = '''
    select 
    *
    from 
    "team_{teamId}_stripe".events as e
    order by e.created_on desc
    limit 100
    '''.format(teamId=user['team_id'])
    try:
        df = pd.read_sql(sql, db.engine)
    except Exception as e:
        logger.error(f'get_events error: {e}')
        ret = {
            'ok': False, 
            'error': 'noData',
        }
        return json.dumps(ret), 200, {'ContentType':'application/json'}
    df = pd.read_sql(sql, db.engine)
    df = json.loads(df.to_json(orient='records'))
    ret = {
        'ok': True, 
        'data': df,
        }
    return json.dumps(ret), 200, {'ContentType':'application/json'}

@app.route('/get_metrics', methods=["GET", "POST"])
def get_metrics():
    data = flask.request.get_json()
    logger.info(f'get_metrics: {data}')
    user = getUser(data)
    logger.info(f'get_metrics user: {user}')
    sql = '''
    select 
    *,
    1 as active
    from 
    "team_{teamId}_stripe".mrr_facts as mrr
    order by mrr.mrr_dt asc
    '''.format(teamId=user['team_id'])
    try:
        df = pd.read_sql(sql, db.engine)
        df['mrr_month_dt'] = df.mrr_month_dt + pd.Timedelta(hours=12)
    except Exception as e:
        logger.error(f'get_metrics error: {e}')
        ret = {
            'ok': False, 
            'error': 'noData',
        }
        return json.dumps(ret), 200, {'ContentType':'application/json'}
    piv = df.pivot_table(index='mrr_month_dt', values=['mrr', 'active', 'churned_mrr'], aggfunc='sum')
    df = json.loads(df.to_json(orient='records'))
    sql = '''
    with c1 as (
        select 
        sum(mrr.churned_mrr) / (sum(mrr.mrr) / 3) as churn_rate,
        sum(mrr.churned_mrr) as churned_mrr,
        sum(mrr.mrr) as mrr,
        avg(mrr.mrr) as avg_mrr,
        sum(mrr.mrr) / count(1) as arpu
        
        from 
        "team_{teamId}_stripe".mrr_facts as mrr
        where mrr.current_month = 0
        and mrr.mrr_month_dt > current_timestamp - interval '4 months'
    )
    select 
    *, 
    100 / (churn_rate*100) as lifetime_months,
    100 / (churn_rate*100) * avg_mrr as clv
    from c1;
    '''.format(teamId=user['team_id'])
    ltv = pd.read_sql(sql, db.engine)
    ltv = json.loads(ltv.to_json(orient='records'))[0]
    sql = '''
    with mrr as (
        select
        mrr.mrr_month_dt,
        mrr.customer_created_on,
        date_trunc('month', mrr.customer_created_on)::date::text as vintage,
        vintage_age,
        mrr.mrr
        from 
        "team_{teamId}_stripe".mrr_facts as mrr
        where customer_created_on > (current_timestamp - interval '13 months')
    ), vintage_start as (
        select
        vintage,
        sum(mrr.mrr) as starting_mrr,
        count(1) as starting_customers
        from 
        mrr as mrr
        where mrr.vintage_age = 0
        group by 1
    ), vintage_perf as (
        select
        vintage,
        vintage_age,
        sum(mrr.mrr) as mrr,
        count(1) as customers
        from 
        mrr as mrr
        group by 1, 2
    ), res as (
        select 
        vp.vintage, 
        vp.vintage_age,
        vp.customers,
        vp.mrr,
        (vp.mrr * 100.0 / vs.starting_mrr) / 100 as revenue_retention,
        (vp.customers * 100.0 / vs.starting_customers) / 100 as customer_retention
        from vintage_perf vp join
        vintage_start as vs on vp.vintage = vs.vintage
        order by vp.vintage, vp.vintage_age
    )
    select *,
    round((revenue_retention*100)::decimal, 0)::text as revenue_retention_text,
    round((customer_retention*100)::decimal, 0)::text as customer_retention_text
    from res
    '''.format(teamId=user['team_id'])
    retention = pd.read_sql(sql, db.engine)
    retention = json.loads(retention.to_json(orient='records'))

    ret = {
        'ok': True, 
        'data': df,
        'ltv': ltv,
        'retention': retention,
        'summary': piv.tail(3).to_dict(orient='records')
        }
    return json.dumps(ret), 200, {'ContentType':'application/json'}

@app.route('/to_slack', methods=["GET", "POST"])
def to_slack():
    data = flask.request.get_json()
    logger.info(f'to_slack: {data}')
    publicId = uuid.uuid4().hex
    return json.dumps({'ok' : True}), 200, {'ContentType':'application/json'}