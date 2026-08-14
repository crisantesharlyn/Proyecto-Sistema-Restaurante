-- ============================================================
-- Sistema de Gestión de Restaurante — Script DDL + datos base
-- Basado en el script del profesor + tabla historial (auditoría)
-- ============================================================

CREATE DATABASE restaurante;

-- Conéctate a la base 'restaurante' antes de ejecutar lo siguiente
-- (en psql: \c restaurante)

CREATE TABLE plato (
    id_plato   SERIAL       PRIMARY KEY,
    nombre     VARCHAR(50)  NOT NULL,
    precio     FLOAT        NOT NULL,
    emoji      VARCHAR(10)
);

CREATE TABLE cliente (
    id_cliente SERIAL       PRIMARY KEY,
    nombre     VARCHAR(50)  NOT NULL
);

CREATE TABLE pedido (
    id_pedido  SERIAL       PRIMARY KEY,
    id_cliente INT          NOT NULL
                REFERENCES cliente(id_cliente)
                ON DELETE RESTRICT,
    total      FLOAT        NOT NULL DEFAULT 0,
    estado     VARCHAR(20)  NOT NULL DEFAULT 'Pendiente'
                CHECK (estado IN ('Pendiente', 'En cocina', 'Listo')),
    fecha      TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE pedido_plato (
    id_pedido  INT          NOT NULL
                REFERENCES pedido(id_pedido)
                ON DELETE CASCADE,
    id_plato   INT          NOT NULL
                REFERENCES plato(id_plato)
                ON DELETE RESTRICT,
    cantidad   INT          NOT NULL DEFAULT 1,
    PRIMARY KEY (id_pedido, id_plato)
);

-- Tabla de auditoría (patrón "Historial" que usa el profesor)
CREATE TABLE historial (
    id      SERIAL       PRIMARY KEY,
    fecha   VARCHAR(20)  NOT NULL,
    hora    VARCHAR(20)  NOT NULL,
    accion  VARCHAR(255) NOT NULL
);

-- Datos base
INSERT INTO plato (nombre, precio, emoji) VALUES
    ('Chaufa',  10.00, '🍚'),
    ('Caldo',   15.00, '🍲'),
    ('Gaseosa',  5.00, '🥤');

INSERT INTO cliente (nombre) VALUES
    ('Juan'),
    ('María');

INSERT INTO pedido (id_cliente, total, estado) VALUES (1, 25.00, 'Listo');
INSERT INTO pedido_plato (id_pedido, id_plato, cantidad) VALUES (1, 1, 1), (1, 2, 1);

INSERT INTO pedido (id_cliente, total, estado) VALUES (2, 15.00, 'En cocina');
INSERT INTO pedido_plato (id_pedido, id_plato, cantidad) VALUES (2, 2, 1);

INSERT INTO pedido (id_cliente, total, estado) VALUES (1, 20.00, 'Pendiente');
INSERT INTO pedido_plato (id_pedido, id_plato, cantidad) VALUES (3, 2, 1), (3, 3, 1);
