with

    source as (select * from {{ source("football_data", "CONTRACTS_RAW") }}),

    stg_contracts as (
        select
            cast("contract_id" as int) as contract_id,
            cast("player_id" as int) as player_id,
            cast("club_id" as int) as club_id,
            cast("start_date" as date) as start_date,
            cast("end_date" as date) as end_date,
            cast("weekly_wage_eur" as numeric(12,2)) as weekly_wage_eur,
            cast("contract_value_eur" as numeric(14,2)) as contract_value_eur

        from source
    )

select *
from stg_contracts
