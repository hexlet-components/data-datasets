SELECT
    substr(ordered_on, 1, 7) AS month,
    sum(revenue) AS total
FROM order_revenue
WHERE ordered_on BETWEEN '2025-10-01' AND '2025-10-24'
   OR ordered_on BETWEEN '2025-11-01' AND '2025-11-24'
GROUP BY substr(ordered_on, 1, 7)
ORDER BY month;

SELECT
    channel,
    SUM(CASE WHEN ordered_on < '2025-11-01' THEN revenue ELSE 0 END) AS october,
    SUM(CASE WHEN ordered_on >= '2025-11-01' THEN revenue ELSE 0 END) AS november
FROM order_revenue
WHERE
    ordered_on BETWEEN '2025-10-01' AND '2025-10-24'
    OR ordered_on BETWEEN '2025-11-01' AND '2025-11-24'
GROUP BY channel;
