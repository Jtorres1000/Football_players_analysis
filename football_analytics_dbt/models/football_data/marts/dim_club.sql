with

    clubs as (select * from {{ ref('stg_football_data__CLUBS_RAW') }}),

    divisions as (select * from {{ ref('stg_football_data__DIVISIONS_RAW') }}),

    dim_club as (
        select
            {{ dbt_utils.generate_surrogate_key(['c.club_id']) }} as club_key,
            c.club_id,
            c.club_name,
            c.division_id,
            d.division_name
        from clubs c
        left join divisions d
            on c.division_id = d.division_id
    )

select *
from dim_club
