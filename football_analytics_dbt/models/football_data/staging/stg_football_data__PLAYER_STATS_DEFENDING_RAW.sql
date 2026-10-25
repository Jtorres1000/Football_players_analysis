with

    source as (select * from {{ source("football_data", "PLAYER_STATS_DEFENDING_RAW") }}),

    stg_player_stats_defending as (
        select
            cast("player_season_id" as int) as player_season_id,
            cast(coalesce("tackles_completed", 0) as smallint) as tackles_completed,
            cast(coalesce("tackles_completed_per_90", 0) as numeric(5, 3)) as tackles_completed_per_90,
            cast(coalesce("tackles_attempted", 0) as smallint) as tackles_attempted,
            cast(coalesce("tackle_completion_ratio", 0) as numeric(5, 4)) as tackle_completion_ratio,
            cast(coalesce("key_tackles", 0) as smallint) as key_tackles,
            cast(coalesce("key_tackles_per_90", 0) as numeric(5, 3)) as key_tackles_per_90,
            cast(coalesce("interceptions", 0) as smallint) as interceptions,
            cast(coalesce("interceptions_per_90", 0) as numeric(5, 3)) as interceptions_per_90,
            cast(coalesce("clearances", 0) as smallint) as clearances,
            cast(coalesce("clearances_per_90", 0) as numeric(5, 3)) as clearances_per_90,
            cast(coalesce("blocks", 0) as smallint) as blocks,
            cast(coalesce("blocks_per_90", 0) as numeric(5, 3)) as blocks_per_90,
            cast(coalesce("headers_won", 0) as smallint) as headers_won,
            cast(coalesce("headers_won_ratio", 0) as numeric(5, 4)) as headers_won_ratio,
            cast(coalesce("headers_won_per_90", 0) as numeric(5, 3)) as headers_won_per_90,
            cast(coalesce("headers_attempted", 0) as smallint) as headers_attempted,
            cast(coalesce("headers_loss_per_90", 0) as numeric(5, 3)) as headers_loss_per_90,
            cast(coalesce("key_headers_per_90", 0) as numeric(5, 3)) as key_headers_per_90,
            cast(coalesce("possession_won_per_90", 0) as numeric(6, 3)) as possession_won_per_90,
            cast(coalesce("possession_lost_per_90", 0) as numeric(6, 3)) as possession_lost_per_90,
            cast(coalesce("pressures_completed", 0) as smallint) as pressures_completed,
            cast(coalesce("pressures_completed_per_90", 0) as numeric(5, 3)) as pressures_completed_per_90,
            cast(coalesce("pressures_attempted", 0) as smallint) as pressures_attempted,
            cast(coalesce("pressures_attempted_per_90", 0) as numeric(6, 3)) as pressures_attempted_per_90,
            cast(coalesce("mistakes_leading_to_goal", 0) as smallint) as mistakes_leading_to_goal,
            cast(coalesce("aerial_challenges_attempted_per_90", 0) as numeric(6, 3)) as aerial_challenges_attempted_per_90

        from source
    )

select *
from stg_player_stats_defending
