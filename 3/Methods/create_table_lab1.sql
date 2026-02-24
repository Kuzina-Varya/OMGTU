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