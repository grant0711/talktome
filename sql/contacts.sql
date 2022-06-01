/*
Contacts are simply people who utilize whatsapp to contact us, we use the whatsapp unique ID
as unique reference code

We would eventually want to link this in some way with our systems
Contacts could either be interested farmers (leads), current clients, VEs, or SLs

The vars column is intended as a flexible way of managing state of contacts when automating
conversation flows, i.e. we would simply update this variable with whatever we like as events
are coming/going to/from the contact to be able to create complex interactions
*/
CREATE SCHEMA IF NOT EXISTS whatsapp;

DROP TABLE IF EXISTS whatsapp.contacts CASCADE;

CREATE TABLE whatsapp.contacts (
    wa_id VARCHAR(20) PRIMARY KEY,
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    vars JSONB
);
