
with emails as (
	select 
	details ->> 'customer_email' as email, 
	details ->> 'customer' as customer_id,
	details ->> 'created' as created
	from public.stripe_invoices 
	where details ->> 'customer_email' is not null
	and team_id = {{ env_var('PAPER_DBT_TEAM_ID') }} 
), max_email as (
	select
	customer_id,
	max(created) as created
	from
	emails
	group by 
	customer_id
)

select 
e.customer_id, 
e.email,
to_timestamp((e.created)::int) as "created_on"
from emails as e inner join
max_email as me on e.customer_id = me.customer_id and e.created = me.created