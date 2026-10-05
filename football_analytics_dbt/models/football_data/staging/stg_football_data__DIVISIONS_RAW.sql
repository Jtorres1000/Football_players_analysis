with

    source as (select * from {{ source("football_data", "DIVISIONS_RAW") }}),

    stg_divisions as (
        select
            cast("division_id" as int) as division_id,
            cast("division_name" as varchar(150)) as division_name,
            cast("division_strength" as numeric(6,2)) as division_strength

        from source
    )

select *
from stg_divisions
