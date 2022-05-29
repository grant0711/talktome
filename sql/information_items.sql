/* This is how we will store individual items of information coming from or going to
our customers. The various types of information items we will track are:

- Text messages
- Phone calls
- Images
- Voice recordings

Initially we will only concern ourselves with text messages for simplicity */

CREATE SCHEMA IF NOT EXISTS examplecompany;

DROP TABLE IF EXISTS examplecompany.information_items;

CREATE TABLE examplecompany.information_items (
    id INT PRIMARY KEY,
    contact_id INT NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    content TEXT,
    time_created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
     
    CONSTRAINT fk_contact FOREIGN KEY (contact_id) REFERENCES examplecompany.contacts(id)
);

/* This creates a unique sequence that we can call using nextval('information_item_counter') 
while inserting new information items so that we can execute more inserts concurrently into
this table */
DROP SEQUENCE IF EXISTS examplecompany.information_item_counter;
CREATE SEQUENCE examplecompany.information_item_counter;

-- Insert some dummy data
INSERT INTO examplecompany.information_items (id, contact_id, content_type, content)
VALUES (nextval('examplecompany.information_item_counter'), 1, 'text/sms', 'First message from contact 1');
INSERT INTO examplecompany.information_items (id, contact_id, content_type, content)
VALUES (nextval('examplecompany.information_item_counter'), 1, 'text/sms', 'Second message from contact 1');
INSERT INTO examplecompany.information_items (id, contact_id, content_type, content)
VALUES (nextval('examplecompany.information_item_counter'), 1, 'text/sms', 'Third message from contact 1');
