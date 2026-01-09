--1. Создание базы данных и таблиц (DDL)
-- Создание таблицы Organization
CREATE TABLE Organization (
    organization_id SERIAL PRIMARY KEY,
    name_of_organization TEXT NOT NULL,
    address TEXT NOT NULL
);

-- Создание таблицы Department
CREATE TABLE Department (
    department_id SERIAL PRIMARY KEY,
    organization_id INTEGER NOT NULL REFERENCES Organization(organization_id) ON UPDATE CASCADE ON DELETE CASCADE,
    name_of_department TEXT NOT NULL
);

-- Создание таблицы Position
CREATE TABLE Position (
    position_id SERIAL PRIMARY KEY,
    name_of_position TEXT NOT NULL UNIQUE,
    description_of_position TEXT,
    salary_range TEXT
);

-- Создание таблицы Employee
CREATE TABLE Employee (
    employee_id SERIAL PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES Department(department_id) ON UPDATE CASCADE ON DELETE CASCADE,
    position_id INTEGER NOT NULL REFERENCES Position(position_id) ON UPDATE CASCADE ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    contact_information TEXT
);

-- Создание таблицы EquipmentCategory
CREATE TABLE EquipmentCategory (
    category_id SERIAL PRIMARY KEY,
    name_of_category TEXT NOT NULL,
    description_of_category TEXT
);

-- Создание таблицы ComputingEquipment
CREATE TABLE ComputingEquipment (
    equipment_id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES EquipmentCategory(category_id) ON UPDATE CASCADE ON DELETE CASCADE,
    name_of_equipment TEXT NOT NULL,
    model_of_equipment TEXT NOT NULL,
    year_manufactured INTEGER NOT NULL CHECK (year_manufactured > 1980),
    serial_number TEXT NOT NULL
);

-- Создание таблицы Component
CREATE TABLE Component (
    component_id SERIAL PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES ComputingEquipment(equipment_id) ON UPDATE CASCADE ON DELETE CASCADE,
    name_of_component TEXT NOT NULL,
    model_of_component TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    is_removable BOOLEAN NOT NULL
);

-- Создание таблицы InventoryNumber
CREATE TABLE InventoryNumber (
    inventory_number_id SERIAL PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES ComputingEquipment(equipment_id) ON UPDATE CASCADE ON DELETE CASCADE,
    number TEXT NOT NULL UNIQUE,
    date_registered DATE NOT NULL,
    acquisition_method TEXT
);

-- Создание таблицы MovementType
CREATE TABLE MovementType (
    movement_type_id SERIAL PRIMARY KEY,
    name_of_type TEXT NOT NULL UNIQUE,
    description_of_type TEXT
);

-- Создание таблицы Movement
CREATE TABLE Movement (
    movement_id SERIAL PRIMARY KEY,
    inventory_number_id INTEGER NOT NULL REFERENCES InventoryNumber(inventory_number_id) ON UPDATE CASCADE ON DELETE CASCADE,
    department_id INTEGER NOT NULL REFERENCES Department(department_id) ON UPDATE CASCADE ON DELETE CASCADE,
    employee_id INTEGER NOT NULL REFERENCES Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    movement_type_id INTEGER NOT NULL REFERENCES MovementType(movement_type_id) ON UPDATE CASCADE ON DELETE CASCADE,
    movement_date DATE NOT NULL,
    reason TEXT
);

-- Создание таблицы EquipmentCondition
CREATE TABLE EquipmentCondition (
    condition_id SERIAL PRIMARY KEY,
    name_of_condition TEXT NOT NULL UNIQUE,
    description_of_condition TEXT
);

-- Создание таблицы RegisterOfRepairWorks
CREATE TABLE RegisterOfRepairWorks (
    repair_work_id SERIAL PRIMARY KEY,
    inventory_number_id INTEGER NOT NULL REFERENCES InventoryNumber(inventory_number_id) ON UPDATE CASCADE ON DELETE CASCADE UNIQUE,
    department_id INTEGER NOT NULL REFERENCES Department(department_id) ON UPDATE CASCADE ON DELETE CASCADE,
    condition_id INTEGER NOT NULL REFERENCES EquipmentCondition(condition_id) ON UPDATE CASCADE ON DELETE CASCADE,
    last_update DATE NOT NULL
);

--2. Создание индексов
-- Индексы для ускорения поиска по часто используемым полям
CREATE INDEX idx_equipment_category ON ComputingEquipment(category_id);
CREATE INDEX idx_inventory_equipment ON InventoryNumber(equipment_id);
CREATE INDEX idx_movement_date ON Movement(movement_date);
CREATE INDEX idx_employee_department ON Employee(department_id);
CREATE INDEX idx_component_equipment ON Component(equipment_id);
CREATE INDEX idx_repair_condition ON RegisterOfRepairWorks(condition_id);
CREATE INDEX idx_movement_department ON Movement(department_id);

--3. Заполнение таблиц тестовыми данными
-- Заполнение таблицы Organization
INSERT INTO Organization (name_of_organization, address) VALUES
('КиберАрена', 'г. Москва, ул. Центральная, д. 10'),
('КиберАрена-2', 'г. Санкт-Петербург, Невский пр., д. 45'),
('КиберАрена-3', 'г. Новосибирск, ул. Ленина, д. 25');

-- Заполнение таблицы EquipmentCategory
INSERT INTO EquipmentCategory (name_of_category, description_of_category) VALUES
('Игровые компьютеры', 'Высокопроизводительные ПК для игр'),
('Игровые консоли', 'Приставки PlayStation, Xbox, Nintendo'),
('Периферия', 'Мыши, клавиатуры, наушники, мониторы'),
('Сетевое оборудование', 'Роутеры, коммутаторы, точки доступа'),
('Серверное оборудование', 'Серверы для локальных сетевых игр');

-- Заполнение таблицы Position
INSERT INTO Position (name_of_position, description_of_position, salary_range) VALUES
('Администратор', 'Управление клиентами и бронированием', '60000-80000 руб.'),
('Техник', 'Ремонт и обслуживание оборудования', '50000-70000 руб.'),
('Менеджер', 'Ведение документации и отчетности', '70000-90000 руб.'),
('Киберспорт-тренер', 'Обучение и тренировка игроков', '80000-120000 руб.'),
('Уборщик', 'Поддержание чистоты в залах', '40000-50000 руб.');

-- Заполнение таблицы EquipmentCondition
INSERT INTO EquipmentCondition (name_of_condition, description_of_condition) VALUES
('Исправен', 'Оборудование полностью функционально'),
('Требует ремонта', 'Частичная неработоспособность компонентов'),
('На ремонте', 'Оборудование находится в сервисном центре'),
('Неисправен', 'Оборудование полностью неработоспособно'),
('Требует замены', 'Оборудование устарело и требует замены');

