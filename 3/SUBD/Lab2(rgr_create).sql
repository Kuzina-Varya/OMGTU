-- >>> создание бд по ргр
DROP DATABASE IF EXISTS rgr_store;

CREATE DATABASE rgr_store
WITH
  OWNER = postgres
  ENCODING = 'UTF8'
  TEMPLATE = template0
  LC_COLLATE = 'Russian_Russia.1251'
  LC_CTYPE   = 'Russian_Russia.1251';


COMMENT ON DATABASE rgr_store
  IS 'RGR: база данных для оформления заказов/чеков/накладных';


