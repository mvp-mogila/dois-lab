SELECT * FROM `Order_list` JOIN `Order` ON `Order_list`.`order_id`=`Order`.`id`
WHERE `product_id`='$product' AND YEAR(`Order`.`date`)='$year' AND MONTH(`Order`.`date`)='$month';