-- Заполнение таблицы MovementType
INSERT INTO MovementType (name_of_type, description_of_type) VALUES
('Установка', 'Начальная установка оборудования в зоне'),
('Перемещение', 'Перемещение между игровыми зонами'),
('Ремонт', 'Отправка оборудования в сервисный центр'),
('Возврат из ремонта', 'Возврат оборудования после ремонта'),
('Списание', 'Окончательное списание оборудования'),
('Апгрейд', 'Отправка на модернизацию комплектующих');

-- Заполнение таблицы Department
INSERT INTO Department (organization_id, name_of_department) VALUES
(1, 'Зона А (VIP)'), 
(1, 'Зона Б (Обычная)'), 
(1, 'Зона В (Киберспорт)'), 
(1, 'Сервисный центр'), 
(1, 'Администрация');

-- Заполнение таблицы ComputingEquipment
INSERT INTO ComputingEquipment (category_id, name_of_equipment, model_of_equipment, year_manufactured, serial_number) VALUES
(1, 'Игровой ПК', 'CyberPowerPC GXIV', 2023, 'CP-PC-001-2023'),
(1, 'Игровой ПК', 'CyberPowerPC GXIV', 2023, 'CP-PC-002-2023'),
(1, 'Игровой ПК', 'CyberPowerPC GXIV', 2022, 'CP-PC-003-2022'),
(2, 'Игровая консоль', 'PlayStation 5', 2023, 'PS5-001-2023'),
(2, 'Игровая консоль', 'Xbox Series X', 2023, 'XBSX-001-2023'),
(2, 'Игровая консоль', 'Nintendo Switch', 2022, 'NS-001-2022'),
(3, 'Монитор', 'ASUS ROG Swift 360Hz', 2023, 'ASUS-MON-001'),
(3, 'Клавиатура', 'Razer Blackwidow V3', 2022, 'RAZ-KB-001'),
(3, 'Мышь', 'Logitech G Pro X Superlight', 2022, 'LOG-MOUSE-001'),
(4, 'Роутер', 'ASUS ROG Rapture GT-AXE16000', 2023, 'ASUS-ROUTER-001'),
(5, 'Сервер', 'Dell PowerEdge R750', 2023, 'DELL-SRV-001'),
(1, 'Игровой ПК', 'CyberPowerPC GXIV', 2023, 'CP-PC-004-2023'),
(1, 'Игровой ПК', 'CyberPowerPC GXIV', 2023, 'CP-PC-005-2023'),
(3, 'Наушники', 'SteelSeries Arctis Pro', 2022, 'SS-HEAD-001'),
(2, 'Игровая консоль', 'PlayStation 5 Digital', 2023, 'PS5D-001-2023');

-- Заполнение таблицы Component
INSERT INTO Component (equipment_id, name_of_component, model_of_component, quantity, is_removable) VALUES
(1, 'Видеокарта', 'NVIDIA GeForce RTX 4090', 1, true),
(1, 'Процессор', 'Intel Core i9-13900K', 1, true),
(1, 'Оперативная память', 'Corsair Vengeance DDR5 64GB', 1, true),
(2, 'Видеокарта', 'NVIDIA GeForce RTX 4080', 1, true),
(2, 'Процессор', 'AMD Ryzen 9 7950X', 1, true),
(3, 'Видеокарта', 'NVIDIA GeForce RTX 4070', 1, true),
(4, 'Накопитель', 'SSD 2TB', 1, true),
(5, 'Накопитель', 'SSD 1TB', 1, true),
(6, 'Накопитель', 'SSD 512GB', 1, true),
(7, 'Кабель питания', 'HDMI 2.1', 2, true),
(8, 'Ключи', 'Механические переключатели', 120, true),
(9, 'Аккумулятор', 'Li-Po', 1, true),
(10, 'Антенна', 'Wi-Fi 6E', 4, true),
(11, 'Жесткий диск', 'HDD 10TB', 4, true),
(12, 'Видеокарта', 'NVIDIA GeForce RTX 4090', 1, true);

-- Заполнение таблицы InventoryNumber
INSERT INTO InventoryNumber (equipment_id, number, date_registered, acquisition_method) VALUES
(1, 'INV-PC-001', '2023-01-15', 'Покупка'),
(2, 'INV-PC-002', '2023-01-15', 'Покупка'),
(3, 'INV-PC-003', '2022-11-20', 'Покупка'),
(4, 'INV-PS5-001', '2023-03-10', 'Покупка'),
(5, 'INV-XB-001', '2023-03-15', 'Покупка'),
(6, 'INV-NS-001', '2022-12-05', 'Покупка'),
(7, 'INV-MON-001', '2023-02-10', 'Покупка'),
(8, 'INV-KB-001', '2022-09-18', 'Покупка'),
(9, 'INV-MOUSE-001', '2022-09-18', 'Покупка'),
(10, 'INV-ROUTER-001', '2023-04-01', 'Покупка'),
(11, 'INV-SRV-001', '2023-05-12', 'Покупка'),
(12, 'INV-PC-004', '2023-06-20', 'Покупка'),
(13, 'INV-PC-005', '2023-06-20', 'Покупка'),
(14, 'INV-HEAD-001', '2022-10-15', 'Покупка'),
(15, 'INV-PS5D-001', '2023-07-01', 'Покупка');

-- Заполнение таблицы Employee
INSERT INTO Employee (department_id, position_id, full_name, contact_information) VALUES
(1, 1, 'Иванов Иван Иванович', 'ivanov@example.com, +7(900)123-45-67'),
(2, 1, 'Петров Петр Петрович', 'petrov@example.com, +7(900)234-56-78'),
(3, 4, 'Сидоров Сидор Сидорович', 'sidorov@example.com, +7(900)345-67-89'),
(4, 2, 'Козлов Козел Козлович', 'kozlov@example.com, +7(900)456-78-90'),
(5, 3, 'Волков Волк Волкович', 'volkov@example.com, +7(900)567-89-01'),
(1, 2, 'Медведев Медведь Медведевич', 'medvedev@example.com, +7(900)111-22-33'),
(2, 2, 'Орлов Орел Орлович', 'orlov@example.com, +7(900)222-33-44'),
(3, 1, 'Соколов Сокол Соколович', 'sokolov@example.com, +7(900)333-44-55'),
(4, 3, 'Лисицин Лис Лисович', 'lisitsin@example.com, +7(900)444-55-66'),
(1, 5, 'Зайцев Заяц Зайцевич', 'zaitsev@example.com, +7(900)555-66-77'),
(2, 5, 'Баранов Баран Баранович', 'baranov@example.com, +7(900)666-77-88'),
(3, 5, 'Кроликов Кролик Кроликович', 'krolikov@example.com, +7(900)777-88-99'),
(5, 1, 'Гусев Гусь Гусевич', 'gusev@example.com, +7(900)888-99-00'),
(4, 4, 'Воробьев Воробей Воробьевич', 'vorobiev@example.com, +7(900)999-00-11'),
(5, 4, 'Соколов Сокол Соколович', 'sokolov2@example.com, +7(900)000-11-22');

