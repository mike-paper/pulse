select 
s.details ->> 'id' as "subscription_id",
s.details ->> 'customer' as "customer_id",
c.email,
s.details ->> 'status' as "status",
(s.details -> 'plan' ->> 'amount')::integer as "plan_amount",
(s.details -> 'plan' ->> 'interval') as "plan_interval",
s.details -> 'items' -> 'data' -> 0 -> 'quantity' as "quantity", 
s.details -> 'items' -> 'data' -> 0 -> 'plan' -> 'tiers' as "tiers", 
s.details -> 'discount' -> 'coupon' -> 'percent_off' as "percent_off", 
s.details -> 'discount' -> 'coupon' -> 'amount_off' as "amount_off", 
s.details -> 'discount' -> 'coupon' -> 'duration' as "discount_duration", 
to_timestamp((s.details ->> 'canceled_at')::int) as "canceled_dt",
to_timestamp((s.details ->> 'start_date')::int) as "start_dt",
to_timestamp((s.details ->> 'created')::int) as "created_on",
(s.details ->> 'created')::int as "created",
(s.details ->> 'canceled_at')::int as "canceled_at"
from 
public.stripe_subscriptions as s left join
{{ref('customers')}} as c on (s.details ->> 'customer') = c.customer_id
where team_id = {{ env_var('PAPER_DBT_TEAM_ID') }} 