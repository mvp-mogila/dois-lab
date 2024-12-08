SELECT * FROM Report JOIN Product USING(product_id)
WHERE product_id='$product' AND year='$year' AND month='$month';