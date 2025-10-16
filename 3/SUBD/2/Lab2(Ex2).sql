DROP TABLE IF EXISTS items       CASCADE;
DROP TABLE IF EXISTS orders      CASCADE;
DROP TABLE IF EXISTS employees   CASCADE;
DROP TABLE IF EXISTS products    CASCADE;
DROP TABLE IF EXISTS customers   CASCADE;
DROP TABLE IF EXISTS manufacturers CASCADE;
DROP TABLE IF EXISTS categories  CASCADE;

CREATE TABLE public.categories (
  cat_ID      integer     NOT NULL,
  cat_name    text        NOT NULL,
  cat_overcat integer,
  CONSTRAINT categories_PK PRIMARY KEY (cat_ID)
);

CREATE TABLE public.manufacturers (
  man_ID      integer   NOT NULL,
  man_name    text      NOT NULL,
  man_address text      NOT NULL,
  CONSTRAINT manufacturers_PK PRIMARY KEY (man_ID)
);

CREATE TABLE public.products (
  prod_ID     integer      NOT NULL,
  prod_name   text         NOT NULL,
  prod_price  numeric(8,2) NOT NULL,
  prod_rest   integer      NOT NULL,
  prod_cat_ID integer      NOT NULL,
  prod_man_ID integer      NOT NULL,
  CONSTRAINT products_PK PRIMARY KEY (prod_ID)
);

CREATE TABLE public.customers (
  cust_ID       integer NOT NULL,
  cust_name     text    NOT NULL,
  cust_address  text    NOT NULL,
  cust_discount integer NOT NULL,
  CONSTRAINT customers_PK PRIMARY KEY (cust_ID)
);

CREATE TABLE public.employees (
  emp_ID       integer NOT NULL,
  emp_name     text    NOT NULL,
  emp_position text    NOT NULL,
  CONSTRAINT employees_PK PRIMARY KEY (emp_ID)
);

CREATE TABLE public.orders (
  ord_ID     integer NOT NULL,
  ord_cust_ID integer NOT NULL,
  ord_emp_ID  integer NOT NULL,
  ord_date    date    NOT NULL,
  CONSTRAINT orders_PK PRIMARY KEY (ord_ID)
);

CREATE TABLE public.items (
  item_ID       integer NOT NULL,
  item_ord_ID   integer NOT NULL,
  item_prod_ID  integer NOT NULL,
  item_prod_count integer NOT NULL,
  CONSTRAINT items_PK PRIMARY KEY (item_ID)
);

ALTER TABLE public.categories
  ADD CONSTRAINT categories_FK
  FOREIGN KEY (cat_overcat)
  REFERENCES public.categories (cat_ID)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE public.products
  ADD CONSTRAINT products_FK1
  FOREIGN KEY (prod_cat_ID)
  REFERENCES public.categories (cat_ID)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE public.products
  ADD CONSTRAINT products_FK2
  FOREIGN KEY (prod_man_ID)
  REFERENCES public.manufacturers (man_ID)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE public.orders
  ADD CONSTRAINT orders_FK1
  FOREIGN KEY (ord_cust_ID)
  REFERENCES public.customers (cust_ID)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE public.orders
  ADD CONSTRAINT orders_FK2
  FOREIGN KEY (ord_emp_ID)
  REFERENCES public.employees (emp_ID)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE public.items
  ADD CONSTRAINT items_FK1
  FOREIGN KEY (item_ord_ID)
  REFERENCES public.orders (ord_ID)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE public.items
  ADD CONSTRAINT items_FK2
  FOREIGN KEY (item_prod_ID)
  REFERENCES public.products (prod_ID)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

-- все таблицы в public
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- внешние ключи
SELECT conname, conrelid::regclass AS table_name, confrelid::regclass AS ref_table
FROM pg_constraint
WHERE contype = 'f'
ORDER BY conname;