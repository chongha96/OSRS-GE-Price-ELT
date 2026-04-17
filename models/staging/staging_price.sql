{{ config(materialized='table') }}


select
    cast(item_id as int) as item_id,
    cast(high_price_volume as bigint) as high_price_volume_5m,
    cast(low_price_volume as bigint) as low_price_volume_5m,
    cast(average_high_price as bigint) as average_high_price,
    cast(average_low_price as bigint) as average_low_price,
    cast(inserted_at as timestamp) as insertion_timestamp
FROM {{ source('ge_tracker', 'prices') }}



