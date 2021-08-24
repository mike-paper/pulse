with plans as (
	select 
	details ->> 'id' as plan_id,
	details ->> 'name' as "name",
	to_timestamp((p.details ->> 'created')::int) as "created_on",
	details ->> 'currency' as "currency",
	details ->> 'amount' as "amount",
	details ->> 'product' as "product",
	details ->> 'active' as "active",
	details ->> 'billing_scheme' as "billing_scheme",
	details ->> 'trial_period_days' as "trial_period_days",
	details -> 'tiers' as "tiers",
	details ->> 'interval' as "interval"
	from public.stripe_plans as p
	where team_id = {{ env_var('PAPER_DBT_TEAM_ID') }} 
)

select * from plans