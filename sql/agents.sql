/*
Agents are the myAgro staff that will be interacting with contacts when required, i.e. call center staff

We will want to track what these staff are communicating so we will link outbound events with agents if
sent by the agent
*/

CREATE SCHEMA IF NOT EXISTS whatsapp;

DROP TABLE IF EXISTS whatsapp.agents CASCADE;

CREATE TABLE whatsapp.agents (
    id VARCHAR(20) PRIMARY KEY, -- myAgro staff ID
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
