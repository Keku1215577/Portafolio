SET search_path TO portfolio_sales;

INSERT INTO categories (name) VALUES
('Computers'),
('Peripherals'),
('Accessories');

INSERT INTO customers (full_name, city, email) VALUES
('Ana Martinez', 'Santo Domingo', 'ana@example.com'),
('Carlos Rodriguez', 'Santiago', 'carlos@example.com'),
('Maria Torres', 'La Romana', 'maria@example.com'),
('Jose Ramirez', 'Santo Domingo', 'jose@example.com'),
('Laura Gomez', 'Santiago', 'laura@example.com'),
('Daniel Perez', 'La Romana', 'daniel@example.com');

INSERT INTO products (name, category_id, price, cost) VALUES
('Laptop 14', 1, 95000.00, 73500.00),
('Desktop Pro', 1, 78000.00, 60000.00),
('Monitor 24', 2, 18500.00, 11200.00),
('Mouse USB', 2, 1250.00, 585.00),
('Keyboard Mec', 2, 3250.00, 1900.00),
('Webcam HD', 3, 4600.00, 2750.00);

INSERT INTO orders (order_date, customer_id, channel, status) VALUES
('2026-01-08', 1, 'Online', 'Completed'),
('2026-01-18', 2, 'Store', 'Completed'),
('2026-02-05', 3, 'Online', 'Completed'),
('2026-02-21', 4, 'Store', 'Completed'),
('2026-03-03', 5, 'Online', 'Completed'),
('2026-03-19', 6, 'Store', 'Completed'),
('2026-04-10', 1, 'Online', 'Completed'),
('2026-04-24', 2, 'Store', 'Completed'),
('2026-05-07', 3, 'Online', 'Completed'),
('2026-05-22', 4, 'Store', 'Completed'),
('2026-06-12', 5, 'Online', 'Completed'),
('2026-06-28', 6, 'Store', 'Completed'),
('2026-07-09', 1, 'Online', 'Completed'),
('2026-07-23', 2, 'Store', 'Completed'),
('2026-08-14', 3, 'Online', 'Completed');

INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount_pct) VALUES
(1, 1, 1, 95000.00, 5),
(1, 4, 2, 1250.00, 0),
(2, 2, 1, 78000.00, 0),
(2, 5, 1, 3250.00, 0),
(3, 3, 2, 18500.00, 5),
(4, 1, 1, 95000.00, 0),
(4, 6, 2, 4600.00, 0),
(5, 4, 8, 1250.00, 0),
(5, 5, 4, 3250.00, 10),
(6, 2, 1, 78000.00, 5),
(6, 3, 2, 18500.00, 0),
(7, 1, 1, 95000.00, 0),
(8, 6, 3, 4600.00, 0),
(8, 4, 5, 1250.00, 0),
(9, 2, 1, 78000.00, 0),
(9, 5, 3, 3250.00, 0),
(10, 1, 1, 95000.00, 5),
(11, 3, 4, 18500.00, 0),
(11, 4, 10, 1250.00, 0),
(12, 6, 2, 4600.00, 0),
(13, 1, 1, 95000.00, 0),
(13, 5, 2, 3250.00, 0),
(14, 2, 1, 78000.00, 0),
(14, 4, 6, 1250.00, 0),
(15, 1, 1, 95000.00, 10),
(15, 6, 2, 4600.00, 0);
