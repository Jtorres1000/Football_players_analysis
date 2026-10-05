with

    source as (select * from {{ source("football_data", "CLUBS_RAW") }}),

    stg_clubs as (
        select
            cast("club_id" as int) as club_id,
            cast("club_name" as varchar(150)) as club_name,
            cast("division_id" as int) as division_id

        from source
    )

select *
from stg_clubs