-- Заполнение таблицы Movement
INSERT INTO Movement (inventory_number_id, department_id, employee_id, movement_type_id, movement_date, reason) VALUES
(1, 1, 1, 1, '2023-01-16', 'Установка в VIP зоне'),
(2, 2, 2, 1, '2023-01-16', 'Установка в обычной зоне'),
(3, 3, 3, 1, '2022-11-21', 'Установка в киберспортивной зоне'),
(4, 1, 1, 1, '2023-03-11', 'Установка PlayStation 5 в VIP зоне'),
(5, 2, 2, 1, '2023-03-16', 'Установка Xbox в обычной зоне'),
(6, 3, 3, 1, '2022-12-06', 'Установка Nintendo Switch в киберспортивной зоне'),
(7, 1, 1, 1, '2023-02-11', 'Установка монитора в VIP зоне'),
(1, 4, 4, 3, '2023-05-10', 'Проблемы с видеокартой'),
(1, 1, 1, 4, '2023-05-15', 'Ремонт завершен успешно'),
(10, 4, 6, 1, '2023-04-02', 'Установка роутера в серверную'),
(11, 4, 4, 1, '2023-05-13', 'Установка игрового сервера'),
(2, 3, 7, 2, '2023-08-01', 'Перемещение для турнира'),
(8, 2, 2, 1, '2022-09-19', 'Установка клавиатуры в обычной зоне'),
(9, 3, 3, 1, '2022-09-19', 'Установка мыши в киберспортивной зоне'),
(15, 2, 2, 1, '2023-07-02', 'Установка PlayStation 5 Digital в обычной зоне');

-- Заполнение таблицы RegisterOfRepairWorks
INSERT INTO RegisterOfRepairWorks (inventory_number_id, department_id, condition_id, last_update) VALUES
(1, 4, 1, '2023-05-15'),
(2, 3, 1, '2023-08-01'),
(3, 3, 1, '2023-01-10'),
(4, 1, 1, '2023-01-10'),
(5, 2, 1, '2023-01-10'),
(6, 3, 1, '2023-01-10'),
(7, 1, 1, '2023-01-10'),
(8, 2, 1, '2023-01-10'),
(9, 3, 1, '2023-01-10'),
(10, 4, 1, '2023-01-10'),
(11, 4, 1, '2023-05-13'),
(12, 1, 1, '2023-06-21'),
(13, 2, 1, '2023-06-21'),
(14, 2, 1, '2022-10-16'),
(15, 2, 1, '2023-07-03');

--Проверка
SELECT * FROM Organization;
SELECT * FROM EquipmentCategory ;
SELECT * FROM Position;
SELECT * FROM EquipmentCondition;
SELECT * FROM MovementType;
SELECT * FROM Department;
SELECT * FROM ComputingEquipment;
SELECT * FROM Component;
SELECT * FROM InventoryNumber;
SELECT * FROM Employee ;
SELECT * FROM Movement;
SELECT * FROM RegisterOfRepairWorks;

--откат
-- Сначала очищаем таблицы с внешними ключами, которые ссылаются на другие таблицы
TRUNCATE TABLE Movement, RegisterOfRepairWorks, Component, InventoryNumber, 
             Employee, ComputingEquipment, Department, EquipmentCondition, 
             MovementType, Position, EquipmentCategory, Organization
CASCADE;


-- Сбрасываем счетчики SERIAL для всех таблиц
SELECT setval('organization_organization_id_seq', 1, false);
SELECT setval('department_department_id_seq', 1, false);
SELECT setval('position_position_id_seq', 1, false);
SELECT setval('employee_employee_id_seq', 1, false);
SELECT setval('equipmentcategory_category_id_seq', 1, false);
SELECT setval('computingequipment_equipment_id_seq', 1, false);
SELECT setval('component_component_id_seq', 1, false);
SELECT setval('inventorynumber_inventory_number_id_seq', 1, false);
SELECT setval('movementtype_movement_type_id_seq', 1, false);
SELECT setval('movement_movement_id_seq', 1, false);
SELECT setval('equipmentcondition_condition_id_seq', 1, false);
SELECT setval('registerofrepairworks_repair_work_id_seq', 1, false);

--4.1. Однотабличный запрос с простым условием
-- Найти всех сотрудников, которые работают администраторами
SELECT employee_id, full_name, contact_information
FROM Employee
WHERE position_id = (SELECT position_id FROM Position WHERE name_of_position = 'Администратор');

--4.2. Однотабличный запрос с сложным условием
-- b1. and, and, not
SELECT equipment_id, name_of_equipment, model_of_equipment, year_manufactured
FROM ComputingEquipment
WHERE year_manufactured > 2020 
  AND category_id IN (SELECT category_id FROM EquipmentCategory WHERE name_of_category = 'Игровые компьютеры')
  AND serial_number NOT LIKE '%Digital%';

-- b2. and, or
SELECT inventory_number_id, number, date_registered, acquisition_method
FROM InventoryNumber
WHERE (acquisition_method = 'Покупка' AND date_registered > '2023-01-01')
   OR (date_registered > '2022-12-01' AND date_registered < '2023-01-01');

-- b3. and, and
SELECT movement_id, movement_date, reason
FROM Movement
WHERE movement_date BETWEEN '2023-01-01' AND '2023-06-30'
  AND movement_type_id = 3;
--многотабличный запрос с вычисляемым полем и простым условием  
--с
SELECT 
    ce.equipment_id,
    ce.name_of_equipment,
    ce.model_of_equipment,
    ec.name_of_category,
    EXTRACT(YEAR FROM CURRENT_DATE) - ce.year_manufactured AS age_years
FROM ComputingEquipment ce
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
WHERE EXTRACT(YEAR FROM CURRENT_DATE) - ce.year_manufactured <= 4; 

--.многотабличный запрос, сложное условие: 
-- d1. or, and, not 
SELECT 
    m.movement_id,
    m.movement_date,
    mt.name_of_type AS movement_type,
    e.full_name AS responsible_employee
