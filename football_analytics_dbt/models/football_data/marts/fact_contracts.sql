with

    contracts as (select * from {{ ref('stg_football_data__CONTRACTS_RAW') }}),
    
    fact_contracts as (
        select
        {{ dbt_utils.generate_surrogate_key(['c.contract_id']) }} as contract_key,
        {{ dbt_utils.generate_surrogate_key(['c.player_id']) }} as player_key,
        c.contract_id,
        c.player_id,
        c.weekly_wage_eur,
        (c.weekly_wage_eur * 52) as annual_wage_eur
        from contracts c

    )

select *
from fact_contracts
