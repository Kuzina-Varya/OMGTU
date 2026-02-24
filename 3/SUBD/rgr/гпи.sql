-- Удаляем БД, если она уже существует (чтобы не было конфликтов)
DROP DATABASE IF EXISTS goodreads;

-- Создаём новую БД с нужными параметрами
CREATE DATABASE goodreads
WITH
  OWNER = postgres
  ENCODING = 'UTF8'
  LC_COLLATE = 'Russian_Russia.1251'
  LC_CTYPE = 'Russian_Russia.1251'
  TEMPLATE = template0;