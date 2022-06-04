DROP SCHEMA IF EXISTS whatsapp CASCADE;
CREATE SCHEMA whatsapp;

-- Agents
CREATE TABLE whatsapp.agents (
    id VARCHAR(20) PRIMARY KEY
);

-- Contacts
CREATE TABLE whatsapp.contacts (
    id VARCHAR(20) PRIMARY KEY
);

-- Conversations
CREATE TABLE whatsapp.conversations (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(20) NOT NULL REFERENCES whatsapp.contacts (id)
);

-- Messages
DROP TYPE IF EXISTS direction;
CREATE TYPE direction AS ENUM ('inbound', 'outbound');

DROP TYPE IF EXISTS message_status;
CREATE TYPE message_status AS ENUM ('pending', 'success', 'failed');

CREATE TABLE whatsapp.messages (
    -- These fields are from the whatsapp message
    id VARCHAR(255) PRIMARY KEY,

    sender_phone VARCHAR(20) NOT NULL,
    receiver_phone VARCHAR(20) NOT NULL,
    route_id VARCHAR(20) NOT NULL,
    timestamp VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL,
    content JSONB NOT NULL,

    -- Synthetic fields
    direction direction NOT NULL,
    automated BOOLEAN NOT NULL,
    status message_status NOT NULL DEFAULT 'pending',
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()

    -- Our conversation ID
    --conversation_id INT NOT NULL REFERENCES whatsapp.conversations (id)
);
