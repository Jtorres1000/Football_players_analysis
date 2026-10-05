with

    source as (select * from {{ source("football_data", "TRANSFERS_RAW") }}),

    stg_transfers as (
        select
            cast("transfer_id" as int) as transfer_id,
            cast("player_id" as int) as player_id,
            cast("from_club_id" as int) as from_club_id,
            cast("to_club_id" as int) as to_club_id,
            cast("season_id" as int) as season_id,
            cast("transfer_date" as date) as transfer_date,
            cast("transfer_fee_eur" as numeric(12,2)) as transfer_fee_eur,
            cast("transfer_type" as varchar(10)) as transfer_type

        from source
    )

select *
from stg_transfers
