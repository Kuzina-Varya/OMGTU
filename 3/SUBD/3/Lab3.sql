-- Очистка (при повторе)
TRUNCATE TABLE
  invoice_composition,
  invoices,
  check_composition,
  receipts,
  order_composition,
  orders,
  product_catalog,
  employees,
  suppliers
RESTART IDENTITY CASCADE;

-- Сотрудникик,поставщики,продукты
INSERT INTO employees (employee_id, emp_name, emp_position) VALUES
  (1,'Иванова А.А.','кассир'),
  (2,'Петров П.П.','менеджер'),
  (3,'Сидорова С.С.','кладовщик');

INSERT INTO suppliers (supplier_code, supplier_name) VALUES
  (10,'ООО «ФруТорг»'),
  (20,'АО «Продукты+»');

INSERT INTO product_catalog (product_code, product_name, product_category, product_price) VALUES
  (100,'Яблоко','Фрукты',35.50),
  (101,'Банан','Фрукты',49.90),
  (200,'Молоко 1л','Молочные',79.00),
  (300,'Хлеб батон','Хлеб',29.00);

-- Заявки и состав
INSERT INTO orders (order_number, order_date) VALUES
  (5001, DATE '2025-03-01'),
  (5002, DATE '2025-03-02');

INSERT INTO order_composition (order_number, product_code, product_quantity) VALUES
  (5001,100,20),
  (5001,200,10),
  (5002,101,15),
  (5002,300,25);

-- Чеки и состав
INSERT INTO receipts (receipt_number, receipt_date, cash_register_number, employee_id) VALUES
  (70001, TIMESTAMP '2025-03-05 10:15:00', 1, 1),
  (70002, TIMESTAMP '2025-03-05 11:20:00', 1, 1);

INSERT INTO check_composition (receipt_number, product_code, quantity_in_check) VALUES
  (70001,100,3),
  (70001,300,1),
  (70002,200,2),
  (70002,101,4);

-- Накладные и состав
INSERT INTO invoices (invoice_number, invoice_date, supplier_code) VALUES
  (9001, DATE '2025-03-03', 10),
  (9002, DATE '2025-03-04', 20);

INSERT INTO invoice_composition (invoice_number, product_code, product_quantity) VALUES
  (9001,100,100),
  (9001,200,60),
  (9002,101,80),
  (9002,300,120);


SELECT * FROM employees ORDER BY employee_id;
SELECT * FROM suppliers ORDER BY supplier_code;
SELECT * FROM product_catalog ORDER BY product_code;
SELECT * FROM orders ORDER BY order_number;
SELECT * FROM order_composition ORDER BY order_number, product_code;
SELECT * FROM receipts ORDER BY receipt_number;
SELECT * FROM check_composition ORDER BY receipt_number, product_code;
SELECT * FROM invoices ORDER BY invoice_number;
SELECT * FROM invoice_composition ORDER BY invoice_number, product_code;


-- ВНИМАНИЕ: выполняем в rgr_store
-- Каждый тест в savepoint'е, чтобы база не менялась
BEGIN;  -- <<< открыли явную транзакцию
-----------------------------
-- 1. CHECK и NOT NULL
-----------------------------
-- 1.1 employees: emp_name не пустой (NOT NULL + not blank)
SAVEPOINT s1;
  INSERT INTO public.employees(employee_id, emp_name, emp_position)
  VALUES (9999, NULL, 'кассир');               -- ожидаем ERROR: NOT NULL
ROLLBACK TO SAVEPOINT s1;

SAVEPOINT s1b;
  INSERT INTO public.employees(employee_id, emp_name, emp_position)
  VALUES (9998, '   ', 'кассир');              -- ожидаем ERROR: employees_name_notblank
ROLLBACK TO SAVEPOINT s1b;

-- 1.2 employees: положительный ID
SAVEPOINT s2;
  INSERT INTO public.employees(employee_id, emp_name, emp_position)
  VALUES (-1, 'Иванов', 'кассир');             -- ожидаем ERROR: employees_id_pos_chk
ROLLBACK TO SAVEPOINT s2;

