with

    distinct_ages as (
        select distinct
            age
        from {{ ref('stg_football_data__PLAYER_SEASONS_RAW') }}
        where age between 15 and 38
    ),

    dim_age_bracket as (
        select
            {{ dbt_utils.generate_surrogate_key(['age']) }} as age_key,
            age,
            case
                when age >= 15 and age < 22 then '15-21'
                when age >= 22 and age < 27 then '22-26'
                when age >= 27 and age < 32 then '27-31'
                when age >= 32 and age < 39 then '32-38'
            end as age_group
        from distinct_ages
    )

select *
from dim_age_bracket
