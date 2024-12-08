USE Supermarket;

CREATE DEFINER=`admin`@`localhost` PROCEDURE `create_report`(in prod_id INT, in rep_year INT, in rep_month INT)

BEGIN
DECLARE done INT default 0;
DECLARE total_cost INT default 0;

DECLARE C1 CURSOR FOR
SELECT SUM(`quantity` * `product_price`) FROM `Order_list` JOIN `Order` ON `Order_list`.`order_id`=`Order`.`id` JOIN `Product` USING(`product_id`)
WHERE `product_id`=prod_id AND YEAR(`Order`.`date`)=rep_year AND MONTH(`Order`.`date`)=rep_month;

DECLARE EXIT HANDLER FOR NOT FOUND SET done = 1;
OPEN C1;
WHILE done = 0 DO
FETCH C1 INTO total_cost;
INSERT INTO `Report`(`year`, `month`, `product_id`, `total_cost`) VALUES(rep_year, rep_month, prod_id, total_cost);
END WHILE;
CLOSE C1;

END

DROP PROCEDURE create_report ;

SELECT SUM(`quantity` * `product_price`) FROM `Order_list` JOIN `Order` ON `Order_list`.`order_id`=`Order`.`id` JOIN `Product` USING(`product_id`)
WHERE `product_id`=1 AND YEAR(`Order`.`date`)=2020 AND MONTH(`Order`.`date`)=1;
