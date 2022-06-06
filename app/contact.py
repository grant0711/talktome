from app import postgres


class Contact:
    def __init__(self, logger, id):
        # FIXME Check if contact is in redis cache and return it if it is, this will be
        # the case if there is a current ongoing conversation occurring with this contact
        # so that means that we will only make a database call on incoming messages
        # where there is no ongoing conversation


        # Check if the contact has been created in postgres and return the contact id if it has
        sql_statements = [
            f"SELECT id FROM whatsapp.contacts WHERE id='{id}';",
            f"INSERT INTO whatsapp.contacts (id) VALUES ('{id}') RETURNING id;"
        ]

        for statement in sql_statements:
            contact_info = postgres.execute(logger, statement)
            logger.debug(contact_info)
            try:
                if len(contact_info[0].get('id')) > 0:
                    self.id = contact_info[0]['id']
                    break
            except IndexError:
                pass