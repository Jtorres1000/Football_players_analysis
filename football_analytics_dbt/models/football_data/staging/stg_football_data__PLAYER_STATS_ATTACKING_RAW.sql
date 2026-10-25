with

    source as (select * from {{ source("football_data", "PLAYER_STATS_ATTACKING_RAW") }}),

    stg_player_stats_attacking as (
        select
            cast("player_season_id" as int) as player_season_id,
            cast(coalesce("goals", 0) as smallint) as goals,
            cast(coalesce("goals_per_90", 0) as numeric(5, 3)) as goals_per_90,
            cast(coalesce("xg", 0) as numeric(6, 2)) as xg,
            cast(coalesce("xg_per_90", 0) as numeric(5, 3)) as xg_per_90,
            cast(coalesce("non_penalty_xg", 0) as numeric(6, 2)) as non_penalty_xg,
            cast(coalesce("non_penalty_xg_per_90", 0) as numeric(5, 3)) as non_penalty_xg_per_90,
            cast(coalesce("xg_overperformance", 0) as numeric(6, 2)) as xg_overperformance,
            cast(coalesce("shots", 0) as smallint) as shots,
            cast(coalesce("shots_per_90", 0) as numeric(5, 3)) as shots_per_90,
            cast(coalesce("shots_on_target", 0) as smallint) as shots_on_target,
            cast(coalesce("shots_on_target_ratio", 0) as numeric(5, 4)) as shots_on_target_ratio,
            cast(coalesce("shots_on_target_per_90", 0) as numeric(5, 3)) as shots_on_target_per_90,
            cast(coalesce("shots_outside_box_per_90", 0) as numeric(5, 3)) as shots_outside_box_per_90,
            cast(coalesce("shots_blocked", 0) as smallint) as shots_blocked,
            cast(coalesce("shots_blocked_per_90", 0) as numeric(5, 3)) as shots_blocked_per_90,
            cast(coalesce("xg_per_shot", 0) as numeric(5, 4)) as xg_per_shot,
            cast(coalesce("conversion_rate", 0) as numeric(5, 4)) as conversion_rate,
            cast(coalesce("goals_outside_box", 0) as smallint) as goals_outside_box,
            cast(coalesce("free_kick_shots", 0) as smallint) as free_kick_shots,
            cast(coalesce("penalties_scored", 0) as smallint) as penalties_scored,
            cast(coalesce("penalties_scored_ratio", 0) as numeric(5, 4)) as penalties_scored_ratio,
            cast(coalesce("penalties_taken", 0) as smallint) as penalties_taken,
            cast(coalesce("penalties_faced", 0) as smallint) as penalties_faced,
            cast(coalesce("assists", 0) as smallint) as assists,
            cast(coalesce("assists_per_90", 0) as numeric(5, 3)) as assists_per_90,
            cast(coalesce("xa", 0) as numeric(6, 2)) as xa,
            cast(coalesce("xa_per_90", 0) as numeric(5, 3)) as xa_per_90,
            cast(coalesce("chances_created", 0) as smallint) as chances_created,
            cast(coalesce("chances_created_per_90", 0) as numeric(5, 3)) as chances_created_per_90,
            cast(coalesce("dribbles_made", 0) as smallint) as dribbles_made,
            cast(coalesce("dribbles_made_per_90", 0) as numeric(5, 3)) as dribbles_made_per_90,
            cast(coalesce("offsides", 0) as smallint) as offsides,
            cast(coalesce("average_min_per_goal", 0) as numeric(8, 2)) as average_min_per_goal

        from source
    )

select *
from stg_player_stats_attacking
