--sql queries
--1 name the line item with id 356
select line_item_name from line_item where line_item_id=356;

--2 the ids and names of all line items in the booking named 'Mc Donalds Jan 2018'
select line_item_id, line_item_name from line_item lt
   left join  placement pla on pla.placement_id=lt.placement_id
   left join booking bo on pla.booking_id=bo.booking_id
    and bo.booking_name = 'McDonalds Jan 2018';

--3 the advertiser categories of all the items in the booking named 'Virgin' in their names. Each category should ideally only be listed once, even if it applies to several line items
select ad.advertiser_category from line_item lt
   left join placement pla on pla.placement_id=lt.placement_id
   left join booking bo on pla.booking_id=bo.booking_id
   left join advertiser ad on bo.advertiser_id=ad.advertiser_id
   and ad.advertiser_category like '%Virgin%'
   group by ad.advertiser_category;