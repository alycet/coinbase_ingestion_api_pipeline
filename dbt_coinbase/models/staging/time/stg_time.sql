with time_table as (
    select
        {{dbt_utils.generate_surrogate_key(['time'])}} as time_key,
        date(time) as date,
        extract(hour from timestamp(time)) as hour,
        extract(minute from timestamp(time)) as minute,
        extract(second from timestamp(time)) as second,
        format_timestamp('%A', timestamp(time)) as day_of_week,
        extract(week from date(time)) as week,
        extract(month from date(time)) as month,
        extract(quarter from date(time)) as quarter,
        extract(year from date(time)) as year     
    from coinbase_data.ticker
)

select * from time_table