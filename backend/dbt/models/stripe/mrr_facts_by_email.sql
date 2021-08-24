with mrr as (
	select *
	from {{ref('mrr_facts')}}
)
select * from mrr