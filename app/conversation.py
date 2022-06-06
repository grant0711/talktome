import datetime

from app import postgres
from app.contact import Contact


def get_or_create_conversation(logger, contact_id):
    """
    
    
    """
    # Check in redis cache if a conversation exists for the current contact_id
    # If it does exist, return it
    # If it doesn't exist, instantiate a new Converation isntance and return it

    # FIXME placeholder for redis cache
    redis = {}
    if redis.get(contact_id):
        return redis[contact_id]

    return Conversation(contact_id)



class Conversation:
    def __init__(self, logger, id=None, contact_id=None, messages=None, state=None):
        self.id = id if id else self.insert_new_conversation(logger, contact_id)
        self.contact_id = contact_id if contact_id else self.contact_id
        self.messages = messages if messages else []
        self.state = state if state else {
            'state' :'initialized',
            'initialized_timestamp': datetime.datetime.utcnow()
        }


    def insert_new_conversation(self, logger, contact_id):
        # Check if our contact_id is in postgres or not
        contact = Contact(logger, contact_id)
        self.contact_id = contact.id

        # Insert our new conversation
        sql = f"INSERT INTO whatsapp.conversations (contact_id) VALUES ('{self.contact_id}') RETURNING id;"
        new_conversation = postgres.execute(logger, sql, commit=True)

        return new_conversation['id']


    def add_message(self, message):
        self.messages = self.messages.insert(0, message)


    def run(self, logger):
        """
        This is where all of the logic will execute to determine and send the response required
        for this specific conversation

        Outputs:
            - bool: True if run produces a successful response to sender, False if an error occurs
        """
        logger.debug('Running the conversation')
        for message in self.messages:
            logger.debug(message)


        return True
        