import json
import uuid
import altair
import altair_saver
import datetime
import pandas as pd
import pints
from logger import logger

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-setuid-sandbox") 
# chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--remote-debugging-port=9222") 
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
# options.binary_location = '/opt/google/chrome/google-chrome'
service_log_path = "chromedriver.log".format('app')
service_args = ['--verbose']
driver = webdriver.Chrome('/chromedriver/chromedriver',
        chrome_options=chrome_options,
        service_args=service_args,
        service_log_path=service_log_path)

vegaConfig = {
  "view": {
    "stroke": "transparent"
  },
  "axis": {
    "grid": False
  }
}

vegaSpec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "config": vegaConfig,
    "description": "MRR by Month",
    "mark": {
    "type": "line", 
    "tooltip": False, 
    "fill": None, 
    "stroke": "#010101",
    "point": {"color": "#010101"},
    },
    "encoding": {
        "x": {
            "field": "mrr_month_dt", 
            "timeUnit": "yearmonth", 
            "type": "temporal",
            "title": None,
            # "axis": {
            #     "values": [
            #         {"year": 2019, "month": "may", "date": 1},
            #         {"year": 2021, "month": "may", "date": 1}
            #     ]
            #     }
        },
        "y": {
            "field": "mrr", 
            "aggregate": "sum", 
            "type": "quantitative",
            "title": None
        },
    },
    "data": {"values": []},
}

def getMrrFacts(engine, teamId):
    logger.info(f'getMrrFacts... {teamId}')
    sql = '''
    select 
    *,
    1 as active
    from 
    "team_{teamId}_stripe".mrr_facts as mrr
    order by mrr.mrr_dt asc
    '''.format(teamId=teamId)
    df = pd.read_sql(sql, engine)
    piv = df.pivot_table(index='mrr_month_dt', values=['mrr', 'active', 'churned_mrr'], aggfunc='sum')
    return {
        'df': df,
        'summary': piv,
    }
    # df = json.loads(df.to_json(orient='records'))

def getMrrChart(d):
    chartId = uuid.uuid4().hex
    # spec = json.loads(specs['mrr'])
    vegaSpec['data']['values'] = d
    chart = altair.Chart.from_dict(vegaSpec)
    filename = f'./static/{chartId}.png'
    altair_saver.save(chart, filename, method='selenium', webdriver=driver)
    return {'ok': True, 'chartId': chartId, 'filename': filename}

def getCustomerChart(d):
    chartId = uuid.uuid4().hex
    vegaSpec['data']['values'] = d
    vegaSpec['description'] = 'Customers by Month'
    vegaSpec['encoding']['y']['field'] = 'active'
    chart = altair.Chart.from_dict(vegaSpec)
    filename = f'./static/{chartId}.png'
    altair_saver.save(chart, filename, method='selenium', webdriver=driver)
    return {'ok': True, 'chartId': chartId, 'filename': filename}

def getSummary(last3):
    logger.info(f'getSummary... {last3}')
    summary = {}
    dt = datetime.datetime.utcnow()
    curr = last3[2]
    prev = last3[1]
    summary['growthGoal'] = .2
    summary['prcntThruMonth'] = dt.day / 30
    summary['growthGoalNow'] = summary['growthGoal'] * summary['prcntThruMonth']
    
    # mrr
    summary['currentMrr'] = curr['mrr']
    summary['previousMrr'] = prev['mrr']
    summary['mrrGrowth'] = summary['currentMrr'] - summary['previousMrr']
    summary['mrrGrowthPrcnt'] = summary['mrrGrowth'] / summary['previousMrr']
    summary['mrrArrow'] = 'arrow_up'
    if summary['mrrGrowth'] < 0:
        summary['mrrArrow'] = 'arrow_down'
    summary['growthGoalProgress'] = "You're ahead of your goal!"
    if summary['mrrGrowthPrcnt'] < summary['growthGoalNow']:
        summary['growthGoalProgress'] = "You're behind your goal, but lets catch up!"
    summary['currentMrrK'] = round(summary['currentMrr'] / 1000, 1)
    summary['mrrGrowthK'] = round(summary['mrrGrowth'] / 1000, 1)
    summary['mrrGrowthPrcntRounded'] = round(summary['mrrGrowthPrcnt'] * 100, 1)

    summary['mrrMsg'] = f"{summary['growthGoalProgress']} MRR is currently " 
    summary['mrrMsg'] += f"*${summary['currentMrrK']}k* :tada: \n:{summary['mrrArrow']}: "
    summary['mrrMsg'] += f"{summary['mrrGrowthPrcntRounded']}% (${summary['mrrGrowthK']}k) MTD."

    # customers
    summary['currentCustomers'] = curr['active']
    summary['previousCustomers'] = prev['active']
    summary['customerGrowth'] = summary['currentCustomers'] - summary['previousCustomers']
    summary['customerGrowthPrcnt'] = summary['customerGrowth'] / summary['previousCustomers']
    summary['customersArrow'] = 'arrow_up'
    if summary['customerGrowth'] < 0:
        summary['customersArrow'] = 'arrow_down'
    summary['customerGrowthPrcntRounded'] = round(summary['customerGrowthPrcnt'] * 100, 1)
    # \n\n<https://trypaper.io|20% of your customers> account for xx% of your MRR"

    summary['customerMsg'] = f"You currently have {summary['currentCustomers']} customers :tada: \n" 
    summary['customerMsg'] += f":{summary['customersArrow']}: "
    summary['customerMsg'] += f"{summary['customerGrowthPrcntRounded']}% ({summary['customerGrowth']}) MTD."
    return summary

def getSlackMsg(engine, teamId):
    sql = '''
    select 
    *,
    1 as active
    from 
    "team_{teamId}_stripe".mrr_facts as mrr
    order by mrr.mrr_dt asc
    '''.format(teamId=teamId)
    df = pd.read_sql(sql, engine)
    piv = df.pivot_table(index='mrr_month_dt', values=['mrr', 'active', 'churned_mrr'], aggfunc='sum')
    df = json.loads(df.to_json(orient='records'))
    summary = piv.tail(3).to_dict(orient='records')
    logger.info(f"piv summary: {summary}")
    toSlack = {}
    chart = getMrrChart(df)
    toSlack['mrrChartUrl'] = pints.cabinet.file(chart['filename'])
    chart = getCustomerChart(df)
    toSlack['customerChartUrl'] = pints.cabinet.file(chart['filename'])
    try:
        toSlack['summary'] = getSummary(summary)
    except Exception as e:
        logger.error(f"error getting summary: {str(e)}")
        toSlack['summary'] = False
    logger.info(f"piv summary: {toSlack}")
    return toSlack