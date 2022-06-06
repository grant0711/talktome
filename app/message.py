from app.classifier import Classifier
from app import postgres
from app.conversation import Conversation



def insert_message(logger, message):
    """
    Inserts a message into whatsapp.messages postgres table

    Inputs:
        - logger: logger object
        - message: instance of class Message (InboundMessage or OutboundMessage)
    Outputs:
        - dict columns as keys, values as values of inserted row
    """
    columns = [
        'id',
        'sender_phone',
        'receiver_phone',
        'route_id',
        'timestamp',
        'type',
        'content',
        'direction',
        'automated'
    ]
    value_str = ', '.join([postgres.convert_to_str(vars(message).get(x)) for x in columns])
    column_str = ', '.join(columns)
    sql = f"INSERT INTO whatsapp.messages ({column_str}) VALUES ({value_str}) RETURNING *;"
    return postgres.execute(logger, sql, commit=True)



class InboundMessage:
    def __init__(self, logger, body):
        changes = body['entry'][0]['changes'][0]
        field = changes['field']
        value = changes['value']
        
        # Index fields we need in postgres out of json payload
        self.id = value[field][0]['id']
        self.sender_phone = value['contacts'][0]['wa_id']
        self.receiver_phone = value['metadata']['display_phone_number']
        self.route_id = value['metadata']['phone_number_id']
        self.timestamp = value[field][0]['timestamp']
        self.type = value[field][0]['type']
        self.content = value[field][0][self.type]

        # Synthetic fields
        self.direction = 'inbound'
        self.automated = False

        # Link message to conversation
        self.conversation = Conversation(logger, contact_id=self.sender_phone)
        self.conversation_id = self.conversation.id

        # Insert our message to postgres now before classifying and before responding
        # to the message within our conversation
        insert_message(logger, self)

        # Classify the message
        self.classification_array = Classifier.classify(logger, self)

        # Add our message to the conversation
        self.conversation.add_message(self)

        # Run our conversation logic
        self.conversation.run()


class OutboundMessage:
    def __init__(self, logger, data):
        pass


