-- Após a inserção dos dados no banco, realizar os comandos abaixo para correção dos sequences
select setval('branch_id_seq', (select max(a.id) from branch a), TRUE);
select setval('city_id_seq', (select max(a.id) from city a), TRUE);
select setval('customer_id_seq', (select max(a.id) from customer a), TRUE);
select setval('department_id_seq', (select max(a.id) from department a), TRUE);
select setval('district_id_seq', (select max(a.id) from district a), TRUE);

select setval('employee_id_seq', (select max(a.id) from employee a), TRUE);
select setval('marital_status_id_seq', (select max(a.id) from marital_status a), TRUE);
select setval('product_id_seq', (select max(a.id) from product a), TRUE);
select setval('product_group_id_seq', (select max(a.id) from product_group a), TRUE);


select setval('zone_id_seq', (select max(a.id) from zone a), TRUE);
select setval('sale_id_seq', (select max(a.id) from sale a), TRUE);
select setval('sale_item_id_seq', (select max(a.id) from sale_item a), TRUE);
select setval('state_id_seq', (select max(a.id) from state a), TRUE);

update sale_item si set product_price = (
    select sale_price from product where product.id = si.id_product
    ) where si.product_price = 0;