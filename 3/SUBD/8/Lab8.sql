
--  Часть 1. Транзакция с точкой сохранения
-- Явная транзакция позволяет группировать несколько операций как единое целое.
-- Команда BEGIN сообщает СУБД: «С этого момента все операции — часть одной транзакции».
BEGIN;

-- 1. Добавляем первый тестовый товар (он должен остаться после COMMIT)
--    Используем уникальные коды (999, 888, 777), чтобы не конфликтовать с реальными товарами из Lab3.
INSERT INTO public.product_catalog (product_code, product_name, product_category, product_price)
VALUES (999, 'Тестовый товар 1', 'Тест', 10.00);

-- Устанавливаем точку сохранения (SAVEPOINT) — это «чекпоинт» внутри транзакции.
-- Всё, что будет выполнено ПОСЛЕ этой точки, можно будет откатить, не теряя изменений ДО неё.
SAVEPOINT sp_after_first_product;

-- 2. Добавляем второй товар и заявку с его участием.
--    Это «рискованная» часть — она будет отменена.
INSERT INTO public.product_catalog (product_code, product_name, product_category, product_price)
VALUES (888, 'Тестовый товар 2', 'Тест', 20.00);

INSERT INTO public.orders (order_number, order_date)
VALUES (5555, CURRENT_DATE);

INSERT INTO public.order_composition (order_number, product_code, product_quantity)
VALUES (5555, 888, 5);

--  Откат к точке сохранения.
--    Команда ROLLBACK TO отменяет ВСЕ изменения, сделанные после SAVEPOINT,
--    но НЕ отменяет то, что было до неё (товар 999 остаётся).
--    Транзакция ПРОДОЛЖАЕТСЯ — можно выполнять новые команды.
ROLLBACK TO SAVEPOINT sp_after_first_product;

-- 3. Вместо отменённого товара добавляем другой — это демонстрирует гибкость частичного отката.
INSERT INTO public.product_catalog (product_code, product_name, product_category, product_price)
VALUES (777, 'Тестовый товар 3', 'Тест', 30.00);

--  Фиксация транзакции.
--    Все оставшиеся изменения (товары 999 и 777) записываются в БД навсегда.
--    После COMMIT транзакция завершена.
COMMIT;

--  Проверка результата транзакции:
--    • Товар 888 и заявка 5555 должны отсутствовать → подтверждает корректный откат.
--    • Товары 999 и 777 должны присутствовать → подтверждает успешную фиксацию.
SELECT * FROM public.product_catalog WHERE product_code IN (999, 888, 777);
SELECT * FROM public.orders WHERE order_number = 5555; -- ожидается пустой результат

--ОТКАТ
ROLLBACK;
DELETE FROM public.product_catalog WHERE product_code IN (999, 888, 777);
DELETE FROM public.orders WHERE order_number = 5555;

-- ============================================================
--  Часть 2. Триггеры модификации данных (3 шт.)
-- ============================================================

-- === Триггер 1: Запрет резкого снижения цены на товаре ===

-- Функция триггера вызывается при любом UPDATE в product_catalog.
-- Она использует специальные переменные:
--   OLD — строка ДО обновления,
--   NEW — строка ПОСЛЕ обновления.
-- Проверка: новая цена < 50% от старой → ошибка.
CREATE OR REPLACE FUNCTION public.tg_check_price_drop()
RETURNS TRIGGER AS $$
BEGIN
    -- Сравниваем NEW и OLD значения
    IF NEW.product_price < OLD.product_price * 0.5 THEN
        -- RAISE EXCEPTION прерывает транзакцию и откатывает все изменения
        RAISE EXCEPTION 'Снижение цены более чем на 50%% запрещено!';
    END IF;
    -- RETURN NEW разрешает обновление
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер привязан к таблице product_catalog.
-- BEFORE UPDATE — вызывается ДО записи в БД, чтобы можно было отменить операцию.
-- FOR EACH ROW — вызывается для каждой изменяемой строки (а не один раз на весь UPDATE).
CREATE TRIGGER tg_check_product_price_update
BEFORE UPDATE ON public.product_catalog
FOR EACH ROW
EXECUTE FUNCTION public.tg_check_price_drop();

-- Попытка снизить цену на товар 100 (Яблоко) с 35.50 до 10.00 → должно быть ЗАПРЕЩЕНО
UPDATE public.product_catalog
SET product_price = 10.00
WHERE product_code = 100;
-- Ожидаем: ERROR: Снижение цены более чем на 50% запрещено!

-- === Триггер 2: Аудит создания чеков ===

-- Таблица аудита — хранит историю всех чеков.
-- SERIAL = автоинкрементный ID 
CREATE TABLE IF NOT EXISTS public.receipt_audit (
    audit_id SERIAL PRIMARY KEY,
    receipt_number INTEGER NOT NULL,
    employee_id INTEGER,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- время создания записи = время чека
);

-- Функция логирует каждый новый чек в таблицу receipt_audit.
-- Она вызывается AFTER INSERT, потому что данные уже записаны в receipts.
CREATE OR REPLACE FUNCTION public.tg_log_receipt_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.receipt_audit (receipt_number, employee_id)
    VALUES (NEW.receipt_number, NEW.employee_id);
    RETURN NEW;  -- для AFTER-триггеров RETURN NEW не обязателен
END;
$$ LANGUAGE plpgsql;

-- AFTER INSERT — действие происходит ПОСЛЕ успешной вставки.
CREATE TRIGGER tg_log_receipt_insert
AFTER INSERT ON public.receipts
FOR EACH ROW
EXECUTE FUNCTION public.tg_log_receipt_insert();

-- Вставляем новый чек
INSERT INTO public.receipts (receipt_number, receipt_date, cash_register_number, employee_id)
VALUES (70100, NOW(), 1, 1);

