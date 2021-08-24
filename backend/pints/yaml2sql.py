import yaml
from logger import logger

def getYaml(s):
    return yaml.safe_load(s)

def getAlias(column, dimOrMeas):
    a = column.get('meta', {}).get(dimOrMeas, {'label': column['name']})['label']
    print('alias:', a)
    return a

def getMeasAlias(measure, name):
    return measure.get('label', name)

def getDimSql(model, selected, column):
    logger.info(f'column: {column}')
    timeframe = column.get('meta', {}).get('dimension', {}).get('timeframe', False)
    colFormat = column.get('meta', {}).get('dimension', {}).get('format', False)
    if timeframe in ['year', 'month', 'day']:
        addSql = f"date_trunc('{timeframe}', {model['name']}.{column['name']})::date::text"
    elif timeframe:
        addSql = f"date_trunc('{timeframe}', {model['name']}.{column['name']})"
    else:
        addSql = f"{model['name']}.{column['name']}"
    if len(selected) > 0:
        addSql = f'\n,{addSql}'
    # return addSql
    return {
        'sql': addSql, 
        'format': colFormat, 
        'column': column,
        'dimOrMeas': 'dimension'
        }

def getMeasSql(model, selected, measure, name, column):
    alias = getMeasAlias(measure, name)
    agg = measure.get('type', False)
    colFormat = measure.get('format', False)
    if agg:
        addSql = f'''{agg}({model['name']}.{column['name']}) as "{alias}"'''
        if len(selected) > 0:
            addSql = f'\n,{addSql}'
    sqlAgg = measure.get('sql', False)
    # TODO: implement custom sql aggs
    if sqlAgg:
        addSql = f'''{sqlAgg} as "{alias}"'''
        if len(selected) > 0:
            addSql = f'\n,{addSql}'
    # import pdb; pdb.set_trace()
    return {
        'sql': addSql, 
        'format': colFormat, 
        'alias': alias, 
        'column': name,
        'dimOrMeas': 'measure'
    }

def dbt2Sql(d, schema):
    sql = 'select\n'
    selected = []
    tables = []
    tableNames = []
    groupBy = '\ngroup by\n'
    orderBy = '\norder by\n'
    hasOrder = False
    hasGroup = False
    for model in d['models']:
        for column in model.get('columns', []):
            dimension = column.get('meta', {}).get('dimension', {})
            if dimension.get('selected', False):
                alias = getAlias(column, 'dimension')
                dim = getDimSql(model, selected, column)
                dim['alias'] = alias
                addSql = dim['sql']
                groupBy+=addSql
                hasGroup = True
                if dimension.get('order_by', False):
                    hasOrder = True
                    orderBy+= f"{addSql} {dimension.get('order_by', 'asc')}"
                addSql = f'{addSql} as "{alias}"'
                sql+=addSql
                selected.append(dim)
                if model['name'] not in tableNames:
                    tables.append(model)
                    tableNames.append(model['name'])
    for model in d['models']:
        for column in model.get('columns', []):
            measures = column.get('meta', {}).get('measures', {})
            for key, measure in measures.items():
                if measure.get('selected', False):
                    meas = getMeasSql(model, selected, measure, key, column)
                    addSql = meas['sql']
                    selected.append(meas)
                    sql+=addSql
                    if model['name'] not in tableNames:
                        tables.append(model)
                        tableNames.append(model['name'])
    sql+= '\nfrom\n'
    join = False
    for idx, table in enumerate(tables):
        logger.info(f'table: {table}')
        sql+= f"{schema}.{table['name']} as {table['name']}"
        if join:
            sql+= f" on {join}"
            join = False
        if idx < len(tables)-1:
            defaultJoin = [{'sql_on': '1=1'}]
            join = table['meta'].get('joins', defaultJoin)[0]['sql_on']
            # TODO: support multiple joins
            sql+= f" left join \n"
            logger.info(f'adding join: {join}')
        
    if hasGroup:
        sql+= groupBy
    if hasOrder:
        sql+= orderBy
    return {
        'sql': sql,
        'selected': selected
    }
