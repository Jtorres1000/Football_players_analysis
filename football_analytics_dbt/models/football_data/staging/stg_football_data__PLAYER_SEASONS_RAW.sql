with

    source as (select * from {{ source("football_data", "PLAYER_SEASONS_RAW") }}),

    stg_player_seasons as (
        select
            cast("player_season_id" as int) as player_season_id,
            cast("player_id" as int) as player_id,
            cast("season_id" as int) as season_id,
            cast("club_id" as int) as club_id,
            cast("age" as smallint) as age,
            cast("mins" as int) as mins,
            cast("starts" as smallint) as starts,
            cast(coalesce("sub_appearances", 0) as smallint) as sub_appearances,
            cast("ability_score" as numeric(7, 2)) as ability_score

        from source
    )

select *
from stg_player_seasons
