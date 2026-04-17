{{ config(materialized='table') }}

--Select the newest record for each item_id to have the most up-to-date value for each unique item
select distinct on (item_id)
    item_id,
    high_alch_value,
    low_alch_value,
    base_value
from {{ ref('staging_rs_item_details') }}
order by item_id, insertion_timestamp desc
