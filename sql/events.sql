/*
Events are simply inbound or outbound whatsapp messages or media

We record every event sent or received here, linking it to a specific contact or agent
*/
CREATE SCHEMA IF NOT EXISTS whatsapp;

DROP TABLE IF EXISTS whatsapp.events;

DROP TYPE IF EXISTS direction;
CREATE TYPE direction AS ENUM ('inbound', 'outbound');

CREATE TABLE whatsapp.events (
    -- These fields are from the whatsapp message
    message_id VARCHAR(255) PRIMARY KEY,
    timestamp VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL,
    text JSONB,
    image JSONB,
    audio JSONB,
    document JSONB,

    -- These are synthetic fields we create
    direction direction NOT NULL,
    automated BOOLEAN NOT NULL, -- Set to TRUE for events sent by robot, FALSE for events sent by humans
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),

    -- Links to agents and contacts
    contact_id VARCHAR(20) NOT NULL,
    agent_id VARCHAR(20), -- myAgro agent ID, optional only for human-sent outbound events
    
     
    CONSTRAINT fk_contact FOREIGN KEY (contact_id) REFERENCES whatsapp.contacts(wa_id),
    CONSTRAINT fk_agent FOREIGN KEY (agent_id) REFERENCES whatsapp.agents(id)
);
