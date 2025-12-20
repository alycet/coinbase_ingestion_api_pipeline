
with source as (
    select * from coinbase_data.ticker
),

renamed as (
    select
        trade_id,
        sequence,
        {{ dbt_utils.generate_surrogate_key(['product_id'])}} as product_id,
        {{ dbt_utils.generate_surrogate_key(['side'])}} as side_key,
        {{ dbt_utils.generate_surrogate_key(['time', 'trade_id'])}} as time_key,
        cast(price as numeric) as price,
        cast(open_24h as numeric) as open_24h,
        cast(volume_24h as numeric) as volume_24h ,
        cast(low_24h as numeric) as low_24h,
        cast(high_24h as numeric) as high_24h,
        cast(volume_30d as numeric) as volume_30d,
        cast(best_bid as numeric) as best_bid,
        cast(best_bid_size as numeric) as best_bid_size,
        cast(best_ask as numeric) as best_ask,
        cast(best_ask_size as numeric) as best_ask_size,
        cast(last_size as numeric) as last_size
    from source

)

select * from renamed

-- {% if is_incremental() %}
--   where time > (select max(time) from {{ this }})
-- {% endif %}
