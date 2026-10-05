with

    source as (select * from {{ source("football_data", "SEASONS_RAW") }}),

    stg_seasons as (
        select
            CAST("season_id" as INT) as season_id,
            CAST("season_label" as VARCHAR(15)) as season_label,
            CAST("season_order" as SMALLINT) as season_order,
            CAST("is_fabricated" as BOOLEAN) as is_fabricated
        from source
    )

select *
from stg_seasons
