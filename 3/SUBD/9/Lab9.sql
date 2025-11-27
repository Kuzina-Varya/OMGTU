
-- === Очистка  ===

-- Удаляем хранимые процедуры
DROP PROCEDURE IF EXISTS public.report_employee_sales(INTEGER);
DROP PROCEDURE IF EXISTS public.find_unsold_products();
DROP PROCEDURE IF EXISTS public.update_product_code(INTEGER, INTEGER);

-- Удаляем вспомогательные таблицы
DROP TABLE IF EXISTS public.unsold_products;

-- === Задача 1: Отчёт по продажам сотрудника (курсор в процедуре) ===

CREATE OR REPLACE PROCEDURE public.report_employee_sales(
    p_employee_id INTEGER
)
LANGUAGE plpgsql AS $$
DECLARE
    -- Объявляем курсор: выбирает все чеки сотрудника
    cur_sales CURSOR FOR
        SELECT r.receipt_number, r.receipt_date, p.product_name, cc.quantity_in_check, p.product_price
        FROM public.receipts r
        JOIN public.check_composition cc ON cc.receipt_number = r.receipt_number
        JOIN public.product_catalog p ON p.product_code = cc.product_code
        WHERE r.employee_id = p_employee_id
        ORDER BY r.receipt_date;

    -- Переменные для хранения строки из курсора
    v_receipt_number INTEGER;
    v_receipt_date TIMESTAMP;
    v_product_name TEXT;
    v_quantity INTEGER;
    v_price NUMERIC(10,2);
    v_total NUMERIC(10,2) := 0;
BEGIN
    RAISE NOTICE '=== Отчёт по продажам сотрудника ID=% ===', p_employee_id;

    -- Открываем курсор
    OPEN cur_sales;
    LOOP
        -- Читаем следующую строку
        FETCH cur_sales INTO v_receipt_number, v_receipt_date, v_product_name, v_quantity, v_price;
        -- Если строк больше нет — выходим из цикла
        EXIT WHEN NOT FOUND;

        -- Выводим детальную строку
        RAISE NOTICE 'Чек % от %: % × % ед. по % руб. = % руб.',
            v_receipt_number,
            v_receipt_date,
            v_product_name,
            v_quantity,
            v_price,
            v_quantity * v_price;

        -- Накапливаем общий итог
        v_total := v_total + (v_quantity * v_price);
    END LOOP;
    CLOSE cur_sales;

    RAISE NOTICE 'Итого по сотруднику: % руб.', v_total;
END;
$$;

-- === Задача 2: Товары без продаж → таблица unsold_products ===

-- Создаём вспомогательную таблицу
CREATE TABLE IF NOT EXISTS public.unsold_products (
    product_code INTEGER PRIMARY KEY,
    product_name TEXT,
    product_category TEXT,
    product_price NUMERIC(10,2)
);

CREATE OR REPLACE PROCEDURE public.find_unsold_products()
LANGUAGE plpgsql AS $$
DECLARE
    -- Курсор: все товары, которых нет в check_composition
    cur_unsold CURSOR FOR
        SELECT p.product_code, p.product_name, p.product_category, p.product_price
        FROM public.product_catalog p
        WHERE NOT EXISTS (
            SELECT 1 FROM public.check_composition cc WHERE cc.product_code = p.product_code
        );
    rec RECORD;
BEGIN
    -- Очищаем таблицу перед новым запуском
    TRUNCATE public.unsold_products;

    RAISE NOTICE 'Ищем товары без продаж...';

    OPEN cur_unsold;
    LOOP
        FETCH cur_unsold INTO rec;
        EXIT WHEN NOT FOUND;

        -- Вставляем "нераспроданный" товар
        INSERT INTO public.unsold_products (product_code, product_name, product_category, product_price)
        VALUES (rec.product_code, rec.product_name, rec.product_category, rec.product_price);

        RAISE NOTICE 'Товар без продаж: % (код %)', rec.product_name, rec.product_code;
    END LOOP;
    CLOSE cur_unsold;

    RAISE NOTICE 'Найдено % нераспроданных товаров.', (SELECT COUNT(*) FROM public.unsold_products);
END;
$$;

-- === Задача 3: Обновление кода товара вручную (без каскада) ===

CREATE OR REPLACE PROCEDURE public.update_product_code(
    p_old_code INTEGER,
    p_new_code INTEGER
)
LANGUAGE plpgsql AS $$
DECLARE
    -- 3 курсора по трём составам
    cur_orders CURSOR FOR SELECT order_number, product_quantity FROM public.order_composition WHERE product_code = p_old_code;
    cur_checks CURSOR FOR SELECT receipt_number, quantity_in_check FROM public.check_composition WHERE product_code = p_old_code;
    cur_invoices CURSOR FOR SELECT invoice_number, product_quantity FROM public.invoice_composition WHERE product_code = p_old_code;

    -- Вспомогательные переменные
    v_order_number INTEGER;
    v_quantity_oc INTEGER;
    v_receipt_number INTEGER;
    v_quantity_cc INTEGER;
    v_invoice_number INTEGER;
    v_quantity_ic INTEGER;
BEGIN
    RAISE NOTICE 'Обновляем код товара % → %', p_old_code, p_new_code;

    -- Обновляем order_composition
    OPEN cur_orders;
    LOOP
        FETCH cur_orders INTO v_order_number, v_quantity_oc;
        EXIT WHEN NOT FOUND;
        UPDATE public.order_composition
        SET product_code = p_new_code
        WHERE order_number = v_order_number AND product_code = p_old_code;
    END LOOP;
    CLOSE cur_orders;

    -- Обновляем check_composition
    OPEN cur_checks;
    LOOP
        FETCH cur_checks INTO v_receipt_number, v_quantity_cc;
        EXIT WHEN NOT FOUND;
        UPDATE public.check_composition
        SET product_code = p_new_code
        WHERE receipt_number = v_receipt_number AND product_code = p_old_code;
    END LOOP;
    CLOSE cur_checks;

    -- Обновляем invoice_composition
    OPEN cur_invoices;
    LOOP
        FETCH cur_invoices INTO v_invoice_number, v_quantity_ic;
        EXIT WHEN NOT FOUND;
        UPDATE public.invoice_composition
        SET product_code = p_new_code
        WHERE invoice_number = v_invoice_number AND product_code = p_old_code;
    END LOOP;
    CLOSE cur_invoices;

    RAISE NOTICE 'Код товара обновлён во всех составах.';
END;
$$;

-- === Демонстрация работы (выполни по частям на защите) ===

-- Вызов 1: отчёт по сотруднику 1
CALL public.report_employee_sales(1);
-- → в Messages: детальные строки чеков и итог

-- Вызов 2: найти товары без продаж
CALL public.find_unsold_products();
-- → в Messages: список нераспроданных товаров
SELECT * FROM unsold_products;

-- Вызов 3: обновить код товара (пример: 101 → 150)
-- Сначала убедис, что 150 не существует
INSERT INTO public.product_catalog (product_code, product_name, product_category, product_price)
VALUES (150, 'Банан NEW', 'Фрукты', 55.00)
ON CONFLICT DO NOTHING;

CALL public.update_product_code(101, 150);
-- → проверка: SELECT * FROM check_composition WHERE product_code = 150;
-- → откат: DELETE FROM product_catalog WHERE product_code = 150;

