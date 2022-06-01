CREATE SCHEMA IF NOT EXISTS examplecompany;

DROP TABLE IF EXISTS examplecompany.events;

CREATE TABLE examplecompany.events (
    message_id VARCHAR(255) PRIMARY KEY,
    contact_id VARCHAR(20) NOT NULL,

    timestamp VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL,
    text JSONB,
    image JSONB,
    audio JSONB,
    document JSONB,

    direction VARCHAR(8) NOT NULL,
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
     
    CONSTRAINT fk_contact FOREIGN KEY (contact_id) REFERENCES examplecompany.contacts(wa_id)
);
