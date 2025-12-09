
with facts as (
    select 
        trade_id,
        sequence,
        product_id,
        side_key,
        time_key,
        price,
        best_bid,
        best_ask,
        (best_ask - best_bid) as bid_ask_spread,
        (best_ask - best_bid)/((best_ask+best_bid)/2) as bid_ask_spread_pct,
        last_size,
        best_bid_size,
        best_ask_size,
        (best_bid_size + best_ask_size) as liquidity_depth,
        (best_bid_size * best_bid) / (best_ask_size * best_ask) as bid_ask_strength_ratio,
        (best_bid_size / best_ask_size) as market_pressure_indicator
    from {{ref('stg_trades')}}
)

select * from facts