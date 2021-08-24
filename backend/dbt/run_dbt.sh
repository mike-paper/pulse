#!/bin/bash
# echo $PAPER_DBT_SCHEMA
cd dbt
# dbt --log-format json run --profiles-dir . --model mrr_facts
dbt --log-format json run --profiles-dir . 