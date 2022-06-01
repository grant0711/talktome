CREATE SCHEMA IF NOT EXISTS examplecompany;

DROP TABLE IF EXISTS examplecompany.contacts CASCADE;

CREATE TABLE examplecompany.contacts (
    wa_id VARCHAR(20) PRIMARY KEY,
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    vars JSONB
);