FROM Movement m
JOIN MovementType mt ON m.movement_type_id = mt.movement_type_id
JOIN Employee e ON m.employee_id = e.employee_id
WHERE (mt.name_of_type = 'Ремонт' OR mt.name_of_type = 'Апгрейд')
  AND m.movement_date > '2023-01-01'
  AND e.position_id != (SELECT position_id FROM Position WHERE name_of_position = 'Уборщик');

--d2. and, and 
SELECT 
    ce.equipment_id,
    ce.name_of_equipment,
    ce.model_of_equipment,
    inv.number AS inventory_number,
    d.name_of_department
FROM ComputingEquipment ce
JOIN InventoryNumber inv ON ce.equipment_id = inv.equipment_id
JOIN Movement m ON inv.inventory_number_id = m.inventory_number_id
JOIN Department d ON m.department_id = d.department_id
WHERE m.movement_date = (SELECT MAX(movement_date) FROM Movement WHERE inventory_number_id = inv.inventory_number_id)
  AND ce.year_manufactured = 2023;

--d3. and, оператор BETWEEN 
SELECT 
    m.movement_id,
    inv.number AS inventory_number,
    ce.name_of_equipment,
    mt.name_of_type,
    m.movement_date,
    d.name_of_department
FROM Movement m
JOIN InventoryNumber inv ON m.inventory_number_id = inv.inventory_number_id
JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
JOIN MovementType mt ON m.movement_type_id = mt.movement_type_id
JOIN Department d ON m.department_id = d.department_id
WHERE m.movement_date BETWEEN '2023-01-01' AND '2023-03-31'
  AND m.department_id = 1;

--d4. and, оператор NOT BETWEEN 
SELECT 
    ce.equipment_id,
    ce.name_of_equipment,
    ce.serial_number,
    ec.name_of_category
FROM ComputingEquipment ce
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
WHERE ce.year_manufactured NOT BETWEEN 2020 AND 2022
  AND ec.name_of_category = 'Игровые консоли';

--d5. оператор IN 
SELECT 
    e.employee_id,
    e.full_name,
    p.name_of_position,
    d.name_of_department
FROM Employee e
JOIN Position p ON e.position_id = p.position_id
JOIN Department d ON e.department_id = d.department_id
WHERE p.name_of_position IN ('Администратор', 'Техник', 'Киберспорт-тренер');

--d6. оператор NOT IN 
SELECT 
    ce.equipment_id,
    ce.name_of_equipment,
    ce.model_of_equipment,
    ec.name_of_category
FROM ComputingEquipment ce
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
WHERE ec.name_of_category NOT IN ('Сетевое оборудование', 'Серверное оборудование');

--с оконными функциями 
--1
SELECT 
    e.employee_id,
    e.full_name AS employee_name,
    d.name_of_department,
    COUNT(m.movement_id) AS individual_movements,
    SUM(COUNT(m.movement_id)) OVER (PARTITION BY d.department_id) AS total_department_movements,
    ROUND(COUNT(m.movement_id) * 100.0 / SUM(COUNT(m.movement_id)) OVER (PARTITION BY d.department_id), 2) AS contribution_percent
FROM Movement m
JOIN Employee e ON m.employee_id = e.employee_id
JOIN Department d ON m.department_id = d.department_id
GROUP BY e.employee_id, e.full_name, d.department_id, d.name_of_department
ORDER BY d.name_of_department, individual_movements DESC;

--2
SELECT 
    m.movement_id,
    inv.number AS inventory_number,
    ce.name_of_equipment,
    d.name_of_department,
    m.movement_date,
    mt.name_of_type AS movement_type,
    ROW_NUMBER() OVER (PARTITION BY m.department_id ORDER BY m.movement_date DESC) AS rn
FROM Movement m
JOIN InventoryNumber inv ON m.inventory_number_id = inv.inventory_number_id
JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
JOIN Department d ON m.department_id = d.department_id
JOIN MovementType mt ON m.movement_type_id = mt.movement_type_id
ORDER BY d.name_of_department, m.movement_date DESC;

--3
SELECT 
    d.department_id,
    d.name_of_department,
    COUNT(m.movement_id) AS total_movements,
    NTILE(4) OVER (ORDER BY COUNT(m.movement_id) DESC) AS quartile
FROM Movement m
JOIN Department d ON m.department_id = d.department_id
GROUP BY d.department_id, d.name_of_department
ORDER BY total_movements DESC;

--с вычисляемым полем
--1
SELECT 
    rrw.repair_work_id,
    inv.number AS inventory_number,
    ce.name_of_equipment,
    ec.name_of_condition,
    CURRENT_DATE - rrw.last_update AS days_in_current_state,
    CASE 
        WHEN CURRENT_DATE - rrw.last_update > 30 THEN 'Требует внимания'
        ELSE 'В норме'
    END AS attention_status
FROM RegisterOfRepairWorks rrw
JOIN InventoryNumber inv ON rrw.inventory_number_id = inv.inventory_number_id
JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
JOIN EquipmentCondition ec ON rrw.condition_id = ec.condition_id;


--2
SELECT 
    ec.name_of_category AS equipment_category,
    c.name_of_component AS component_type,
    SUM(CASE WHEN c.is_removable = true THEN c.quantity ELSE 0 END) AS repairable_quantity,
    SUM(c.quantity) AS total_quantity,
    ROUND(SUM(CASE WHEN c.is_removable = true THEN c.quantity ELSE 0 END) * 100.0 / SUM(c.quantity), 2) AS repair_percentage
FROM Component c
JOIN ComputingEquipment ce ON c.equipment_id = ce.equipment_id
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
GROUP BY ec.name_of_category, c.name_of_component
HAVING SUM(c.quantity) > 0
ORDER BY repair_percentage DESC;

--с агрегатными функциями
--группировка данных и простая сортировка 
SELECT 
    ec.name_of_category,
    SUM(c.quantity) AS total_components,
    COUNT(DISTINCT ce.equipment_id) AS equipment_count,
    ROUND(SUM(c.quantity) * 1.0 / COUNT(DISTINCT ce.equipment_id), 2) AS avg_components_per_unit
FROM Component c
JOIN ComputingEquipment ce ON c.equipment_id = ce.equipment_id
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
GROUP BY ec.category_id, ec.name_of_category
ORDER BY total_components DESC;

-- группировка данных c условием и многоуровневая сортировка (не менее 3х полей)
SELECT 
    e.full_name AS employee_name,
    ec.name_of_category AS equipment_category,
    COUNT(m.movement_id) AS movement_count,
    MIN(m.movement_date) AS first_movement,
    MAX(m.movement_date) AS last_movement
