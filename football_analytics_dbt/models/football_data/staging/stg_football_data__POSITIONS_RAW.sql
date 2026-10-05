with

    source as (select * from {{ source("football_data", "POSITIONS_RAW") }}),

    stg_positions as (
        select
            cast("position_id" as int) as position_id,
            cast("role_code" as varchar(5)) as role_code,
            cast("side_code" as char(1)) as side_code

        from source
    )

select *
from stg_positions
