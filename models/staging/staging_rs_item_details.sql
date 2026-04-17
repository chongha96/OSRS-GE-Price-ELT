{{ config(materialized='table') }}

select
    -- Generates a unique ID based on the item and the timestamp
    cast(id as int) as item_id,
    cast(examine as text) as examine_text,
    cast(members as boolean) as is_members,
    cast(lowalch as int) as low_alch_value,
    cast(highalch as int) as high_alch_value,
    cast(trade_limit as int) as trade_limit_6h,
    cast(value as int) as base_value,
    cast(icon as text) as item_icon,
    cast(name as text) as item_name,
    cast(inserted_at as timestamp) as insertion_timestamp
FROM {{ source('ge_tracker', 'rs_item_details') }}
