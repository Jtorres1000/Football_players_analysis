with

    source as (select * from {{ source("football_data", "INJURIES_RAW") }}),

    stg_injuries as (
        select
            cast("injury_id" as int) as injury_id,
            cast("player_id" as int) as player_id,
            cast("season_id" as int) as season_id,
            cast("injury_type" as varchar(100)) as injury_type,
            cast("start_date" as date) as start_date,
            cast("end_date" as date) as end_date,
            cast(datediff('day', cast("start_date" as date), cast("end_date" as date)) as smallint) as days_out

        from source
    )

select *
from stg_injuries
