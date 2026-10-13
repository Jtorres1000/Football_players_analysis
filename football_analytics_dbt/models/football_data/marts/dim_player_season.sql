with

    seasons as (select * from {{ ref('stg_football_data__SEASONS_RAW') }}),

    player_seasons as (select * from {{ ref('stg_football_data__PLAYER_SEASONS_RAW') }}),

    player_positions as (select * from {{ ref('stg_football_data__PLAYER_POSITIONS_RAW') }}),

    positions as (select * from {{ ref('stg_football_data__POSITIONS_RAW') }}),

    aggregated_positions as (
        select
            pp.player_id,
            listagg(
                concat(
                    pos.role_code,
                    coalesce(' (' || nullif(trim(pos.side_code), '') || ')', '')
                ),
                ', '
            ) within group (order by pp.position_rank asc) as all_positions_str

        from player_positions pp
        join positions pos
            on pp.position_id = pos.position_id
        group by pp.player_id
    ),

    dim_player_seasons as (
        select
        {{ dbt_utils.generate_surrogate_key(['ps.player_season_id']) }} as player_season_key,
        s.season_id,
        ps.player_season_id,
        s.season_label,
        ps.age,
        case 
            when ps.age >= 15 and ps.age < 22 then '15-21'
            when ps.age >= 22 and ps.age < 27 then '22-26'
            when ps.age >= 27 and ps.age < 32 then '27-31'
            when ps.age >= 32 and ps.age < 39 then '32-38'
        end as age_group,
        ap.all_positions_str

        from seasons s
        INNER JOIN player_seasons ps
            using(season_id)
        INNER JOIN aggregated_positions ap
            using(player_id)
    )

select *
from dim_player_seasons
