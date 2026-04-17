{{
  config(
    materialized='incremental',
    unique_key='transaction_id',
    incremental_strategy='delete+insert'
  )
}}


with prices as (
    select * from {{ ref('staging_price') }}
    {% if is_incremental() %}
      where insertion_timestamp > (select max(insertion_timestamp) from {{ this }})
    {% endif %}
),

item_details as (
    select * from {{ ref('staging_rs_item_details') }}
),

nature_rune_cost as (
    select average_low_price as cost
    from {{ ref('staging_price') }}
    where item_id = 561
    order by insertion_timestamp desc
    limit 1
)

select 
    {{ dbt_utils.generate_surrogate_key(['p.item_id', 'p.insertion_timestamp']) }} as transaction_id,
    p.high_price_volume_5m,
    p.low_price_volume_5m,
    p.average_high_price,
    p.average_low_price,
    p.insertion_timestamp,
    -- Calculate GE Tax
    case 
        when (p.average_high_price * 0.02) > 5000000 then 5000000
        else floor(p.average_high_price * 0.02)
    end as ge_tax,
    -- Calculate Margin (using the tax logic above)
    ((p.average_high_price - (case when (p.average_high_price * 0.02) > 5000000 then 5000000 else floor(p.average_high_price * 0.02) end)) - p.average_low_price) as net_ge_margin,
    -- Calculate Alch Profit
    (i.high_alch_value - p.average_low_price - (select cost from nature_rune_cost)) as alch_profit,
    p.item_id as item_id_fkey
from prices p
left join item_details i on p.item_id = i.item_id
