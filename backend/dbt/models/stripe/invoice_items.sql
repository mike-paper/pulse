with invoice_lines as (
	select *,
	jsonb_array_elements(lines_data) as lines
	from {{ref('invoices')}} as i
), invoice_lines2 as (
	select 
	il.customer_id,
	il.invoice_id,
	il.created_on,
	lines ->> 'id' as line_id, -- this is the subscription_id if it is a subscription item
	lines -> 'plan' ->> 'billing_scheme' as billing_scheme,
	lines -> 'plan' ->> 'id' as plan_id,
	(lines -> 'plan' ->> 'amount')::integer as plan_amount,
	lines -> 'plan' ->> 'interval' as plan_interval,
	lines ->> 'amount' as invoice_amount,
	(lines ->> 'quantity')::int as quantity,
	(lines ->> 'proration')::bool as proration,
	lines -> 'plan' ->> 'tiers' as plan_tiers
	from invoice_lines as il
)
select i.*
from 
invoice_lines2 as i
-- order by i.created_on desc