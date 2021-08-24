with customers as (
	select 
	c.details ->> 'id' as customer_id,
	c.details ->> 'email' as email,
	to_timestamp((c.details ->> 'created')::int) as "created_on"
	from 
	public.stripe_customers as c 
	where c.team_id = {{ env_var('PAPER_DBT_TEAM_ID') }}
)
select * from customers