
DROP DATABASE IF EXISTS sales;

CREATE DATABASE sales
WITH
  OWNER = postgres
  ENCODING = 'UTF8'
  TEMPLATE = template0
  LC_COLLATE = 'Russian_Russia.1251'   
  LC_CTYPE   = 'Russian_Russia.1251'   
  TABLESPACE = pg_default
  CONNECTION LIMIT = -1
  IS_TEMPLATE = False;

COMMENT ON DATABASE sales
  IS 'База данных для службы оформления заказов на товары';

SELECT datname FROM pg_database ORDER BY datname;

SELECT
  d.datname                               AS database,
  pg_get_userbyid(d.datdba)               AS owner,
  pg_encoding_to_char(d.encoding)         AS encoding,
  d.datcollate,
  d.datctype,
  t.spcname                               AS tablespace,
  d.datconnlimit                          AS connection_limit,
  d.datistemplate                         AS is_template,
  shobj_description(d.oid, 'pg_database') AS comment,   
  pg_size_pretty(pg_database_size(d.datname)) AS db_size
FROM pg_database AS d
LEFT JOIN pg_tablespace AS t ON t.oid = d.dattablespace
WHERE d.datname = 'sales';












