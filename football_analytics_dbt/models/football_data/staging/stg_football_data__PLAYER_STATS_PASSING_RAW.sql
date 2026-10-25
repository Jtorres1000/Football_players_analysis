with

    source as (select * from {{ source("football_data", "PLAYER_STATS_PASSING_RAW") }}),

    stg_player_stats_passing as (
        select
            cast("player_season_id" as int) as player_season_id,
            cast(coalesce("passes_completed", 0) as smallint) as passes_completed,
            cast(coalesce("passes_completed_per_90", 0) as numeric(6, 3)) as passes_completed_per_90,
            cast(coalesce("passes_attempted", 0) as smallint) as passes_attempted,
            cast(coalesce("passes_attempted_per_90", 0) as numeric(6, 3)) as passes_attempted_per_90,
            cast(coalesce("pass_completion_ratio", 0) as numeric(5, 4)) as pass_completion_ratio,
            cast(coalesce("progressive_passes", 0) as smallint) as progressive_passes,
            cast(coalesce("progressive_passes_per_90", 0) as numeric(5, 3)) as progressive_passes_per_90,
            cast(coalesce("key_passes", 0) as smallint) as key_passes,
            cast(coalesce("key_passes_per_90", 0) as numeric(5, 3)) as key_passes_per_90,
            cast(coalesce("open_play_key_passes", 0) as smallint) as open_play_key_passes,
            cast(coalesce("open_play_key_passes_per_90", 0) as numeric(5, 3)) as open_play_key_passes_per_90,
            cast(coalesce("crosses_completed", 0) as smallint) as crosses_completed,
            cast(coalesce("crosses_completed_per_90", 0) as numeric(5, 3)) as crosses_completed_per_90,
            cast(coalesce("crosses_attempted", 0) as smallint) as crosses_attempted,
            cast(coalesce("crosses_attempted_per_90", 0) as numeric(6, 3)) as crosses_attempted_per_90,
            cast(coalesce("crosses_completion_ratio", 0) as numeric(5, 4)) as crosses_completion_ratio,
            cast(coalesce("open_play_crosses_completed", 0) as smallint) as open_play_crosses_completed,
            cast(coalesce("open_play_crosses_completed_per_90", 0) as numeric(5, 3)) as open_play_crosses_completed_per_90,
            cast(coalesce("open_play_crosses_attempted", 0) as smallint) as open_play_crosses_attempted,
            cast(coalesce("open_play_crosses_attempted_per_90", 0) as numeric(5, 3)) as open_play_crosses_attempted_per_90,
            cast(coalesce("open_play_crosses_ratio", 0) as numeric(5, 4)) as open_play_crosses_ratio

        from source
    )

select *
from stg_player_stats_passing
