SELECT product_name, product_category, product_price, product_weight, product_weight_measure
FROM Product
WHERE product_price>='$lower' AND product_price<='$upper';