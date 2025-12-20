with distinct_products as (
    select distinct product_id as product_name
    from coinbase_data.ticker
),

final_product_table as (
    select 
    {{ dbt_utils.generate_surrogate_key(['product_name'])}} as product_id,
    product_name,
    split(product_name, '-')[OFFSET(0)] AS base_currency,
    split(product_name, '-')[OFFSET(1)] AS quote_currency

    from distinct_products
)

select * from final_product_table

-- {% if is_incremental() %}
--   where time > (select max(time) from {{ this }})
-- {% endif %}

