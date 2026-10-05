with

    source as (select * from {{ source("football_data", "NATIONS_RAW") }}),
    
    clean_raw_nations as (
        select
            "nation_id",
            "nation_name",
            -- Correción para usar el mismo código en las tablas del seed csv
            CASE 
                WHEN "nation_code" = 'GER' THEN 'DEU' 
                WHEN "nation_code" = 'NCA' THEN 'NIC' 
                WHEN "nation_code" = 'GRN' THEN 'GRD' 
                ELSE "nation_code"
            END AS "nation_code"
        from source
    ),

    country_codes_name as (select * from {{ ref('nations_code') }}),

    stg_nations as (
        select
            cast("nation_id" as int) as nation_id,
            cast("nation_code" as varchar(10)) as nation_code,
            cast(cn.name as varchar(100)) as nation_name

        from clean_raw_nations crn
        LEFT JOIN country_codes_name cn ON
        crn."nation_code" = cn.alpha_3
    )

select *
from stg_nations