FROM Movement m
JOIN Employee e ON m.employee_id = e.employee_id
JOIN InventoryNumber inv ON m.inventory_number_id = inv.inventory_number_id
JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
GROUP BY e.employee_id, e.full_name, ec.category_id, ec.name_of_category
HAVING COUNT(m.movement_id) >= 2
ORDER BY movement_count DESC, e.full_name ASC, ec.name_of_category ASC;

--с подзапросом
--запрос с использованием подзапроса,возвращающих единичное значение; 
SELECT 
    c.component_id,
    c.name_of_component,
    c.model_of_component,
    c.quantity,
    ce.name_of_equipment
FROM Component c
JOIN ComputingEquipment ce ON c.equipment_id = ce.equipment_id
WHERE c.quantity > (SELECT AVG(quantity) FROM Component);

-- запрос с использованием операций IN и NOT IN; 
SELECT 
    e.employee_id,
    e.full_name,
    p.name_of_position,
    d.name_of_department
FROM Employee e
JOIN Position p ON e.position_id = p.position_id
JOIN Department d ON e.department_id = d.department_id
WHERE e.department_id IN (
    SELECT department_id FROM Department 
    WHERE name_of_department LIKE '%он%'
)
AND e.position_id NOT IN (
    SELECT position_id FROM Position 
    WHERE name_of_position = 'Уборщик'
);

--– запрос с использованием ключевых слов ANY и ALL; 
SELECT 
    ce.equipment_id,
    ce.name_of_equipment,
    ce.model_of_equipment,
    ce.year_manufactured,
    ce.serial_number
FROM ComputingEquipment ce
WHERE ce.year_manufactured > ALL (
    SELECT year_manufactured FROM ComputingEquipment 
    WHERE category_id = (SELECT category_id FROM EquipmentCategory WHERE name_of_category = 'Игровые консоли')
)
OR ce.equipment_id = ANY (
    SELECT equipment_id FROM Component 
    WHERE name_of_component = 'Видеокарта' AND model_of_component LIKE '%RTX 4090%'
);

-- запрос с использованием операций EXISTS и NOT EXISTS. 
SELECT 
    d.department_id,
    d.name_of_department,
    o.name_of_organization
FROM Department d
JOIN Organization o ON d.organization_id = o.organization_id
WHERE EXISTS (
    SELECT 1 FROM Movement m 
    WHERE m.department_id = d.department_id 
    AND m.movement_date > '2023-06-01'
)
AND NOT EXISTS (
    SELECT 1 FROM Employee e 
    WHERE e.department_id = d.department_id 
    AND e.position_id = (SELECT position_id FROM Position WHERE name_of_position = 'Киберспорт-тренер')
);

--запрос на основе материализованного представления 
CREATE MATERIALIZED VIEW mv_equipment_summary AS
SELECT 
    d.department_id,
    d.name_of_department,
    ec.category_id,
    ec.name_of_category,
    COUNT(*) AS total_equipment,
    COUNT(CASE WHEN ecn.name_of_condition = 'Исправен' THEN 1 END) AS functional_equipment,
    EXTRACT(YEAR FROM CURRENT_DATE) - AVG(ce.year_manufactured) AS avg_age_years,
    MAX(rrw.last_update) AS last_service_date
FROM RegisterOfRepairWorks rrw
JOIN Department d ON rrw.department_id = d.department_id
JOIN InventoryNumber inv ON rrw.inventory_number_id = inv.inventory_number_id
JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
JOIN EquipmentCondition ecn ON rrw.condition_id = ecn.condition_id
GROUP BY d.department_id, d.name_of_department, ec.category_id, ec.name_of_category;

--сам запрос к материализованному представлению
SELECT 
    name_of_department AS department,
    name_of_category AS equipment_category,
    total_equipment,
    functional_equipment,
    ROUND(functional_equipment * 100.0 / total_equipment, 2) AS functional_percentage,
    avg_age_years,
    last_service_date
FROM mv_equipment_summary
WHERE department_id = 1
ORDER BY functional_percentage DESC;


-- 6
-- материализованное представление
-- Создание второго материализованного представления
CREATE MATERIALIZED VIEW mv_equipment_status AS
SELECT 
    ce.equipment_id,
    ce.name_of_equipment,
    ce.model_of_equipment,
    ec.name_of_category,
    ce.year_manufactured,
    inv.number AS inventory_number,
    inv.date_registered,
    d.name_of_department AS current_location,
    ecn.name_of_condition AS current_condition,
    rrw.last_update AS condition_updated
FROM ComputingEquipment ce
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
JOIN InventoryNumber inv ON ce.equipment_id = inv.equipment_id
JOIN RegisterOfRepairWorks rrw ON inv.inventory_number_id = rrw.inventory_number_id
JOIN EquipmentCondition ecn ON rrw.condition_id = ecn.condition_id
JOIN Department d ON rrw.department_id = d.department_id;

-- Обновление материализованного представления перед запросом
REFRESH MATERIALIZED VIEW mv_equipment_status;

-- Запрос к материализованному представлению
SELECT 
    equipment_id,
    name_of_equipment,
    model_of_equipment,
    name_of_category,
    inventory_number,
    current_location,
    current_condition,
    EXTRACT(YEAR FROM CURRENT_DATE) - year_manufactured AS age_years,
    condition_updated,
    CASE 
        WHEN CURRENT_DATE - condition_updated > 90 THEN 'Требует обслуживания'
        WHEN CURRENT_DATE - condition_updated > 60 THEN 'Плановое обслуживание скоро'
        ELSE 'В норме'
    END AS maintenance_status
FROM mv_equipment_status
WHERE current_condition = 'Исправен'
  AND current_location = 'Зона А (VIP)'
ORDER BY condition_updated ASC;

-- Объявление и использование курсора
DO $$
DECLARE
    equipment_cursor CURSOR FOR 
        SELECT 
            inv.number AS inventory_number,
            d.name_of_department,
            ec.name_of_condition,
            rrw.last_update
        FROM RegisterOfRepairWorks rrw
        JOIN InventoryNumber inv ON rrw.inventory_number_id = inv.inventory_number_id
        JOIN Department d ON rrw.department_id = d.department_id
        JOIN EquipmentCondition ec ON rrw.condition_id = ec.condition_id
        ORDER BY d.name_of_department, ec.name_of_condition;
    
    equipment_record RECORD;