-- Проверяем лог
SELECT * FROM public.receipt_audit WHERE receipt_number = 70100;
-- Ожидаем: 1 строка с данными чека

-- === Триггер 3: Запрет удаления чеков за сегодня ===

-- Функция проверяет дату чека.
-- OLD.receipt_date::DATE — приводим timestamp к дате для сравнения с CURRENT_DATE.
CREATE OR REPLACE FUNCTION public.tg_prevent_receipt_delete()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.receipt_date::DATE = CURRENT_DATE THEN
        RAISE EXCEPTION 'Удаление чеков за сегодня запрещено!';
    END IF;
    RETURN OLD;  -- разрешает удаление, если дата не сегодня
END;
$$ LANGUAGE plpgsql;

-- BEFORE DELETE — проверка происходит ДО удаления, чтобы можно было его отменить.
CREATE TRIGGER tg_prevent_receipt_delete
BEFORE DELETE ON public.receipts
FOR EACH ROW
EXECUTE FUNCTION public.tg_prevent_receipt_delete();

-- Попытка удалить только что созданный чек (дата = сегодня)
DELETE FROM public.receipts WHERE receipt_number = 70100;
-- Ожидаем: ERROR: Удаление чеков за сегодня запрещено!

-- ============================================================
--  Часть 3. Триггеры событий (2 шт.)
-- Срабатывают не на изменение данных, а на изменение СТРУКТУРЫ БД (DDL).
-- ============================================================

-- === Триггер события 1: Логирование создания таблиц ===

-- Таблица для хранения истории DDL-операций.
CREATE TABLE IF NOT EXISTS public.ddl_log (
    id SERIAL PRIMARY KEY,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tag TEXT,          -- тип команды (например, 'CREATE TABLE')
    object_name TEXT   -- имя созданного объекта
);

-- Функция использует системную функцию pg_event_trigger_ddl_commands(),
-- которая возвращает список всех объектов, созданных в текущей DDL-команде.
CREATE OR REPLACE FUNCTION public.evtr_log_table_create()
RETURNS EVENT_TRIGGER AS $$
BEGIN
    INSERT INTO public.ddl_log (tag, object_name)
    SELECT 'CREATE TABLE', obj.object_identity
    FROM pg_event_trigger_ddl_commands() AS obj
    WHERE obj.object_type = 'table';  -- логируем только таблицы
END;
$$ LANGUAGE plpgsql;

-- EVENT TRIGGER работает на уровне всей БД.
-- ON ddl_command_end — срабатывает ПОСЛЕ выполнения DDL-команды.
-- WHEN TAG IN (...) — фильтр по типу команды.
CREATE EVENT TRIGGER evtr_log_table_create
ON ddl_command_end
WHEN TAG IN ('CREATE TABLE')
EXECUTE FUNCTION public.evtr_log_table_create();

-- Создаём временную таблицу
CREATE TABLE public.test_trigger_table (id INTEGER);

-- Проверяем лог
SELECT * FROM public.ddl_log WHERE object_name = 'public.test_trigger_table';
-- Ожидаем: 1 строка с записью о создании

-- === Триггер события 2: Блокировка удаления таблиц из схемы public ===

-- Функция использует pg_event_trigger_dropped_objects() — системная функция,
-- возвращающая список удаляемых объектов.
CREATE OR REPLACE FUNCTION public.evtr_block_drop_table()
RETURNS EVENT_TRIGGER AS $$
DECLARE
    obj RECORD;  -- переменная для перебора результата запроса
BEGIN
    -- Проходим по всем удаляемым объектам
    FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
    WHERE object_type = 'table' AND schema_name = 'public'
    LOOP
        -- Если хоть один — таблица из public → прерываем выполнение
        RAISE EXCEPTION 'Удаление таблиц из схемы public запрещено!';
    END LOOP;
    -- Если цикл ничего не нашёл — удаление разрешено (например, DROP VIEW)
END;
$$ LANGUAGE plpgsql;

-- ON sql_drop — срабатывает ПРИ ПОПЫТКЕ удаления объектов.
CREATE EVENT TRIGGER evtr_block_drop_table_in_public
ON sql_drop
EXECUTE FUNCTION public.evtr_block_drop_table();

-- Попытка удалить тестовую таблицу
DROP TABLE public.test_trigger_table;
-- Ожидаем: ERROR: Удаление таблиц из схемы public запрещено!

--ОТКАТ
-- === 1. Удаляем обычные триггеры и функции ===
DROP TRIGGER IF EXISTS tg_check_product_price_update ON public.product_catalog;
DROP FUNCTION IF EXISTS public.tg_check_price_drop();

DROP TRIGGER IF EXISTS tg_log_receipt_insert ON public.receipts;
DROP FUNCTION IF EXISTS public.tg_log_receipt_insert();

DROP TRIGGER IF EXISTS tg_prevent_receipt_delete ON public.receipts;
DROP FUNCTION IF EXISTS public.tg_prevent_receipt_delete();

-- === 2. Удаляем триггеры событий и функции ===
DROP EVENT TRIGGER IF EXISTS evtr_log_table_create;
DROP EVENT TRIGGER IF EXISTS evtr_block_drop_table_in_public;
DROP FUNCTION IF EXISTS public.evtr_log_table_create();
DROP FUNCTION IF EXISTS public.evtr_block_drop_table();

-- === 3. Удаляем вспомогательные таблицы ===
DROP TABLE IF EXISTS public.receipt_audit;
DROP TABLE IF EXISTS public.ddl_log;

-- === 4. Очищаем следы тестовых данных ===
DELETE FROM public.receipts WHERE receipt_number = 70100;
DROP TABLE IF EXISTS public.test_trigger_table;  -- на случай, если триггер защиты отключили
