with

    source as (select * from {{ source("football_data", "PLAYER_STATS_GOALKEEPING_RAW") }}),

    stg_player_stats_goalkeeping as (
        select
            cast("player_season_id" as int) as player_season_id,
            cast(coalesce("saves_tipped", 0) as smallint) as saves_tipped,
            cast(coalesce("saves_parried", 0) as smallint) as saves_parried,
            cast(coalesce("saves_held", 0) as smallint) as saves_held,
            cast(coalesce("saves_per_90", 0) as numeric(5, 3)) as saves_per_90,
            cast(coalesce("save_ratio", 0) as numeric(5, 4)) as save_ratio,
            cast(coalesce("clean_sheets", 0) as smallint) as clean_sheets,
            cast(coalesce("clean_sheets_per_90", 0) as numeric(5, 3)) as clean_sheets_per_90,
            cast(coalesce("conceded_per_90", 0) as numeric(5, 3)) as conceded_per_90,
            cast(coalesce("team_conceded", 0) as smallint) as team_conceded,
            cast(coalesce("team_conceded_per_90", 0) as numeric(5, 3)) as team_conceded_per_90,
            cast(coalesce("team_goals", 0) as smallint) as team_goals,
            cast(coalesce("team_goals_per_90", 0) as numeric(5, 3)) as team_goals_per_90,
            cast(coalesce("goals_conceded", 0) as smallint) as goals_conceded,
            cast(coalesce("penalties_saved", 0) as smallint) as penalties_saved,
            cast(coalesce("penalties_saved_ratio", 0) as numeric(5, 4)) as penalties_saved_ratio,
            cast(coalesce("expected_saves_ratio", 0) as numeric(5, 4)) as expected_saves_ratio,
            cast(coalesce("expected_goals_prevented", 0) as numeric(6, 2)) as expected_goals_prevented,
            cast(coalesce("expected_goals_prevented_per_90", 0) as numeric(5, 3)) as expected_goals_prevented_per_90

        from source
    )

select *
from stg_player_stats_goalkeeping
