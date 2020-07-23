
-- Bigquery Clean Data Sql
WITH
  base_today AS(
  SELECT
    *,
    DATE(_PARTITIONTIME) AS date_time
  FROM
    crawler_product_detail.DATA
  WHERE
    DATE(_PARTITIONTIME) = CURRENT_DATE() ),
  base_yesterday AS(
  SELECT
    itemid,
    name,
    type_name,
    type_sold,
    DATE(_PARTITIONTIME) AS date_time
  FROM
    crawler_product_detail.DATA
  WHERE
    DATE(_PARTITIONTIME) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) )
SELECT
  t.*,
  y.type_sold AS yesterday_sold,
  t.type_sold - y.type_sold AS sold,
  t.type_price*(t.type_sold - y.type_sold) AS revenue
FROM
  base_today AS t
LEFT JOIN
  base_yesterday AS y
ON
  t.itemid = y.itemid
  AND t.name = y.name
  AND t.type_name = y.type_name
ORDER BY
  sold DESC

