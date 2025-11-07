/*Процедура обновления,ее вызов и проверка результата*/
CREATE OR REPLACE PROCEDURE public.add_receipt_with_items(
    p_receipt_number INTEGER,
    p_receipt_date TIMESTAMP,
    p_cash_register_number INTEGER,
    p_employee_id INTEGER,
    p_items JSONB  -- массив объектов: [{"product_code": 100, "quantity": 2}, ...]
)
LANGUAGE plpgsql AS $$
DECLARE
    item JSONB;
    v_product_code INTEGER;
    v_quantity INTEGER;
BEGIN
    -- Проверка существования сотрудника
    IF NOT EXISTS (SELECT 1 FROM public.employees WHERE employee_id = p_employee_id) THEN
        RAISE EXCEPTION 'Сотрудник с ID % не найден', p_employee_id;
    END IF;

    -- Проверка даты (не из будущего)
    IF p_receipt_date > CURRENT_TIMESTAMP THEN
        RAISE EXCEPTION 'Дата чека не может быть из будущего';
    END IF;

    -- Вставка чека
    INSERT INTO public.receipts (
        receipt_number, receipt_date, cash_register_number, employee_id
    ) VALUES (
        p_receipt_number, p_receipt_date, p_cash_register_number, p_employee_id
    );

    -- Вставка состава чека
    FOR item IN SELECT * FROM jsonb_array_elements(p_items)
    LOOP
        v_product_code := (item->>'product_code')::INTEGER;
        v_quantity := (item->>'quantity')::INTEGER;

        -- Проверка товара
        IF NOT EXISTS (SELECT 1 FROM public.product_catalog WHERE product_code = v_product_code) THEN
            RAISE EXCEPTION 'Товар с кодом % не найден в каталоге', v_product_code;
        END IF;

        -- Проверка количества
        IF v_quantity <= 0 THEN
            RAISE EXCEPTION 'Количество товара должно быть > 0';
        END IF;

        INSERT INTO public.check_composition (receipt_number, product_code, quantity_in_check)
        VALUES (p_receipt_number, v_product_code, v_quantity);
    END LOOP;

    RAISE NOTICE 'Чек % успешно добавлен с % позициями', p_receipt_number, jsonb_array_length(p_items);
END;
$$;

CALL public.add_receipt_with_items(
    70003,
    '2025-10-31 14:30:00'::TIMESTAMP,
    1,
    1,
    '[{"product_code": 100, "quantity": 5}, {"product_code": 200, "quantity": 2}]'::JSONB
);

-- Чек создан?
SELECT * FROM public.receipts WHERE receipt_number = 70003;

-- Состав чека добавлен?
SELECT * FROM public.check_composition WHERE receipt_number = 70003;

-- Удаляем состав чека (иначе FOREIGN KEY не даст удалить чек)
DELETE FROM public.check_composition
WHERE receipt_number = 70003;

-- Удаляем сам чек
DELETE FROM public.receipts
WHERE receipt_number = 70003;

--Удаление 
DROP PROCEDURE public.add_receipt_with_items;

/*Процедура обновления, ее вызов и проверка результата*/
CREATE OR REPLACE PROCEDURE public.update_product_price(
    p_product_code INTEGER,
    p_new_price NUMERIC(10,2)
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_new_price < 0 THEN
        RAISE EXCEPTION 'Цена не может быть отрицательной';
    END IF;

    UPDATE public.product_catalog
    SET product_price = p_new_price
    WHERE product_code = p_product_code;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Товар с кодом % не найден', p_product_code;
    END IF;

    RAISE NOTICE 'Цена товара % обновлена на %', p_product_code, p_new_price;
END;
$$;
--Откат
BEGIN;

-- Вызов процедуры
CALL public.update_product_price(100, 40.00);

-- Проверка результата
SELECT product_code, product_name, product_price
FROM public.product_catalog
WHERE product_code = 100;

ROLLBACK;

/*Процедура удаления*/
CREATE OR REPLACE PROCEDURE public.delete_old_orders(
    p_older_than_days INTEGER DEFAULT 365
)
LANGUAGE plpgsql AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM public.orders
    WHERE order_date <= CURRENT_DATE - p_older_than_days::INTEGER;

    DELETE FROM public.orders
    WHERE order_date <= CURRENT_DATE - p_older_than_days::INTEGER;

    RAISE NOTICE 'Удалено % старых заявок (старше % дней)', v_count, p_older_than_days;
END;
$$;
BEGIN;
CALL public.delete_old_orders(1);

-- Сколько заявок осталось?
SELECT * FROM public.orders;
ROLLBACK;
/*Функция получения суммы по чеку*/
CREATE OR REPLACE FUNCTION public.get_total_receipt_amount(
    p_receipt_number INTEGER
) RETURNS NUMERIC(10,2)
LANGUAGE plpgsql AS $$
DECLARE
    v_total NUMERIC(10,2);
BEGIN
    SELECT COALESCE(SUM(cc.quantity_in_check * pc.product_price), 0)
    INTO v_total
    FROM public.check_composition cc
    JOIN public.product_catalog pc ON pc.product_code = cc.product_code
    WHERE cc.receipt_number = p_receipt_number;

    RETURN v_total;
END;
$$;

SELECT public.get_total_receipt_amount(70001) AS total_amount;


/*Функция отчета по товарам сотрудника*/
CREATE OR REPLACE FUNCTION public.get_employee_sales_report(
    p_employee_id INTEGER,
    p_start_date DATE,
    p_end_date DATE
)
RETURNS TABLE (
    product_name TEXT,
    total_quantity INTEGER,
    total_revenue NUMERIC(10,2)
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        pc.product_name,
        SUM(cc.quantity_in_check)::INTEGER AS total_quantity,
        SUM(cc.quantity_in_check * pc.product_price)::NUMERIC(10,2) AS total_revenue
    FROM public.receipts r
    JOIN public.check_composition cc ON cc.receipt_number = r.receipt_number
    JOIN public.product_catalog pc ON pc.product_code = cc.product_code
    WHERE r.employee_id = p_employee_id
      AND r.receipt_date::DATE BETWEEN p_start_date AND p_end_date
    GROUP BY pc.product_name
    ORDER BY total_revenue DESC;
END;
$$;

SELECT *
FROM public.get_employee_sales_report(
    p_employee_id := 1,
    p_start_date := '2025-03-01',
    p_end_date := '2025-03-31'
);
