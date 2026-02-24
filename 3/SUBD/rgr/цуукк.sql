CREATE DATABASE ComputerInventory
WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False
    TEMPLATE = template0;

COMMENT ON DATABASE ComputerInventory
    IS 'База данных для автоматизации учёта средств вычислительной техники в компьютерном клубе "КиберАрена"';