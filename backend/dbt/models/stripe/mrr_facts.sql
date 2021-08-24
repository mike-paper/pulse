
with annuals as (
	select 
	generate_series(
		i.created_on, 
		(
			select last_day_of_month --needs to be capped at a year
			from public.d_date as d 
			where d.date_actual = (
					least(
						(i.created_on::timestamp + interval '11 months')::date, 
						s.canceled_dt::date,
						current_timestamp::date
					)
				)
		), 
		'1 month'::interval
	) as monthly,
	i.invoice_id
	from {{ref('invoice_facts')}} as i left join
	{{ref('subscriptions')}} as s on i.subscription_id = s.subscription_id
	where i.plan_interval = 'year'
), annuals2 as (
	select
	i.*,
	a.monthly as mrr_dt
	from
	{{ref('invoice_facts')}} as i inner join 
	annuals as a on i.invoice_id = a.invoice_id
), mrr as (
	select
	mrr.customer_id	,
	mrr.invoice_id	,
	mrr.subscription_id	,
	mrr.mrr_dt,
	mrr.created_on	,
	mrr.total	,
	mrr.amount_due	,
	mrr.amount_off	,
	mrr.percent_off_precise	,
	mrr.coupon_duration	,
	mrr.plan_interval	,
	mrr.plan_id	,
	mrr.base_mrr,
	s.canceled_dt,
	-- TODO: flat amount discounts, I have someone using these now s
	case 
	when coupon_duration = 'forever' then 
		(base_mrr * (1 - percent_off_precise / 100))
	else base_mrr
	end as discounted_mrr,
	case 
	when percent_off_precise is not null then 
		(base_mrr * (1 - percent_off_precise / 100))
	else base_mrr
	end as fully_discounted_mrr
	from
	(
		select *, i.created_on as mrr_dt
		from {{ref('invoice_facts')}} as i
		where plan_interval != 'year'
		union all
		select *
		from annuals2
	) as mrr left join
	{{ref('subscriptions')}} as s on mrr.subscription_id = s.subscription_id
), max_mrr as ( --get the most recent mrr record not in the current month
	select 
	customer_id,
	max(mrr_dt) as mrr_dt
	from mrr as mrr
	where canceled_dt is null
	group by customer_id
), current_mrr as (
	select
	mrr.customer_id	,
	invoice_id	,
	subscription_id	,
	current_timestamp as mrr_dt,
	current_timestamp as created_on,
	total	,
	amount_due	,
	amount_off	,
	percent_off_precise	,
	coupon_duration	,
	plan_interval	,
	plan_id	,
	base_mrr,
	canceled_dt,
	discounted_mrr,
	fully_discounted_mrr
	from 
	mrr as mrr inner join
	max_mrr as max_mrr on mrr.customer_id = max_mrr.customer_id and mrr.mrr_dt = max_mrr.mrr_dt
	where date_trunc('month', mrr.mrr_dt) = date_trunc('month', current_date - interval '1 month')
), mrr2 as (
	select 
	* 
	from (
		select *, 'sent' as invoice_status from mrr
		union all
		select *, 'pending' as invoice_status from current_mrr
	) as mrr
), mrr3 as (
	select 
	ce.email,
	c.created_on as customer_created_on,
	mrr.*,
	case 
	when date_trunc('month', mrr.canceled_dt) = date_trunc('month', mrr.mrr_dt) then 0
	else discounted_mrr end as mrr
	from mrr2 as mrr left join
	{{ref('customers')}} as c on mrr.customer_id = c.customer_id left join
	{{ref('customer_emails')}} as ce on mrr.customer_id = ce.customer_id 
), mrr4 as (
	select mrr.*,
	date_trunc('month', mrr.mrr_dt) as mrr_month_dt,
	prev_mrr.mrr as prev_mrr,
	case 
	when prev_mrr.mrr is null then 'new'
	when mrr.mrr > prev_mrr.mrr then 'expansion'
	when mrr.mrr < prev_mrr.mrr then 'churn'
	when date_trunc('month', mrr.canceled_dt) = date_trunc('month', mrr.mrr_dt) then 'churn'
	else 'same' end as mrr_status,
	case 
	when prev_mrr.mrr is null then 0
	when date_trunc('month', mrr.canceled_dt) = date_trunc('month', mrr.mrr_dt) then mrr.mrr
	when mrr.mrr < prev_mrr.mrr then prev_mrr.mrr - mrr.mrr
	else 0 end as churned_mrr,
	case 
	when prev_mrr.mrr is null then 0
	when mrr.mrr > prev_mrr.mrr then mrr.mrr - prev_mrr.mrr
	else 0 end as expansion_mrr,
	case 
	when prev_mrr.mrr is null then mrr.mrr
	else 0 end as new_mrr,
	prev_mrr.mrr_dt as prev_mrr_dt
	from mrr3 as mrr left join
	mrr3 as prev_mrr on mrr.customer_id = prev_mrr.customer_id and
							date_trunc('month', mrr.mrr_dt) = date_trunc('month', prev_mrr.mrr_dt + interval '1 month')
)

select 
mrr.*,
date_trunc('month', mrr.customer_created_on)::date::text as vintage,
(extract(year from age(mrr.mrr_month_dt, date_trunc('month', mrr.customer_created_on))) * 12 +
	extract(month from age(mrr.mrr_month_dt, date_trunc('month', mrr.customer_created_on)))) as vintage_age,
case 
when mrr.mrr_month_dt = max_month.mrr_month_dt then 1
else 0 end as current_month,
cume_dist() OVER (PARTITION BY mrr.mrr_month_dt ORDER BY mrr.mrr) as mrr_percentile,
ntile(10) OVER (PARTITION BY mrr.mrr_month_dt ORDER BY mrr.mrr) as mrr_rank
from mrr4 as mrr left join
(select max(mrr4.mrr_month_dt) as mrr_month_dt from mrr4) as max_month on mrr.mrr_month_dt = max_month.mrr_month_dt