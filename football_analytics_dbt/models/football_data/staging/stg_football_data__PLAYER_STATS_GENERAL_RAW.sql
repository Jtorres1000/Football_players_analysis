with

    source as (select * from {{ source("football_data", "PLAYER_STATS_GENERAL_RAW") }}),

    stg_player_stats_general as (
        select
            cast("player_season_id" as int) as player_season_id,
            cast(coalesce("points_per_game", 0) as numeric(4, 3)) as points_per_game,
            cast(coalesce("average_rating", 0) as numeric(3, 2)) as average_rating,
            cast(coalesce("games_won", 0) as smallint) as games_won,
            cast(coalesce("games_lost", 0) as smallint) as games_lost,
            cast(coalesce("games_drawn", 0) as smallint) as games_drawn,
            cast(coalesce("game_win_ratio", 0) as numeric(5, 4)) as game_win_ratio,
            cast(coalesce("player_of_the_match", 0) as smallint) as player_of_the_match,
            cast(coalesce("mins_per_gm", 0) as numeric(6, 2)) as mins_per_gm,
            cast(coalesce("yellows", 0) as smallint) as yellows,
            cast(coalesce("red", 0) as smallint) as red,
            cast(coalesce("fouls_made", 0) as smallint) as fouls_made,
            cast(coalesce("fouls_against", 0) as smallint) as fouls_against,
            cast(coalesce("distance_covered", 0) as numeric(7, 2)) as distance_covered,
            cast(coalesce("distance_covered_per_90", 0) as numeric(5, 2)) as distance_covered_per_90,
            cast(coalesce("high_intensity_sprints_per_90", 0) as numeric(6, 3)) as high_intensity_sprints_per_90

        from source
    )

select *
from stg_player_stats_general
