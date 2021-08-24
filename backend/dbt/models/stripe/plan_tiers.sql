with plans as (
	select 
	plan_id,
	jsonb_array_elements(tiers) as tiers
	from {{ref('plans')}} as p
	where p.tiers != 'null'
), plans2 as (
	select 
	(tiers ->> 'up_to')::int as up_to,
	(tiers ->> 'flat_amount')::float as flat_amount,
	(tiers ->> 'amount')::float as amount,
	* 
	from plans 
), plans3 as (
	select 
	plan_id,
	coalesce(flat_amount, amount) as amount,
	coalesce(up_to, 999999999999) as up_to,
	row_number() OVER (order by plan_id desc, up_to) as rnum
	from plans2
	order by plan_id desc, up_to asc
), plans4 as (
	select 
	p.plan_id,
	p.amount,
	-- p.up_to as lower_tier,
	case when p.up_to = 999999999999 then p3.up_to + 1 else p.up_to end as lower_tier,
	case 
	when p.up_to = 999999999999 then p.up_to
	when p2.up_to = 999999999999 then p.up_to else p2.up_to - 1 end as upper_tier
	-- p.up_to,
	-- p2.up_to as p2_up_to,
	-- p3.up_to as past
	from plans3 as p left join 
	plans3 as p2 on p.plan_id = p2.plan_id and p.rnum = p2.rnum - 1 left join
	plans3 as p3 on p.plan_id = p3.plan_id and p.rnum = p3.rnum + 1
)

select * from plans4