
  -- Чистый старт на случай повторного запуска
DROP TABLE IF EXISTS invoice_composition CASCADE;
DROP TABLE IF EXISTS invoices            CASCADE;
DROP TABLE IF EXISTS check_composition   CASCADE;
DROP TABLE IF EXISTS receipts            CASCADE;
DROP TABLE IF EXISTS order_composition   CASCADE;
DROP TABLE IF EXISTS orders              CASCADE;
DROP TABLE IF EXISTS product_catalog     CASCADE;
DROP TABLE IF EXISTS employees           CASCADE;
DROP TABLE IF EXISTS suppliers           CASCADE;

-- Сотрудники
CREATE TABLE public.employees (
  employee_id   integer PRIMARY KEY,
  emp_name      text    NOT NULL,
  emp_position  text    NOT NULL
);

-- Поставщики (логично под supplier_code во входных данных)
CREATE TABLE public.suppliers (
  supplier_code integer PRIMARY KEY,
  supplier_name text    NOT NULL
);

-- Каталог товаров
CREATE TABLE public.product_catalog (
  product_code     integer       PRIMARY KEY,
  product_name     text          NOT NULL,
  product_category text          NOT NULL,
  product_price    numeric(10,2) NOT NULL
);

-- Заявки
CREATE TABLE public.orders (
  order_number integer PRIMARY KEY,
  order_date   date    NOT NULL
);

-- Состав заявки
CREATE TABLE public.order_composition (
  order_number     integer NOT NULL,
  product_code     integer NOT NULL,
  product_quantity integer NOT NULL,
  CONSTRAINT order_composition_pk PRIMARY KEY (order_number, product_code)
);

-- Чеки
CREATE TABLE public.receipts (
  receipt_number       integer   PRIMARY KEY,
  receipt_date         timestamp NOT NULL,
  cash_register_number integer   NOT NULL,
  employee_id          integer   NOT NULL
);

-- Состав чека
CREATE TABLE public.check_composition (
  receipt_number    integer NOT NULL,
  product_code      integer NOT NULL,
  quantity_in_check integer NOT NULL,
  CONSTRAINT check_composition_pk PRIMARY KEY (receipt_number, product_code)
);

-- Накладные
CREATE TABLE public.invoices (
  invoice_number integer PRIMARY KEY,
  invoice_date   date    NOT NULL,
  supplier_code  integer NOT NULL
);

-- Состав накладной
CREATE TABLE public.invoice_composition (
  invoice_number   integer NOT NULL,
  product_code     integer NOT NULL,
  product_quantity integer NOT NULL,
  CONSTRAINT invoice_composition_pk PRIMARY KEY (invoice_number, product_code)
);






-- order_composition → orders / product_catalog
ALTER TABLE public.order_composition
  ADD CONSTRAINT oc_fk_order
  FOREIGN KEY (order_number)
  REFERENCES public.orders (order_number)
  ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE public.order_composition
  ADD CONSTRAINT oc_fk_product
  FOREIGN KEY (product_code)
  REFERENCES public.product_catalog (product_code)
  ON DELETE CASCADE ON UPDATE CASCADE;

-- receipts → employees
ALTER TABLE public.receipts
  ADD CONSTRAINT receipts_fk_employee
  FOREIGN KEY (employee_id)
  REFERENCES public.employees (employee_id)
  ON DELETE CASCADE ON UPDATE CASCADE;

-- check_composition → receipts / product_catalog
ALTER TABLE public.check_composition
  ADD CONSTRAINT cc_fk_receipt
  FOREIGN KEY (receipt_number)
  REFERENCES public.receipts (receipt_number)
  ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE public.check_composition
  ADD CONSTRAINT cc_fk_product
  FOREIGN KEY (product_code)
  REFERENCES public.product_catalog (product_code)
  ON DELETE CASCADE ON UPDATE CASCADE;

-- invoices → suppliers
ALTER TABLE public.invoices
  ADD CONSTRAINT invoices_fk_supplier
  FOREIGN KEY (supplier_code)
  REFERENCES public.suppliers (supplier_code)
  ON DELETE CASCADE ON UPDATE CASCADE;

-- invoice_composition → invoices / product_catalog
ALTER TABLE public.invoice_composition
  ADD CONSTRAINT ic_fk_invoice
  FOREIGN KEY (invoice_number)
  REFERENCES public.invoices (invoice_number)
  ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE public.invoice_composition
  ADD CONSTRAINT ic_fk_product
  FOREIGN KEY (product_code)
  REFERENCES public.product_catalog (product_code)
  ON DELETE CASCADE ON UPDATE CASCADE;





-- Таблицы в public
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname='public'
ORDER BY tablename;

-- Все внешние ключи
SELECT conname,
       conrelid::regclass  AS table_name,
       confrelid::regclass AS ref_table
FROM pg_constraint
WHERE contype='f'
ORDER BY conname;

-- Характеристики БД
SELECT
  d.datname                               AS database,
  pg_get_userbyid(d.datdba)               AS owner,
  pg_encoding_to_char(d.encoding)         AS encoding,
  d.datcollate, d.datctype,
  shobj_description(d.oid, 'pg_database') AS comment
FROM pg_database d
WHERE d.datname='rgr_store';


-- посмотри, кто держит rgr_store
SELECT pid, usename, state, query
FROM pg_stat_activity
WHERE datname = 'rgr_store';


-- завершить все чужие сессии rgr_store (кроме текущей)
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'rgr_store'
  AND pid <> pg_backend_pid();


SELECT pg_terminate_backend(8780);