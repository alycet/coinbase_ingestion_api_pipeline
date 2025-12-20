with distinct_sides as (
    select distinct side
    from coinbase_data.ticker
),

final as (
    select 
    {{ dbt_utils.generate_surrogate_key(['side'])}} as side_key,
    side as side_name
    from distinct_sides
)

select * from final

-- {% if is_incremental() %}
--   where time > (select max(time) from {{ this }})
-- {% endif %}

