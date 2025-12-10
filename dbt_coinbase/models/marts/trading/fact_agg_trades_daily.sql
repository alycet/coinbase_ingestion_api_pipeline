
with base as (
    select 
        tr.*,
        ti.trade_date,
        s.side_name
    from {{ ref('stg_trades')}} tr
    join {{ref('stg_time')}} ti
        on tr.time_key = ti.time_key
    join {{ref('stg_sides')}} s
        on tr.side_key = s.side_key
    
),

daily_agg as (
    select 
        product_id,
        trade_date,
        --price measures
        avg(price) as average_price,
        min(price) as min_price,
        max(price) as max_price,
        sum(price * last_size) / SUM(last_size) as vol_weighted_avg_price,
        --volume_30d,
        --volume meaures
        sum(last_size) as total_trade_volume,
        avg(last_size) as avg_trade_volume,
        sum(case when side_name = 'buy' then last_size else 0 end) as buy_volume,
        sum(case when side_name = 'sell' then last_size else 0 end) as sell_volume,
        --volatility measures
        (max(price) - min(price)) as high_low_range,
        (max(price) - min(price)/ min(price)) * 100 as high_low_range_prcnt,
        --time based measures
        count(*) as trade_count,
        count(*) / 1440.0 as trades_per_minute,
        count(*) / 24.0 as trades_per_hour,
        --buy/ sell aggregates
        sum(case when side_name = 'buy' then 1 else 0 end) as buy_trade_count,
        sum(case when side_name = 'sell' then 1 else 0 end) as sell_trade_count,
        cast(sum(case when side_name = 'buy' then 1 else 0 end) as float64)/count(*) as buy_ratio,
        cast(sum(case when side_name = 'buy' then last_size else 0 end) as float64) / sum(last_size) as buy_volume_ratio,
        cast(sum(case when side_name = 'sell' then last_size else 0 end) as float64) / sum(last_size) as sell_pressure_index,
    from base
    group by 1,2

)

select * from daily_agg

