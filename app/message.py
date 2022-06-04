import json

from app.classifier import Classifier
from app import postgres


def convert(input):
    if type(input) == int:
        return str(input)
    elif type(input) == dict:
        return "'" + json.dumps(input) + "'"
    elif type(input) == str:
        return "'" + input + "'"
    elif type(input) == bool:
        return 'TRUE' if input else 'FALSE'

    raise Exception(f'Input datatype : {type(input)} not handled')

def insert_message(logger, message):
    columns = ', '.join(list(vars(message).keys()))
    values = ', '.join([convert(x) for x in list(vars(message).values())])
    sql = f"INSERT INTO whatsapp.messages ({columns}) VALUES ({values}) RETURNING *;"
    message_info = postgres.execute(logger, sql, commit=True)
    logger.debug(message_info)



class InboundMessage:
    def __init__(self, logger, body):
        changes = body['entry'][0]['changes'][0]
        field = changes['field']
        value = changes['value']
        
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

        # Insert our message to postgres
        insert_message(logger, self)

        # Classify the message
        self.classify(logger)

        logger.debug(vars(self))


    def push_to_conversation(self, logger):
        pass



    def classify(self, logger):
        self.classification_array = Classifier.classify(self, logger)
        logger.debug(self.classification_array)


class OutboundMessage:
    def __init__(self, data, logger):
        pass


