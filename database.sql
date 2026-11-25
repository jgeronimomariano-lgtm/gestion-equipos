-- =====================================================
-- Sistema de Gestión y Préstamo de Equipos de Cómputo
-- Script: database.sql
-- Motor: MySQL / MariaDB
-- =====================================================

-- Fuerza UTF-8 para que las tildes (Portátil, Préstamo) se guarden bien
SET NAMES utf8mb4;

DROP DATABASE IF EXISTS gestion_equipos;
CREATE DATABASE gestion_equipos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE gestion_equipos;

-- -----------------------------------------------------
-- Tabla: Equipos (inventario)
-- -----------------------------------------------------
CREATE TABLE Equipos (
    id_equipo        INT AUTO_INCREMENT PRIMARY KEY,
    serial           VARCHAR(50)  NOT NULL UNIQUE,
    tipo_dispositivo ENUM('PC de escritorio', 'Portátil', 'Tablet', 'Router') NOT NULL,
    marca            VARCHAR(50)  NOT NULL,
    modelo           VARCHAR(50)  NOT NULL,
    estado           ENUM('Disponible', 'En Préstamo', 'En Mantenimiento')
                     NOT NULL DEFAULT 'Disponible'
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Tabla: Usuarios (aprendices e instructores)
-- -----------------------------------------------------
CREATE TABLE Usuarios (
    documento        VARCHAR(20)  PRIMARY KEY,
    nombre_completo  VARCHAR(100) NOT NULL,
    rol              ENUM('Aprendiz', 'Instructor') NOT NULL
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Tabla: Prestamos (transaccional: une Usuarios y Equipos)
-- fecha_devolucion es NULL mientras el equipo no se devuelva
-- -----------------------------------------------------
CREATE TABLE Prestamos (
    id_prestamo       INT AUTO_INCREMENT PRIMARY KEY,
    documento_usuario VARCHAR(20) NOT NULL,
    id_equipo         INT         NOT NULL,
    fecha_salida      DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion  DATETIME    NULL,
    CONSTRAINT fk_prestamo_usuario
        FOREIGN KEY (documento_usuario) REFERENCES Usuarios(documento)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prestamo_equipo
        FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =====================================================
-- DATOS DE PRUEBA
-- =====================================================

INSERT INTO Equipos (serial, tipo_dispositivo, marca, modelo, estado) VALUES
('PC-HP-0001',   'PC de escritorio', 'HP',      'ProDesk 400 G7', 'Disponible'),
('PC-DELL-0002', 'PC de escritorio', 'Dell',    'OptiPlex 3080',  'Disponible'),
('LT-LEN-0003',  'Portátil',         'Lenovo',  'ThinkPad E14',   'En Préstamo'),
('LT-ASU-0004',  'Portátil',         'Asus',    'VivoBook 15',    'Disponible'),
('LT-HP-0005',   'Portátil',         'HP',      'Pavilion 14',    'En Préstamo'),
('TB-SAM-0006',  'Tablet',           'Samsung', 'Galaxy Tab A8',  'Disponible'),
('RT-TPL-0007',  'Router',           'TP-Link', 'Archer C6',      'En Mantenimiento'),
('RT-CIS-0008',  'Router',           'Cisco',   'RV340',          'Disponible');

INSERT INTO Usuarios (documento, nombre_completo, rol) VALUES
('1001234567', 'Carlos Andrés Mejía Torres',    'Aprendiz'),
('1002345678', 'Laura Sofía Pérez Gómez',       'Aprendiz'),
('1003456789', 'Miguel Ángel Rodríguez Ruiz',   'Aprendiz'),
('72345678',   'Jesus Ernesto Aviles Vizcaino', 'Instructor'),
('32456789',   'Marta Lucía Herrera Castro',    'Instructor');

-- Dos préstamos ya devueltos (historial)
INSERT INTO Prestamos (documento_usuario, id_equipo, fecha_salida, fecha_devolucion) VALUES
('1001234567', 1, '2026-11-10 08:00:00', '2026-11-10 12:30:00'),
('1002345678', 6, '2026-11-12 14:00:00', '2026-11-13 09:15:00');

-- Dos préstamos activos (coinciden con los equipos 'En Préstamo')
INSERT INTO Prestamos (documento_usuario, id_equipo, fecha_salida, fecha_devolucion) VALUES
('1003456789', 3, '2026-11-20 07:45:00', NULL),
('72345678',   5, '2026-11-22 10:00:00', NULL);
