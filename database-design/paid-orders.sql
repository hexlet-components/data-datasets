CREATE TABLE products (
    id integer PRIMARY KEY,
    name text NOT NULL,
    price_rub numeric(12, 2) NOT NULL CHECK (price_rub >= 0)
);

-- Каждая покупка в этом магазине содержит одну единицу товара.
CREATE TABLE paid_orders (
    id integer PRIMARY KEY,
    product_id integer NOT NULL REFERENCES products (id),
    paid_rub numeric(12, 2) NOT NULL CHECK (paid_rub >= 0)
);

INSERT INTO products (id, name, price_rub) VALUES
    (1, 'Кружка', 590.00),
    (2, 'Блокнот', 120.00);

INSERT INTO paid_orders (id, product_id, paid_rub) VALUES
    (101, 1, 450.00),
    (102, 2, 119.95);
