with untiered as (
	select 
	i.*,
	plan_amount as amount,
	line_id as subscription_id
	from {{ref('invoice_items')}} as i
	where proration = 'no'
	and billing_scheme != 'tiered'
), tier_and_untiered as (
	select a.*
	from
		(
			select 
			invoice_id, 
			customer_id,
			subscription_id,
			plan_id,
			plan_interval,
			amount,
			quantity
			from {{ref('invoices_tiered')}} as tiered
			union all
			select 
			invoice_id, 
			customer_id,
			subscription_id,
			plan_id,
			plan_interval,
			amount*quantity as amount,
			quantity
			from untiered as untiered
			where quantity > 0
	) as a
), invoices2 as (
	select 
	i.*,
	case 
	when plan_interval = 'year' then il.amount / (12*100)
	else il.amount / 100 
	end as base_mrr,
	il.quantity,
	il.plan_interval,
	il.plan_id,
	il.subscription_id
	from 
	{{ref('invoices')}} as i left join 
	tier_and_untiered as il on i.invoice_id = il.invoice_id
)

select i.*
from 
invoices2 as i