--2.1. Все типы JOIN
-- 2.1a) INNER JOIN: заявки × состав × товары
SELECT o.order_number, o.order_date, p.product_name, oc.product_quantity
FROM public.orders o
JOIN public.order_composition oc ON oc.order_number = o.order_number
JOIN public.product_catalog     p ON p.product_code = oc.product_code
ORDER BY o.order_number, p.product_name;

-- 2.1b) LEFT JOIN: все чеки + кассир (NULL, если не найден)
SELECT r.receipt_number, r.receipt_date, e.emp_name
FROM public.receipts r
LEFT JOIN public.employees e ON e.employee_id = r.employee_id
ORDER BY r.receipt_number;

-- 2.1c) RIGHT JOIN: все товары, даже если их нет в накладных
SELECT ic.invoice_number, p.product_code, p.product_name
FROM public.invoice_composition ic
RIGHT JOIN public.product_catalog p ON p.product_code = ic.product_code
ORDER BY p.product_code;

-- 2.1d) FULL OUTER JOIN: все поставщики и все накладные
SELECT s.supplier_code, s.supplier_name, i.invoice_number, i.invoice_date
FROM public.suppliers s
FULL JOIN public.invoices i ON i.supplier_code = s.supplier_code
ORDER BY COALESCE(s.supplier_code, -1), COALESCE(i.invoice_number, -1);

-- 2.1e) CROSS JOIN: возьмём по 2 сотрудника × 2 товара (у тебя их ≥2)
SELECT e.emp_name, p.product_name
FROM (SELECT * FROM public.employees ORDER BY employee_id LIMIT 2) e
CROSS JOIN (SELECT * FROM public.product_catalog ORDER BY product_code LIMIT 2) p;

--2.2. DISTINCT
SELECT DISTINCT product_category
FROM public.product_catalog
ORDER BY product_category;

--2.3. BETWEEN
SELECT receipt_number, receipt_date
FROM public.receipts
WHERE receipt_date BETWEEN TIMESTAMP '2025-03-05 00:00:00'
                       AND     TIMESTAMP '2025-03-05 23:59:59'
ORDER BY receipt_number;


--2.4. LIMIT
SELECT product_code, product_name, product_price
FROM public.product_catalog
ORDER BY product_price DESC
LIMIT 3;


--2.5. OFFSET
SELECT product_code, product_name, product_price
FROM public.product_catalog
ORDER BY product_code
LIMIT 2 OFFSET 1;


--2.6. LIKE / NOT LIKE
-- содержит «ло» (например, «Молоко»)
SELECT product_code, product_name
FROM public.product_catalog
WHERE product_name LIKE '%ло%';

-- исключаем «батон»
SELECT product_code, product_name
FROM public.product_catalog
WHERE product_name NOT LIKE '%батон%';


--2.7. POSIX-регулярные выражения
-- начинаются с «Яблоко» или «Банан»
SELECT product_code, product_name
FROM public.product_catalog
WHERE product_name ~ '^(Яблоко|Банан)';

-- нечувствительно к регистру: фамилии на «…ова»
SELECT employee_id, emp_name
FROM public.employees
WHERE emp_name ~* 'ова\b';


--2.8. Агрегированные данные
-- количество, минимум и максимум цен
SELECT COUNT(*) AS product_cnt,
       MIN(product_price) AS min_price,
       MAX(product_price) AS max_price
FROM public.product_catalog;

-- средняя цена по категориям
SELECT product_category, ROUND(AVG(product_price), 2) AS avg_price
FROM public.product_catalog
GROUP BY product_category
ORDER BY product_category;

--2.9. Вложенный запрос
-- товары, попадавшие в чеки
SELECT p.product_code, p.product_name
FROM public.product_catalog p
WHERE EXISTS (
  SELECT 1
  FROM public.check_composition cc
  WHERE cc.product_code = p.product_code
)
ORDER BY p.product_code;

-- товары, НЕ попадавшие в чеки
SELECT p.product_code, p.product_name
FROM public.product_catalog p
WHERE NOT EXISTS (
  SELECT 1
  FROM public.check_composition cc
  WHERE cc.product_code = p.product_code
)
ORDER BY p.product_code;


--2.10. CASE
SELECT product_code, product_name, product_price,
       CASE
         WHEN product_price >= 100 THEN 'дорогой'
         WHEN product_price >= 50  THEN 'средний'
         ELSE 'дешевый'
       END AS price_band
FROM public.product_catalog
ORDER BY product_price DESC;


--2.11. Группировка и простая сортировка
SELECT p.product_code, p.product_name,
       SUM(cc.quantity_in_check) AS sold_qty
FROM public.product_catalog p
JOIN public.check_composition cc ON cc.product_code = p.product_code
GROUP BY p.product_code, p.product_name
ORDER BY sold_qty DESC;


--2.12. Группировка с условием и многоуровневой сортировкой
SELECT s.supplier_name,
       p.product_category,
       SUM(ic.product_quantity) AS total_qty
FROM public.invoice_composition ic
JOIN public.invoices  i ON i.invoice_number = ic.invoice_number
JOIN public.suppliers s ON s.supplier_code  = i.supplier_code
JOIN public.product_catalog p ON p.product_code = ic.product_code
GROUP BY s.supplier_name, p.product_category
HAVING SUM(ic.product_quantity) > 50
ORDER BY s.supplier_name ASC, total_qty DESC;
