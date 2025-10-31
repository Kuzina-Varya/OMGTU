-- Очистка (при повторе)
DROP TABLE IF EXISTS product_media CASCADE;
DROP TABLE IF EXISTS receipt_payments CASCADE;


-- === массивы: фотографии и тэги по товарам ===
CREATE TABLE public.product_media (
  product_code integer PRIMARY KEY
    REFERENCES public.product_catalog(product_code)
    ON DELETE CASCADE ON UPDATE CASCADE,

  photos text[] NOT NULL,                  -- массив путей/URL к фото
  tags   text[] DEFAULT '{}'::text[],      -- массив тэгов

  -- правила
  CONSTRAINT pm_photos_not_empty CHECK (cardinality(photos) > 0)
);

-- Наполнение 
INSERT INTO public.product_media(product_code, photos, tags) VALUES
  (100, ARRAY['/img/100-1.jpg','/img/100-2.jpg'], ARRAY['fruits','fresh']),
  (101, ARRAY['/img/101-1.jpg'],                  ARRAY['fruits','import']),
  (200, ARRAY['/img/200-1.jpg','/img/200-2.jpg'], ARRAY['dairy']);
-- Проверки
-- Все товары, у которых среди тэгов есть 'fruits'
SELECT pm.*
FROM public.product_media pm
WHERE pm.tags @> ARRAY['fruits'];

-- Фото по строкам
SELECT product_code, UNNEST(photos) AS photo
FROM public.product_media;

-- Кол-во фото на товар
SELECT product_code, array_length(photos, 1) AS photos_count
FROM public.product_media;


-- === JSONB: параметры платежа по чеку ===
CREATE TABLE public.receipt_payments (
  receipt_number integer PRIMARY KEY
    REFERENCES public.receipts(receipt_number)
    ON DELETE CASCADE ON UPDATE CASCADE,

  payment jsonb NOT NULL,

  -- "валидация схемы" через CHECK:
  -- 1) это объект, 2) есть ключи method и amount,
  -- 3) метод из списка, 4) amount >= 0
  CONSTRAINT rp_is_object      CHECK (jsonb_typeof(payment) = 'object'),
  CONSTRAINT rp_has_required   CHECK (payment ? 'method' AND payment ? 'amount'),
  CONSTRAINT rp_method_enum    CHECK ((payment->>'method') IN ('cash','card','qr')),
  CONSTRAINT rp_amount_non_neg CHECK (((payment->>'amount')::numeric) >= 0)
);

-- Наполнение (под твои чеки 70001, 70002)
INSERT INTO public.receipt_payments(receipt_number, payment) VALUES
  (70001, jsonb_build_object(
            'method','card',
            'amount', 214.50,
            'card_last4','1234',
            'bank','SBER'
         )),
  (70002, jsonb_build_object(
            'method','cash',
            'amount',  328.90,
            'change_given', 71.10
         ));
--Проверки
-- Чеки, оплаченные картой
SELECT r.receipt_number, p.payment->>'method' AS method, (p.payment->>'amount')::numeric AS amount
FROM public.receipt_payments p
JOIN public.receipts r USING (receipt_number)
WHERE p.payment->>'method' = 'card';

SELECT * FROM public.receipt_payments;
SELECT * FROM public.product_media;

-- Все поля JSON 
SELECT receipt_number,
       payment->>'method'          AS method,
       (payment->>'amount')::numeric AS amount,
       payment->>'bank'            AS bank,
       payment->>'card_last4'      AS last4
FROM public.receipt_payments;

-- Чеки с суммой больше 300
SELECT receipt_number
FROM public.receipt_payments
WHERE (payment->>'amount')::numeric > 300;

-- Просмотр наполнения
SELECT * FROM public.product_media ORDER BY product_code;
SELECT * FROM public.receipt_payments ORDER BY receipt_number;

-- product_media: запрещён пустой массив фотографий
INSERT INTO public.product_media(product_code, photos, tags)
VALUES (300, ARRAY[]::text[], ARRAY['bread']);  -- ОЖИДАЕМ ERROR: pm_photos_not_empty

-- receipt_payments: нарушение схемы JSON (неверный method и отрицательная сумма)
INSERT INTO public.receipt_payments(receipt_number, payment)
VALUES (70001, '{"method":"bitcoin","amount":-5}'::jsonb);  -- ОЖИДАЕМ ERROR по rp_method_enum/rp_amount_non_neg



