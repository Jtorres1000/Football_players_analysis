with

    ps as (select * from {{ ref('stg_football_data__PLAYER_SEASONS_RAW') }}),

    seasons as (select * from {{ ref('stg_football_data__SEASONS_RAW') }}),

    contracts as (select * from {{ ref('stg_football_data__CONTRACTS_RAW') }}),
    season_dates as (
        select
            season_id,
            season_order,
            date_from_parts(try_to_number(left(season_label, 4)), 7, 1) as season_start_date,
            date_from_parts(try_to_number(left(season_label, 4)) + 1, 6, 30) as season_end_date
        from seasons
    ),
    -- Se usa la tabla de clubs y contracts para decidir cuál es el contrato mas reciente del jugador y utilizarlo para calcular su salario anual.
    season_contracts as (
        select
            ps.player_season_id,
            c.weekly_wage_eur,
            (c.weekly_wage_eur * 52) as annual_wage_eur,
            row_number() over (
                partition by ps.player_season_id
                order by
                    case
                        when c.start_date <= sd.season_end_date
                         and coalesce(c.end_date, sd.season_end_date) >= sd.season_start_date
                        then 0
                        else 1
                    end asc,
                    case when c.club_id = ps.club_id then 0 else 1 end asc,
                    c.start_date desc
            ) as rn
        from ps
        inner join season_dates sd
            on ps.season_id = sd.season_id
        inner join contracts c
            on ps.player_id = c.player_id
    ),

    fact_joined as (
        select
            ps.player_season_id,
            ps.player_id,
            ps.season_id,
            ps.age,
            ps.ability_score,
            ps.ability_score - lag(ps.ability_score) over (
                partition by ps.player_id
                order by sd.season_order asc
            ) as ability_score_delta,
            sc.weekly_wage_eur,
            sc.annual_wage_eur
        from ps
        inner join season_dates sd
            on ps.season_id = sd.season_id
        inner join season_contracts sc
            on ps.player_season_id = sc.player_season_id
            and sc.rn = 1
        where ps.age between 15 and 38
    ),

    fact_player_season as (
        select
            {{ dbt_utils.generate_surrogate_key(['player_season_id']) }} as player_season_key,
            {{ dbt_utils.generate_surrogate_key(['player_id']) }} as player_key,
            {{ dbt_utils.generate_surrogate_key(['season_id']) }} as season_key,
            {{ dbt_utils.generate_surrogate_key(['age']) }} as age_key,
            ability_score,
            ability_score_delta,
            weekly_wage_eur,
            annual_wage_eur
        from fact_joined
    )

select *
from fact_player_season