BEGIN
    OPEN equipment_cursor;
    
    LOOP
        FETCH equipment_cursor INTO equipment_record;
        EXIT WHEN NOT FOUND;
        
        RAISE NOTICE 'Инвентарный номер: %, Подразделение: %, Состояние: %, Последнее обновление: %', 
            equipment_record.inventory_number,
            equipment_record.name_of_department,
            equipment_record.name_of_condition,
            equipment_record.last_update;
    END LOOP;
    
    CLOSE equipment_cursor;
END $$;

-- Объявление и использование второго курсора
DO $$
DECLARE
    movement_cursor CURSOR FOR 
        SELECT 
            m.movement_id,
            inv.number AS inventory_number,
            ce.name_of_equipment,
            d.name_of_department,
            mt.name_of_type AS movement_type,
            m.movement_date,
            m.reason
        FROM Movement m
        JOIN InventoryNumber inv ON m.inventory_number_id = inv.inventory_number_id
        JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
        JOIN Department d ON m.department_id = d.department_id
        JOIN MovementType mt ON m.movement_type_id = mt.movement_type_id
        ORDER BY m.movement_date DESC;
    
    movement_record RECORD;
BEGIN
    OPEN movement_cursor;
    RAISE NOTICE 'Последние операции с оборудованием:';
    RAISE NOTICE '------------------------------------------------------------';
    LOOP
        FETCH movement_cursor INTO movement_record;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'ID: %, Инв. №: %, Оборудование: %, Зона: %, Тип: %, Дата: %, Причина: %', 
            movement_record.movement_id,
            movement_record.inventory_number,
            movement_record.name_of_equipment,
            movement_record.name_of_department,
            movement_record.movement_type,
            movement_record.movement_date,
            movement_record.reason;
    END LOOP;
    -- Добавляем проверку, если данных нет
    IF NOT FOUND THEN
        RAISE NOTICE 'Нет данных для отображения';
    END IF;
    CLOSE movement_cursor;
END $$;


-- создание функции
CREATE OR REPLACE FUNCTION get_functional_equipment_count(
    dept_id INTEGER,
    cat_id INTEGER
)
RETURNS INTEGER AS $$
DECLARE
    equipment_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO equipment_count
    FROM RegisterOfRepairWorks rrw
    JOIN InventoryNumber inv ON rrw.inventory_number_id = inv.inventory_number_id
    JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
    JOIN EquipmentCondition ec ON rrw.condition_id = ec.condition_id
    WHERE rrw.department_id = dept_id
      AND ce.category_id = cat_id
      AND ec.name_of_condition = 'Исправен';
      
    RETURN equipment_count;
END;
$$ LANGUAGE plpgsql;


---- Проверка функции для получения количества исправных игровых ПК в VIP-зоне
SELECT 
    get_functional_equipment_count(1, 1) AS functional_pcs_in_vip_zone,
    'Зона А (VIP)' AS department_name,
    'Игровые компьютеры' AS equipment_category;

