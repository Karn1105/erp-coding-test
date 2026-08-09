-- Step 1: Create the orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10, 2),
    order_date DATE
);

-- Step 2: Insert sample data for testing
INSERT INTO orders (order_id, customer_id, total_amount, order_date) VALUES
(1, 101, 1500.00, '2025-05-10'),
(2, 102, 2500.50, '2025-06-15'),
(3, 101, 3000.00, '2025-07-20'),
(4, 103, 4500.00, '2025-02-11'),
(5, 104, 1200.00, '2025-08-30'),
(6, 105, 5100.00, '2025-09-05'),
(7, 102, 800.00, '2025-10-12');

-- Step 3: Run your query to find the top 5 customers for 2025
SELECT customer_id, SUM(total_amount) AS total_order_value
FROM orders
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'
GROUP BY customer_id
ORDER BY total_order_value DESC
LIMIT 5;
