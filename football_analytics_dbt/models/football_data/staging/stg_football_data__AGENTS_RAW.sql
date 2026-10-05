with

    source as (select * from {{ source("football_data", "AGENTS_RAW") }}),

    stg_agents as (
        select
            cast("agent_id" as int) as agent_id,
            cast("agent_name" as varchar(150)) as agent_name,
            cast("agency_name" as varchar(150)) as agency_name

        from source
    )

select *
from stg_agents