-- 1.3 suppliers: имя не пустое, код > 0
SAVEPOINT s3;
  INSERT INTO public.suppliers(supplier_code, supplier_name)
  VALUES (0, 'ООО Тест');                      -- ожидаем ERROR: suppliers_code_pos_chk
ROLLBACK TO SAVEPOINT s3;

SAVEPOINT s3b;
  INSERT INTO public.suppliers(supplier_code, supplier_name)
  VALUES (999, '   ');                         -- ожидаем ERROR: suppliers_name_notblank
ROLLBACK TO SAVEPOINT s3b;

-- 1.4 product_catalog: цена неотрицательная, имя/категория не пустые, код > 0
SAVEPOINT s4;
  INSERT INTO public.product_catalog(product_code, product_name, product_category, product_price)
  VALUES (100, 'Дубль', 'Разное', -1.00);      -- PK-дубль + ERROR: products_price_nonneg_chk
ROLLBACK TO SAVEPOINT s4;

SAVEPOINT s4b;
  INSERT INTO public.product_catalog(product_code, product_name, product_category, product_price)
  VALUES (9999, ' ', 'Фрукты', 10);            -- ERROR: products_name_notblank
ROLLBACK TO SAVEPOINT s4b;

-- 1.5 orders: номер > 0, дата не из будущего
SAVEPOINT s5;
  INSERT INTO public.orders(order_number, order_date)
  VALUES (0, CURRENT_DATE);                    -- ERROR: orders_num_pos_chk
ROLLBACK TO SAVEPOINT s5;

SAVEPOINT s5b;
  INSERT INTO public.orders(order_number, order_date)
  VALUES (9999, CURRENT_DATE + INTERVAL '1 day'); -- ERROR: orders_date_past_chk
ROLLBACK TO SAVEPOINT s5b;

-- 1.6 order_composition: количество > 0
SAVEPOINT s6;
  INSERT INTO public.order_composition(order_number, product_code, product_quantity)
  VALUES (5001, 100, 0);                       -- ERROR: oc_qty_pos_chk
ROLLBACK TO SAVEPOINT s6;

-- 1.7 receipts: номер/касса > 0, дата не из будущего
SAVEPOINT s7;
  INSERT INTO public.receipts(receipt_number, receipt_date, cash_register_number, employee_id)
  VALUES (0, now(), 1, 1);                     -- ERROR: receipts_num_pos_chk
ROLLBACK TO SAVEPOINT s7;

SAVEPOINT s7b;
  INSERT INTO public.receipts(receipt_number, receipt_date, cash_register_number, employee_id)
  VALUES (70099, now() + INTERVAL '1 day', 1, 1); -- ERROR: receipts_date_past_chk
ROLLBACK TO SAVEPOINT s7b;

SAVEPOINT s7c;
  INSERT INTO public.receipts(receipt_number, receipt_date, cash_register_number, employee_id)
  VALUES (70098, now(), 0, 1);                 -- ERROR: receipts_register_pos_chk
ROLLBACK TO SAVEPOINT s7c;

-- 1.8 check_composition: количество > 0
SAVEPOINT s8;
  INSERT INTO public.check_composition(receipt_number, product_code, quantity_in_check)
  VALUES (70001, 100, 0);                      -- ERROR: cc_qty_pos_chk
ROLLBACK TO SAVEPOINT s8;

-- 1.9 invoices: номер > 0, дата не из будущего
SAVEPOINT s9;
  INSERT INTO public.invoices(invoice_number, invoice_date, supplier_code)
  VALUES (0, CURRENT_DATE, 10);                -- ERROR: invoices_num_pos_chk
ROLLBACK TO SAVEPOINT s9;

SAVEPOINT s9b;
  INSERT INTO public.invoices(invoice_number, invoice_date, supplier_code)
  VALUES (9999, CURRENT_DATE + 1, 10);         -- ERROR: invoices_date_past_chk
ROLLBACK TO SAVEPOINT s9b;

-- 1.10 invoice_composition: количество > 0
SAVEPOINT s10;
  INSERT INTO public.invoice_composition(invoice_number, product_code, product_quantity)
  VALUES (9001, 100, 0);                       -- ERROR: ic_qty_pos_chk
ROLLBACK TO SAVEPOINT s10;

