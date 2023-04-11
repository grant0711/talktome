from app import postgres


class Contact:
    def __init__(self, logger, id):
        # FIXME Check if contact is in redis cache and return it if it is, because contacts are
        # just whatsapp telephone numbers these will never be changed, if we do want to
        # link additional variables to contacts in the future we will need a method to clear the redis
        # cache after updating variables
        redis = {}
        if redis.get(id):
            self.id = id


        # Check if the contact has been created in postgres and return the contact id if it has
        sql_statements = [
            f"SELECT id FROM whatsapp.contacts WHERE id='{id}';",
            f"INSERT INTO whatsapp.contacts (id) VALUES ('{id}') RETURNING id;"
        ]

        for statement in sql_statements:
            contact_info = postgres.execute(logger, statement, commit=True)

            if contact_info == []:
                pass
            
            elif contact_info.get('id'):
                self.id = contact_info['id']
                break
