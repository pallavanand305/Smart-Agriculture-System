-- Smart Agriculture System — PostgreSQL Schema
-- Run: psql -U postgres -d smart_agri -f schema.sql

CREATE TABLE IF NOT EXISTS farms (
    farm_id      SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    location     VARCHAR(200),
    area_hectares DECIMAL(8,2),
    owner_name   VARCHAR(100),
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS zones (
    zone_id    SERIAL PRIMARY KEY,
    farm_id    INT REFERENCES farms(farm_id) ON DELETE CASCADE,
    zone_name  VARCHAR(50) NOT NULL,
    latitude   DECIMAL(10,7),
    longitude  DECIMAL(10,7),
    crop_type  VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS sensor_nodes (
    node_id    SERIAL PRIMARY KEY,
    zone_id    INT REFERENCES zones(zone_id) ON DELETE CASCADE,
    node_type  VARCHAR(50),
    mac_address VARCHAR(17) UNIQUE,
    status     VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    reading_id    BIGSERIAL PRIMARY KEY,
    node_id       INT REFERENCES sensor_nodes(node_id),
    temperature   DECIMAL(5,2),
    humidity      DECIMAL(5,2),
    soil_moisture DECIMAL(5,2),
    n_level       DECIMAL(6,2),
    p_level       DECIMAL(6,2),
    k_level       DECIMAL(6,2),
    ph            DECIMAL(4,2),
    co2           DECIMAL(7,2),
    timestamp     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id        SERIAL PRIMARY KEY,
    zone_id        INT REFERENCES zones(zone_id),
    task_type      VARCHAR(50),
    priority_score DECIMAL(8,6),
    status         VARCHAR(20) DEFAULT 'pending',
    created_at     TIMESTAMP DEFAULT NOW(),
    due_at         TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ml_predictions (
    pred_id           SERIAL PRIMARY KEY,
    zone_id           INT REFERENCES zones(zone_id),
    crop_label        VARCHAR(50),
    confidence        DECIMAL(5,3),
    yield_estimate    DECIMAL(6,2),
    moisture_forecast DECIMAL(5,2),
    created_at        TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    user_id       SERIAL PRIMARY KEY,
    farm_id       INT REFERENCES farms(farm_id),
    username      VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(20) DEFAULT 'farmer',
    email         VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id   SERIAL PRIMARY KEY,
    zone_id    INT REFERENCES zones(zone_id),
    user_id    INT REFERENCES users(user_id),
    alert_type VARCHAR(50),
    message    TEXT,
    sent_at    TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast time-range queries on sensor_readings
CREATE INDEX IF NOT EXISTS idx_readings_timestamp ON sensor_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_readings_node      ON sensor_readings(node_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_tasks_zone_status  ON tasks(zone_id, status);
