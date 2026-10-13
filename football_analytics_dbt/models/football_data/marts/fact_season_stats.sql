with

    players_season as (select * from {{ ref('stg_football_data__PLAYER_SEASONS_RAW') }}),
    
    fact_season_stats as (
        select
        {{dbt_utils.generate_surrogate_key(['ps.player_season_id']) }} as player_season_key,
        {{dbt_utils.generate_surrogate_key(['ps.player_id']) }} as player_key,
        {{dbt_utils.generate_surrogate_key(['ps.season_id']) }} as season_key,
        ability_score,
        from players_season ps

    )

select *
from fact_season_stats