-- создание процедуры
CREATE OR REPLACE PROCEDURE register_equipment_movement(
    p_inventory_number_id INT,
    p_department_id INT,
    p_employee_id INT,
    p_movement_type_id INT,
    p_reason TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_current_department_id INT;
    v_equipment_name TEXT;
BEGIN
    -- Проверка существования инвентарного номера
    SELECT ce.name_of_equipment INTO v_equipment_name
    FROM InventoryNumber inv
    JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
    WHERE inv.inventory_number_id = p_inventory_number_id;
    IF v_equipment_name IS NULL THEN
        RAISE EXCEPTION 'Инвентарный номер % не найден в базе данных', p_inventory_number_id;
    END IF;
    -- Получение текущего местоположения оборудования
    SELECT department_id INTO v_current_department_id
    FROM Movement
    WHERE inventory_number_id = p_inventory_number_id
    ORDER BY movement_date DESC
    LIMIT 1;
    -- Проверка на попытку переместить оборудование в то же подразделение
    IF v_current_department_id = p_department_id AND p_movement_type_id NOT IN (3, 4) THEN
        RAISE EXCEPTION 'Оборудование "%" уже находится в указанном подразделении', v_equipment_name;
    END IF;
    -- Регистрация перемещения
    INSERT INTO Movement (
        inventory_number_id,
        department_id,
        employee_id,
        movement_type_id,
        movement_date,
        reason
    ) VALUES (
        p_inventory_number_id,
        p_department_id,
        p_employee_id,
        p_movement_type_id,
        CURRENT_DATE,
        p_reason
    );
    -- Автоматическое обновление состояния оборудования при ремонте или возврате
    IF p_movement_type_id = 3 THEN -- Ремонт
        UPDATE RegisterOfRepairWorks
        SET 
            condition_id = (SELECT condition_id FROM EquipmentCondition WHERE name_of_condition = 'На ремонте'),
            last_update = CURRENT_DATE,
            department_id = p_department_id
        WHERE inventory_number_id = p_inventory_number_id;   
    ELSIF p_movement_type_id = 4 THEN -- Возврат из ремонта
        UPDATE RegisterOfRepairWorks
        SET 
            condition_id = (SELECT condition_id FROM EquipmentCondition WHERE name_of_condition = 'Исправен'),
            last_update = CURRENT_DATE,
            department_id = p_department_id
        WHERE inventory_number_id = p_inventory_number_id;
    END IF; 
    RAISE NOTICE 'Операция успешно выполнена: оборудование "%" перемещено в подразделение %', 
        v_equipment_name, 
        (SELECT name_of_department FROM Department WHERE department_id = p_department_id);
END;
$$;


-- Вызов процедуры для перемещения наушников на ремонт
CALL register_equipment_movement(
    p_inventory_number_id := 14,  -- Наушники SteelSeries Arctis Pro
    p_department_id := 4,         -- Сервисный центр
    p_employee_id := 4,           -- Козлов Козел Козлович (техник)
    p_movement_type_id := 3,      -- Тип перемещения: Ремонт
    p_reason := 'Проблемы с микрофоном'
);


---- Создание функции для триггера
CREATE OR REPLACE FUNCTION update_repair_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_update := CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER trg_update_repair_date
BEFORE UPDATE OF condition_id, department_id ON RegisterOfRepairWorks
FOR EACH ROW
EXECUTE FUNCTION update_repair_date();


-- Создание 2 функции для триггера
CREATE OR REPLACE FUNCTION check_component_quantity()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity <= 0 THEN
        RAISE EXCEPTION 'Количество компонентов не может быть меньше или равно нулю. Указано: %', NEW.quantity;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание 2 триггера
CREATE TRIGGER trg_check_component_quantity
BEFORE INSERT OR UPDATE OF quantity ON Component
FOR EACH ROW
EXECUTE FUNCTION check_component_quantity();


-- ========================
-- СЕКЦИЯ 1: ПРОСМОТР СТРУКТУРЫ И ДАННЫХ
-- ========================

-- 1.1 Просмотр основных таблиц и их содержимого
SELECT '=== Просмотр структуры и данных ===' AS section;

-- Организации и подразделения
SELECT 'Организации:' AS table_name;
SELECT * FROM Organization;

SELECT 'Подразделения:' AS table_name;
SELECT * FROM Department;

-- Оборудование и категории
SELECT 'Категории оборудования:' AS table_name;
SELECT * FROM EquipmentCategory;

SELECT 'Оборудование:' AS table_name;
SELECT equipment_id, name_of_equipment, model_of_equipment, year_manufactured, serial_number 
FROM ComputingEquipment;

-- Сотрудники и должности
SELECT 'Должности:' AS table_name;
SELECT * FROM Position;

SELECT 'Сотрудники:' AS table_name;
SELECT employee_id, full_name, (SELECT name_of_position FROM Position WHERE position_id = e.position_id) AS position,
       (SELECT name_of_department FROM Department WHERE department_id = e.department_id) AS department
FROM Employee e;

-- ========================
-- СЕКЦИЯ 2: ДЕМОНСТРАЦИЯ ИНДЕКСОВ
-- ========================

SELECT '=== Демонстрация работы индексов ===' AS section;

-- Показать использование индексов при выполнении запросов
EXPLAIN ANALYZE
SELECT ce.name_of_equipment, ec.name_of_category, ce.year_manufactured
FROM ComputingEquipment ce
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
WHERE ce.year_manufactured > 2021;

EXPLAIN ANALYZE
SELECT m.movement_date, mt.name_of_type, d.name_of_department, ce.name_of_equipment
FROM Movement m
JOIN MovementType mt ON m.movement_type_id = mt.movement_type_id
JOIN Department d ON m.department_id = d.department_id
JOIN InventoryNumber inv ON m.inventory_number_id = inv.inventory_number_id
JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
WHERE m.movement_date BETWEEN '2023-01-01' AND '2023-12-31';

-- ========================
-- СЕКЦИЯ 3: ДЕМОНСТРАЦИЯ МАТЕРИАЛИЗОВАННЫХ ПРЕДСТАВЛЕНИЙ
-- ========================

SELECT '=== Демонстрация материализованных представлений ===' AS section;

-- Обновление и просмотр первого материализованного представления
REFRESH MATERIALIZED VIEW mv_equipment_summary;
SELECT 'Статистика оборудования по подразделениям и категориям:' AS description;
SELECT * FROM mv_equipment_summary ORDER BY department_id, category_id;

-- Обновление и просмотр второго материализованного представления
REFRESH MATERIALIZED VIEW mv_equipment_status;
SELECT 'Текущее состояние оборудования:' AS description;
SELECT equipment_id, name_of_equipment, model_of_equipment, current_location, current_condition, condition_updated
FROM mv_equipment_status
ORDER BY current_location, current_condition;

-- ========================
-- СЕКЦИЯ 4: ДЕМОНСТРАЦИЯ ФУНКЦИЙ
-- ========================

SELECT '=== Демонстрация функций ===' AS section;

-- Проверка функции подсчета исправного оборудования
SELECT 'Количество исправных игровых ПК в VIP-зоне (department_id=1, category_id=1):' AS description;
SELECT get_functional_equipment_count(1, 1) AS functional_count;

-- Демонстрация функции расчета стоимости ремонта
SELECT 'Расчет стоимости ремонта для оборудования:' AS description;
SELECT 
    ce.equipment_id,
    ce.name_of_equipment,
    ce.model_of_equipment,
    calculate_repair_cost(ce.equipment_id) AS estimated_repair_cost
FROM ComputingEquipment ce
WHERE ce.equipment_id IN (1, 4, 7, 10)
ORDER BY equipment_id;

-- ========================
-- СЕКЦИЯ 5: ДЕМОНСТРАЦИЯ ПРОЦЕДУР
-- ========================

SELECT '=== Демонстрация процедур ===' AS section;

-- Демонстрация работы процедуры регистрации перемещения
SELECT 'Регистрация перемещения оборудования на ремонт:' AS description;
CALL register_equipment_movement(
    p_inventory_number_id := 14,  -- Наушники SteelSeries Arctis Pro
    p_department_id := 4,         -- Сервисный центр
    p_employee_id := 4,           -- Козлов Козел Козлович (техник)
    p_movement_type_id := 3,      -- Тип перемещения: Ремонт
    p_reason := 'Проблемы с микрофоном'
);

-- Проверка результата работы процедуры
SELECT 'Проверка последних перемещений:' AS description;
SELECT 
    m.movement_id,
    inv.number AS inventory_number,
    ce.name_of_equipment,
    mt.name_of_type AS movement_type,
    m.movement_date,
    m.reason
FROM Movement m
JOIN InventoryNumber inv ON m.inventory_number_id = inv.inventory_number_id
JOIN ComputingEquipment ce ON inv.equipment_id = ce.equipment_id
JOIN MovementType mt ON m.movement_type_id = mt.movement_type_id
WHERE m.inventory_number_id = 14
ORDER BY m.movement_date DESC
LIMIT 3;

-- ========================
-- СЕКЦИЯ 6: ДЕМОНСТРАЦИЯ ТРИГГЕРОВ
-- ========================

SELECT '=== Демонстрация триггеров ===' AS section;

-- 6.1 Демонстрация триггера проверки количества компонентов
SELECT 'Попытка вставить компонент с некорректным количеством:' AS description;
DO $$
BEGIN
    BEGIN
        INSERT INTO Component (equipment_id, name_of_component, model_of_component, quantity, is_removable)
        VALUES (1, 'Тестовый компонент', 'TEST-001', -5, true);
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Триггер успешно сработал: %', SQLERRM;
    END;
END $$;

-- 6.2 Демонстрация триггера обновления даты
SELECT 'Обновление состояния оборудования и проверка триггера:' AS description;
UPDATE RegisterOfRepairWorks 
SET condition_id = (SELECT condition_id FROM EquipmentCondition WHERE name_of_condition = 'Требует ремонта')
WHERE inventory_number_id = 1;

SELECT 'Проверка обновленной даты:' AS description;
SELECT 
    inv.number AS inventory_number,
    ec.name_of_condition AS current_condition,
    rrw.last_update
FROM RegisterOfRepairWorks rrw
JOIN InventoryNumber inv ON rrw.inventory_number_id = inv.inventory_number_id
JOIN EquipmentCondition ec ON rrw.condition_id = ec.condition_id
WHERE rrw.inventory_number_id = 1;

-- ========================
-- СЕКЦИЯ 7: АНАЛИТИЧЕСКИЕ ЗАПРОСЫ
-- ========================

SELECT '=== Аналитические запросы ===' AS section;

-- 7.1 Распределение оборудования по возрасту
SELECT 'Средний возраст оборудования по категориям:' AS description;
SELECT 
    ec.name_of_category,
    COUNT(ce.equipment_id) AS equipment_count,
    AVG(EXTRACT(YEAR FROM CURRENT_DATE) - ce.year_manufactured) AS avg_age_years,
    MIN(ce.year_manufactured) AS oldest_year,
    MAX(ce.year_manufactured) AS newest_year
FROM ComputingEquipment ce
JOIN EquipmentCategory ec ON ce.category_id = ec.category_id
GROUP BY ec.category_id, ec.name_of_category
ORDER BY avg_age_years DESC;

-- 7.2 Анализ активности сотрудников
SELECT 'Активность сотрудников по перемещениям оборудования:' AS description;
SELECT 
    e.full_name AS employee_name,
    d.name_of_department,
    p.name_of_position,
    COUNT(m.movement_id) AS total_movements,
    COUNT(CASE WHEN m.movement_type_id = 3 THEN 1 END) AS repair_count,
    COUNT(CASE WHEN m.movement_type_id = 1 THEN 1 END) AS installation_count
FROM Employee e
JOIN Movement m ON e.employee_id = m.employee_id
JOIN Department d ON e.department_id = d.department_id
JOIN Position p ON e.position_id = p.position_id
GROUP BY e.employee_id, e.full_name, d.name_of_department, p.name_of_position
ORDER BY total_movements DESC;

-- 7.3 Состояние оборудования по зонам
SELECT 'Состояние оборудования по игровым зонам:' AS description;
SELECT 
    d.name_of_department,
    ec.name_of_condition,
    COUNT(rrw.repair_work_id) AS equipment_count,
    ROUND(COUNT(rrw.repair_work_id) * 100.0 / SUM(COUNT(rrw.repair_work_id)) OVER (PARTITION BY d.department_id), 2) AS percentage
FROM RegisterOfRepairWorks rrw
JOIN Department d ON rrw.department_id = d.department_id
JOIN EquipmentCondition ec ON rrw.condition_id = ec.condition_id
GROUP BY d.department_id, d.name_of_department, ec.condition_id, ec.name_of_condition
ORDER BY d.name_of_department, equipment_count DESC;

-- ========================
-- СЕКЦИЯ 8: ДЕМОНСТРАЦИЯ КУРСОРОВ
-- ========================

SELECT '=== Демонстрация курсоров ===' AS section;

-- Выполнение первого курсора для отслеживания состояния оборудования
DO $$
DECLARE
    equipment_cursor CURSOR FOR 
        SELECT 
            inv.number AS inventory_number,
            d.name_of_department,
            ec.name_of_condition,
            rrw.last_update
        FROM RegisterOfRepairWorks rrw
        JOIN InventoryNumber inv ON rrw.inventory_number_id = inv.inventory_number_id
        JOIN Department d ON rrw.department_id = d.department_id
        JOIN EquipmentCondition ec ON rrw.condition_id = ec.condition_id
        ORDER BY d.name_of_department, ec.name_of_condition;
    
    equipment_record RECORD;
BEGIN
    OPEN equipment_cursor;
    
    RAISE NOTICE '=== СОСТОЯНИЕ ОБОРУДОВАНИЯ ПО ПОДРАЗДЕЛЕНИЯМ ===';
    RAISE NOTICE 'Инв. номер | Подразделение | Состояние | Последнее обновление';
    RAISE NOTICE '--------------------------------------------------------';
    
    LOOP
        FETCH equipment_cursor INTO equipment_record;
        EXIT WHEN NOT FOUND;
        
        RAISE NOTICE '% | % | % | %', 
            equipment_record.inventory_number,
            equipment_record.name_of_department,
            equipment_record.name_of_condition,
            equipment_record.last_update;
    END LOOP;
    
    CLOSE equipment_cursor;
END $$;

-- ========================
-- СЕКЦИЯ 9: СВОДНАЯ ИНФОРМАЦИЯ
-- ========================

SELECT '=== Сводная информация о базе данных ===' AS section;

-- Количество записей в основных таблицах
SELECT 
    'Organization' AS table_name, COUNT(*) AS record_count FROM Organization
UNION ALL
SELECT 'Department', COUNT(*) FROM Department
UNION ALL
SELECT 'Position', COUNT(*) FROM Position
UNION ALL
SELECT 'Employee', COUNT(*) FROM Employee
UNION ALL
SELECT 'EquipmentCategory', COUNT(*) FROM EquipmentCategory
UNION ALL
SELECT 'ComputingEquipment', COUNT(*) FROM ComputingEquipment
UNION ALL
SELECT 'Component', COUNT(*) FROM Component
UNION ALL
SELECT 'InventoryNumber', COUNT(*) FROM InventoryNumber
UNION ALL
SELECT 'MovementType', COUNT(*) FROM MovementType
UNION ALL
SELECT 'Movement', COUNT(*) FROM Movement
UNION ALL
SELECT 'EquipmentCondition', COUNT(*) FROM EquipmentCondition
UNION ALL
SELECT 'RegisterOfRepairWorks', COUNT(*) FROM RegisterOfRepairWorks
ORDER BY table_name;

-- Информация об объектах базы данных
SELECT '=== Информация о созданных объектах ===' AS section;

SELECT 
    'Триггеры' AS object_type, 
    COUNT(*) AS count 
FROM pg_trigger 
WHERE tgname LIKE 'trg_%'
UNION ALL
SELECT 
    'Функции', 
    COUNT(*) 
FROM pg_proc 
WHERE proname LIKE 'get_%' OR proname LIKE 'calculate_%' OR proname LIKE 'check_%'
UNION ALL
SELECT 
    'Процедуры', 
    COUNT(*) 
FROM pg_proc 
WHERE proname LIKE 'register_%'
UNION ALL
SELECT 
    'Материализованные представления', 
    COUNT(*) 
FROM pg_matviews 
WHERE matviewname LIKE 'mv_%'
UNION ALL
SELECT 
    'Индексы', 
    COUNT(*) 
FROM pg_indexes 
WHERE tablename IN ('computingequipment', 'movement', 'employee', 'component', 'registerofrepairworks');

SELECT 'Демонстрация успешно завершена!' AS result;