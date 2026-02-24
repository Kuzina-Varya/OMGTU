DROP DATABASE IF EXISTS gshipping_db;

--Создание бд
CREATE DATABASE shipping_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TEMPLATE = template0
    CONNECTION LIMIT = -1;


-- Таблица Маршрут
CREATE TABLE Route (
    route_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    distance NUMERIC(10, 2) NOT NULL,
    base_salary NUMERIC(10, 2) NOT NULL,
    CONSTRAINT chk_route_distance CHECK (distance > 0),
    CONSTRAINT chk_route_salary CHECK (base_salary >= 0)
);

-- Таблица Стаж
CREATE TABLE ExperienceLevel (
    experience_level_id SERIAL PRIMARY KEY,
    percentage_rate NUMERIC(5, 2) NOT NULL,
    description VARCHAR(255),
    CONSTRAINT chk_percentage_rate CHECK (percentage_rate >= 0 AND percentage_rate <= 100)
);

-- Таблица Водитель
CREATE TABLE Driver (
    driver_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    experience_level_id INTEGER NOT NULL,
    CONSTRAINT fk_driver_experience_level 
        FOREIGN KEY (experience_level_id) 
        REFERENCES ExperienceLevel(experience_level_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Таблица Рейс\Перевозка
CREATE TABLE Shipment (
    shipment_id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL,
    departure_date TIMESTAMP NOT NULL,
    arrival_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_shipment_route 
        FOREIGN KEY (route_id) 
        REFERENCES Route(route_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_dates CHECK (arrival_date > departure_date)
);

-- Таблица Экипаж
CREATE TABLE CrewAssignment (
    shipment_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    bonus NUMERIC(10, 2),
    PRIMARY KEY (shipment_id, driver_id),
    CONSTRAINT fk_crew_assignment_shipment 
        FOREIGN KEY (shipment_id) 
        REFERENCES Shipment(shipment_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_crew_assignment_driver 
        FOREIGN KEY (driver_id) 
        REFERENCES Driver(driver_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_bonus CHECK (bonus >= 0)
);


-- Удаление всех таблиц с автоматическим удалением зависимостей
DROP TABLE IF EXISTS CrewAssignment CASCADE;
DROP TABLE IF EXISTS Driver CASCADE;
DROP TABLE IF EXISTS Shipment CASCADE;
DROP TABLE IF EXISTS ExperienceLevel CASCADE;
DROP TABLE IF EXISTS Route CASCADE;




-- Вставка тестовых данных

INSERT INTO Route (name, distance, base_salary) VALUES
('Москва - Санкт-Петербург', 705.50, 15000.00),
('Москва - Казань', 820.00, 17000.00),
('Санкт-Петербург - Казань', 1550.00, 28000.00),
('Москва - Екатеринбург', 1667.00, 30000.00),
('Новосибирск - Омск', 655.00, 14000.00),
('Казань - Уфа', 530.00, 12000.00);

INSERT INTO ExperienceLevel (percentage_rate, description) VALUES
(0.00, 'Начинающий водитель (без опыта)'),
(5.00, 'Младший водитель (1-2 года)'),
(10.00, 'Опытный водитель (3-5 лет)'),
(15.00, 'Старший водитель (5-10 лет)'),
(20.00, 'Ведущий водитель (10-15 лет)'),
(25.00, 'Эксперт (более 15 лет)');

INSERT INTO Driver (full_name, experience_level_id) VALUES
('Иванов Петр Сергеевич', 3),
('Сидоров Алексей Михайлович', 5),
('Козлов Дмитрий Александрович', 2),
('Новиков Сергей Владимирович', 4),
('Морозов Андрей Игоревич', 1),
('Волков Николай Павлович', 6);

INSERT INTO Shipment (route_id, departure_date, arrival_date) VALUES
(1, '2025-03-01 08:00:00', '2025-03-01 20:30:00'),
(2, '2025-03-02 09:00:00', '2025-03-02 23:00:00'),
(3, '2025-03-03 07:00:00', '2025-03-04 05:00:00'),
(4, '2025-03-04 10:00:00', '2025-03-06 08:00:00'),
(5, '2025-03-05 06:00:00', '2025-03-05 16:00:00'),
(6, '2025-03-06 11:00:00', '2025-03-06 19:00:00');

INSERT INTO CrewAssignment (shipment_id, driver_id, bonus) VALUES
(1, 1, 2500.00),
(2, 2, 3400.00),
(3, 3, 2800.00),
(4, 4, 6000.00),
(5, 5, 1400.00),
(6, 6, 3000.00);

--Проверка
SELECT * FROM Route;