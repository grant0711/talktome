import json

from . import async_postgres


def insert_incoming_event(logger, message_info, contact_info):
    """
    Inserts incoming message event into postgres

    Inputs:
        - logger: logger object
        - message_info: dict 'messages' key within message post request body
        - contact_info: dict client info returning from contact insert statement
    Outputs:
        - dict with 'message_id' key and value pair if successful, empty list if unsucessful insert
    """
    # Transform our dicts into strings for JSONB insert or set as NULL
    text = "'"+json.dumps(message_info.get("text"))+"'" if message_info.get("text") else "NULL"
    image = "'"+json.dumps(message_info.get("image"))+"'" if message_info.get("image") else "NULL"
    audio = "'"+json.dumps(message_info.get("audio"))+"'" if message_info.get("audio") else "NULL"
    document = "'"+json.dumps(message_info.get("document"))+"'" if message_info.get("document") else "NULL"

    sql = f"""
        INSERT INTO whatsapp.events (message_id, timestamp, type, text, image, audio, document, direction, automated, contact_id)
        VALUES ('{message_info["id"]}', '{message_info["timestamp"]}', '{message_info["type"]}', {text}, {image}, {audio}, {document}, 'inbound', FALSE, '{contact_info["wa_id"]}')
        RETURNING message_id;
    """
    message_id = async_postgres.execute(logger, 'heroku', sql, commit=True)
    return message_id[0]