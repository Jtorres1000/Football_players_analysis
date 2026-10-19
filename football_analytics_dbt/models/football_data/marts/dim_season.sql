with

    seasons as (select * from {{ ref('stg_football_data__SEASONS_RAW') }}),

    dim_season as (
        select
            {{ dbt_utils.generate_surrogate_key(['s.season_id']) }} as season_key,
            s.season_id,
            s.season_label
        from seasons s
    )

select *
from dim_season
