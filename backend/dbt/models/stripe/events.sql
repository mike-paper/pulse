with events as (
	select 
	c.details ->> 'id' as event_id,
	c.details ->> 'type' as event_type,
	to_timestamp((c.details ->> 'created')::int) as "created_on",
	c.details -> 'data' -> 'object' as event,
	c.details -> 'data' -> 'object' ->> 'customer' as customer_id
	from 
	public.stripe_events as c 
	where c.team_id = {{ env_var('PAPER_DBT_TEAM_ID') }}
)
select 
c.email,
e.* 
from events as e left join 
{{ref('customers')}} as c on e.customer_id = c.customer_id