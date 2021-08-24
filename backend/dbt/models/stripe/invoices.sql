--TODO: support multiple invoices for a single customer
with invoices as (
	select 
	details ->> 'customer' as customer_id,
	details ->> 'id' as invoice_id,
	to_timestamp((details ->> 'created')::int) as created_on,
	date_trunc('month', to_timestamp((details ->> 'created')::int)) as created_month,
	details ->> 'total' as total,
	details ->> 'amount_due' as amount_due,
	(details -> 'lines' -> 'data') as lines_data,
	(((details ->> 'discount')::jsonb) -> 'coupon' ->> 'amount_off')::float as amount_off,
	(((details ->> 'discount')::jsonb) -> 'coupon' ->> 'percent_off_precise')::float as percent_off_precise,
	(((details ->> 'discount')::jsonb) -> 'coupon' ->> 'duration')::text as coupon_duration
	from 
	public.stripe_invoices as si 
	where 1=1 
	and team_id = {{ env_var('PAPER_DBT_TEAM_ID') }} 
), max_in_month as ( 
	select customer_id, created_month, max(created_on) as created_on
	from
	invoices as i
	group by customer_id, created_month
), invoices2 as (
	select 
	i.*
	from invoices as i inner join
	max_in_month as m on i.customer_id = m.customer_id and i.created_on = m.created_on
)
select * from invoices2