SET search_path TO portfolio_sales;

-- 1. KPI general
SELECT
    COUNT(DISTINCT o.order_id) AS completed_orders,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS revenue,
    ROUND(
        SUM(
            oi.quantity * (
                oi.unit_price * (1 - oi.discount_pct / 100.0) - p.cost
            )
        ),
        2
    ) AS gross_profit,
    ROUND(
        100 * SUM(
            oi.quantity * (
                oi.unit_price * (1 - oi.discount_pct / 100.0) - p.cost
            )
        ) / NULLIF(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 0),
        2
    ) AS gross_margin_pct
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.status = 'Completed';

-- 2. Ranking de productos por ingresos y utilidad
SELECT
    p.name AS product,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS revenue,
    ROUND(
        SUM(
            oi.quantity * (
                oi.unit_price * (1 - oi.discount_pct / 100.0) - p.cost
            )
        ),
        2
    ) AS gross_profit
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.status = 'Completed'
GROUP BY p.product_id, p.name
ORDER BY gross_profit DESC;

-- 3. Evolución mensual con variación porcentual
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', o.order_date)::date AS month,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'Completed'
    GROUP BY 1
),
with_previous AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS previous_revenue
    FROM monthly
)
SELECT
    month,
    revenue,
    previous_revenue,
    ROUND(100 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0), 2) AS variation_pct
FROM with_previous
ORDER BY month;

-- 4. Comparación por canal
SELECT
    o.channel,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY o.channel
ORDER BY revenue DESC;

-- 5. Clientes con mayor facturación
SELECT
    c.full_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.full_name, c.city
ORDER BY revenue DESC;

-- 6. Ventas por ciudad
SELECT
    c.city,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY c.city
ORDER BY revenue DESC;

-- 7. Productos con margen bruto superior al 30%
SELECT
    p.name,
    ROUND(
        100 * SUM(
            oi.quantity * (
                oi.unit_price * (1 - oi.discount_pct / 100.0) - p.cost
            )
        ) / NULLIF(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 0),
        2
    ) AS gross_margin_pct
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY p.product_id, p.name
HAVING 100 * SUM(
    oi.quantity * (
        oi.unit_price * (1 - oi.discount_pct / 100.0) - p.cost
    )
) / NULLIF(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 0) > 30
ORDER BY gross_margin_pct DESC;