-----------------------------
-- 2. PRIMARY KEY (уникальность)
-----------------------------
-- Дубликат PK в products (id 100 уже есть)
SAVEPOINT s11;
  INSERT INTO public.product_catalog(product_code, product_name, product_category, product_price)
  VALUES (100, 'Дубль', 'Разное', 10.00);      -- ERROR: duplicate key value ... pkey
ROLLBACK TO SAVEPOINT s11;

-- Составной PK: повтор товара в той же заявке/чеке/накладной
SAVEPOINT s12;
  INSERT INTO public.order_composition(order_number, product_code, product_quantity)
  VALUES (5001, 100, 1);                       -- ERROR: order_composition_pk
ROLLBACK TO SAVEPOINT s12;

SAVEPOINT s12b;
  INSERT INTO public.check_composition(receipt_number, product_code, quantity_in_check)
  VALUES (70001, 100, 1);                      -- ERROR: check_composition_pk
ROLLBACK TO SAVEPOINT s12b;

SAVEPOINT s12c;
  INSERT INTO public.invoice_composition(invoice_number, product_code, product_quantity)
  VALUES (9001, 100, 1);                       -- ERROR: invoice_composition_pk
ROLLBACK TO SAVEPOINT s12c;

-----------------------------
-- 3. FOREIGN KEY (ссылочная целостность)
-----------------------------
-- Несуществующий сотрудник в чеке
SAVEPOINT s13;
  INSERT INTO public.receipts(receipt_number, receipt_date, cash_register_number, employee_id)
  VALUES (70111, now(), 1, 999);               -- ERROR: receipts_fk_employee
ROLLBACK TO SAVEPOINT s13;

-- Несуществующий товар в составе заявки
SAVEPOINT s14;
  INSERT INTO public.order_composition(order_number, product_code, product_quantity)
  VALUES (5001, 9999, 1);                      -- ERROR: oc_fk_product
ROLLBACK TO SAVEPOINT s14;

-- Несуществующий чек в составе чека
SAVEPOINT s15;
  INSERT INTO public.check_composition(receipt_number, product_code, quantity_in_check)
  VALUES (79999, 100, 1);                      -- ERROR: cc_fk_receipt
ROLLBACK TO SAVEPOINT s15;

-- Несуществующий поставщик в накладной
SAVEPOINT s16;
  INSERT INTO public.invoices(invoice_number, invoice_date, supplier_code)
  VALUES (90111, CURRENT_DATE, 999);           -- ERROR: invoices_fk_supplier
ROLLBACK TO SAVEPOINT s16;

-----------------------------
-- 4. КАСКАДЫ (ON DELETE/UPDATE CASCADE)
-----------------------------
-- 4.1 ON DELETE CASCADE: удаляем товар 300 → записи из check_/invoice_composition по нему должны исчезнуть
SAVEPOINT s17;
  -- покажем, что строки по 300 есть:
  SELECT 'before', count(*) FROM public.check_composition   WHERE product_code = 300;
  SELECT 'before', count(*) FROM public.invoice_composition WHERE product_code = 300;

  DELETE FROM public.product_catalog WHERE product_code = 300;  -- каскад на составы

  SELECT 'after', count(*) FROM public.check_composition   WHERE product_code = 300;  -- ожидается 0
  SELECT 'after', count(*) FROM public.invoice_composition WHERE product_code = 300;  -- ожидается 0
ROLLBACK TO SAVEPOINT s17;

-- 4.2 ON UPDATE CASCADE: поменяем номер заявки → дочерние строки тоже обновятся
SAVEPOINT s18;
  -- подготовим временную заявку и её строку
  INSERT INTO public.orders(order_number, order_date) VALUES (6000, CURRENT_DATE);
  INSERT INTO public.order_composition(order_number, product_code, product_quantity)
  VALUES (6000, 100, 1);

  UPDATE public.orders SET order_number = 7000 WHERE order_number = 6000;  -- каскад на order_composition

  -- дочерняя строка должна быть уже с 7000
  SELECT * FROM public.order_composition WHERE order_number = 7000 AND product_code = 100;
ROLLBACK TO SAVEPOINT s18;

ROLLBACK; 




