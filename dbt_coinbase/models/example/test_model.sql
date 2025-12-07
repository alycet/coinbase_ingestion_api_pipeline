{{ config(
    materialized='table',
    schema = 'prod'
    ) }}

select * from coinbase_data.ticker limit 10