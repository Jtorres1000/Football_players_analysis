with

    player as (select * from {{ ref('stg_football_data__PLAYERS_RAW') }}),

    player_positions as (select * from {{ ref('stg_football_data__PLAYER_POSITIONS_RAW') }}),

    positions as (select * from {{ ref('stg_football_data__POSITIONS_RAW') }}),

    primary_pos as (
        select
            pp.player_id,
            pos.role_code as primary_role_code,
            pos.side_code as primary_side_code
        from player_positions pp
        inner join positions pos
            on pp.position_id = pos.position_id
        where pp.position_rank = 1
        qualify row_number() over (partition by pp.player_id order by pp.position_id asc) = 1
    ),

    dim_player as (
        select
            {{ dbt_utils.generate_surrogate_key(['p.player_id']) }} as player_key,
            p.player_id,
            p.name,
            p.primary_category,
            pp.primary_role_code,
            pp.primary_side_code
        from player p
        left join primary_pos pp
            on p.player_id = pp.player_id
    )

select *
from dim_player
