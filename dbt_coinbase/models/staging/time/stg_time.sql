with time_table as (
    select
        {{dbt_utils.generate_surrogate_key(['time', 'trade_id'])}} as time_key,
        date(time) as trade_date,
        extract(hour from timestamp(time)) as trade_hour,
        extract(minute from timestamp(time)) as trade_minute,
        extract(second from timestamp(time)) as trade_second,
        format_timestamp('%A', timestamp(time)) as trade_day_of_week,
        extract(week from date(time)) as trade_week,
        extract(month from date(time)) as trade_month,
        extract(quarter from date(time)) as trade_quarter,
        extract(year from date(time)) as trade_year     
    from coinbase_data.ticker
)

select * from time_table