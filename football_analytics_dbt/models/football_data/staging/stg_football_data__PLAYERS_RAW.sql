with

    source as (select * from {{ source("football_data", "PLAYERS_RAW") }}),

    stg_players as (
        select
           
            cast("player_id" as int) as player_id,
            cast("name" as varchar(150)) as name,
            cast("nation_id" as int) as nation_id,
            cast("height_cm" as smallint) as height_cm,
            cast("weight_kg" as smallint) as weight_kg,
            cast("is_eu_national" as boolean) as is_eu_national,
            cast("primary_category" as varchar(12)) as primary_category,
            cast("agent_id" as int) as agent_id

        from source
    )

select *
from stg_players
