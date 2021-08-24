import os
import subprocess
import json
import yaml

from logger import logger

def getDbt():
    with open(r'./dbt/models/stripe/models.yml') as file:
        d = yaml.safe_load(file)
        logger.info(f'getDbt: {d}')
    return d

def getCols(sql, cols):
    cols2 = []
    for col in cols:
        # import pdb; pdb.set_trace()
        colFormat = [s for s in sql['selected'] if s['alias'] == col]
        if colFormat:
            colFormat = colFormat[0].get('format', False)
        else:
            colFormat = False
        col2 = {
            'name': col,
            'format': colFormat
            }
        cols2.append(col2)
    return cols2

def runDbt(teamId):
    logger.info(f"run_dbt user: {teamId}")
    os.environ['PAPER_DBT_SCHEMA'] = f"team_{teamId}"
    os.environ['PAPER_DBT_TEAM_ID'] = f"{teamId}"
    session = subprocess.Popen(['./dbt/run_dbt.sh'], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = session.communicate()
    logger.info(f'run_dbt stdout: {stdout}')
    dbtLogs = []
    dbtErrors = []
    if stderr:
        logger.error(f'run_dbt stderr: {stderr}')
    try:
        s = stdout.strip()
        lines = s.splitlines()
        for line in lines:
            j = json.loads(line)
            if j['levelname'] == 'ERROR':
                logger.error(f"run_dbt error: {j['message']}")
                dbtErrors.append(j)
            if 'OK created table' in j['message']:
                count = int(j['message'].split('SELECT')[1].split('\x1b')[0])
                table = j['extra']['unique_id']
                table = table.split('.')
                table = table[len(table)-1]
                print(table, count)
                j['table'] = table
                j['count'] = count
                dbtLogs.append(j)
    except Exception as e:
        logger.error(f'run_dbt log parse error: {e}')
    return dbtLogs, dbtErrors