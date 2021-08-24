
with sum_invoice_items as ( 
	select 
	customer_id,
	invoice_id, 
	line_id as subscription_id,
	plan_id,
	plan_interval,
	sum(i.quantity) as quantity
	from {{ref('invoice_items')}} as i
	where proration = 'no'
	and billing_scheme = 'tiered'
	group by 
	customer_id,
	invoice_id, 
	line_id,
	plan_id,
	plan_interval
), invoice_items as ( 
	select 
	customer_id,
	invoice_id, 
	subscription_id,
	plan_id,
	plan_interval,
	generate_series(1, i.quantity) as quantity
	from sum_invoice_items as i
), invoice_items2 as (
	select 
	customer_id,
	invoice_id, 
	subscription_id,
	i.plan_id,
	i.plan_interval,
	sum(pt.amount) as amount,
	sum(quantity) as quantity
	from 
	invoice_items as i left join
	{{ref('plan_tiers')}} as pt on i.plan_id = pt.plan_id and 
		i.quantity >= pt.lower_tier and i.quantity <= pt.upper_tier
	group by 
	customer_id,
	invoice_id, 
	subscription_id,
	i.plan_id,
	i.plan_interval
)

select i.*
from 
invoice_items2 as i 