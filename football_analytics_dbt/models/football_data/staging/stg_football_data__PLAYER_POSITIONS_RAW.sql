with

    source as (select * from {{ source("football_data", "PLAYER_POSITIONS_RAW") }}),

    stg_player_positions as (
        select
            cast("player_id" as int) as player_id,
            cast("position_id" as int) as position_id,
            cast("position_rank" as smallint) as position_rank

        from source
    )

select *
from stg_player_positions
