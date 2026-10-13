with

    player as (select * from {{ ref('stg_football_data__PLAYERS_RAW') }}),

    dim_player as (
        select
        {{ dbt_utils.generate_surrogate_key(['p.player_id']) }} as player_key,
        p.player_id,
        p.name,
        p.primary_category
        from player p
    )


select *
from dim_player
