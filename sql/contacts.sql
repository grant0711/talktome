/*
This is to hold information on our contacts, i.e. people who
contact the company for any reason
*/
CREATE SCHEMA IF NOT EXISTS examplecompany;

DROP TABLE IF EXISTS examplecompany.contacts CASCADE;

CREATE TABLE examplecompany.contacts (
    id INT PRIMARY KEY,
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    vars JSONB
);

/* This creates a unique sequence that we can call using nextval('contact_counter') 
while inserting new information items so that we can execute more inserts concurrently into
this table */
DROP SEQUENCE IF EXISTS examplecompany.contact_counter;
CREATE SEQUENCE examplecompany.contact_counter;

-- Insert some dummy data
INSERT INTO examplecompany.contacts (id, phone_number)
VALUES (nextval('examplecompany.contact_counter'), '+221777777777');
INSERT INTO examplecompany.contacts (id, phone_number)
VALUES (nextval('examplecompany.contact_counter'), '+221777777776');
INSERT INTO examplecompany.contacts (id, phone_number)
VALUES (nextval('examplecompany.contact_counter'), '+221777777775');
INSERT INTO examplecompany.contacts (id, phone_number)
VALUES (nextval('examplecompany.contact_counter'), '+221777777774');
