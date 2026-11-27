-- Подтверждённые владельцем источника суммы строк есть в source-check.csv.
CREATE VIEW checked_items AS
SELECT order_id, line_no,
       CASE WHEN amount IS NULL AND order_id = 101 AND line_no = 1 THEN 600
            WHEN amount IS NULL AND order_id = 102 AND line_no = 1 THEN 400
            ELSE amount END AS amount
FROM items;

CREATE VIEW order_revenue AS
WITH sales AS (
    SELECT order_id, SUM(amount) AS gross FROM checked_items GROUP BY order_id
), returns AS (
    SELECT order_id, SUM(amount) AS returned FROM refunds GROUP BY order_id
)
SELECT o.order_id, o.ordered_on, o.channel, s.gross - COALESCE(r.returned, 0) AS revenue
FROM orders AS o
JOIN sales AS s ON s.order_id = o.order_id
LEFT JOIN returns AS r ON r.order_id = o.order_id;
