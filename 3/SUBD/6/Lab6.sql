--простое представление
CREATE OR REPLACE VIEW public.active_receipts AS
SELECT
    r.receipt_number,
    r.receipt_date,
    r.cash_register_number,
    e.emp_name AS cashier_name
FROM public.receipts r
JOIN public.employees e ON e.employee_id = r.employee_id
WHERE r.receipt_date >= CURRENT_DATE - INTERVAL '30 days';
--Проверка и откат
SELECT * FROM public.active_receipts;
DROP MATERIALIZED VIEW IF EXISTS public.active_receipts;

--материализованоое представление
CREATE MATERIALIZED VIEW public.product_sales_summary AS
SELECT
    p.product_code,
    p.product_name,
    p.product_category,
    p.product_price,
    COALESCE(SUM(cc.quantity_in_check), 0) AS total_sold,
    COALESCE(SUM(cc.quantity_in_check * p.product_price), 0) AS total_revenue
FROM public.product_catalog p
LEFT JOIN public.check_composition cc ON cc.product_code = p.product_code
GROUP BY p.product_code, p.product_name, p.product_category, p.product_price;
--Проверка и откат
SELECT * FROM public.product_sales_summary;
DROP MATERIALIZED VIEW IF EXISTS public.product_sales_summary;

--материализованное представление
CREATE MATERIALIZED VIEW public.supplier_invoice_totals AS
SELECT
    s.supplier_code,
    s.supplier_name,
    SUM(ic.product_quantity) AS total_supplied
FROM public.suppliers s
JOIN public.invoices i ON i.supplier_code = s.supplier_code
JOIN public.invoice_composition ic ON ic.invoice_number = i.invoice_number
GROUP BY s.supplier_code, s.supplier_name;
--Проверка и откат
SELECT * FROM public.supplier_invoice_totals;
DROP MATERIALIZED VIEW IF EXISTS public.supplier_invoice_totals;

--запрос с вложенным подзапросом
SELECT product_name, total_sold
FROM public.product_sales_summary
WHERE total_sold > (
    SELECT AVG(total_sold)
    FROM public.product_sales_summary
);

--запрос с группировкой и простой сортировкой
SELECT
    product_category,
    SUM(total_revenue) AS category_revenue
FROM public.product_sales_summary
GROUP BY product_category
ORDER BY category_revenue DESC;

--запрос с группировкой и многоуровневой сортировкой
SELECT supplier_name, supplier_code, total_supplied
FROM public.supplier_invoice_totals
ORDER BY supplier_name ASC,total_supplied DESC;
