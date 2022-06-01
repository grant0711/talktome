import json

from . import async_postgres

def insert_incoming_event(logger, message_info, contact_info):
    """
    
    """
    logger.debug(f"MESSAGE INFO : {message_info}")
    logger.debug(f"CONTACT INFO : {contact_info}")

    # Transform our dicts into strings for JSONB insert or set as None
    text = "'"+json.dumps(message_info.get("text"))+"'" if message_info.get("text") else None
    image = "'"+json.dumps(message_info.get("image"))+"'" if message_info.get("image") else None
    audio = "'"+json.dumps(message_info.get("audio"))+"'" if message_info.get("audio") else None
    document = "'"+json.dumps(message_info.get("document"))+"'" if message_info.get("document") else None

    sql = f"""
        INSERT INTO whatsapp.events (message_id, timestamp, type, text, image, audio, document, direction, automated, contact_id)
        VALUES ('{message_info["id"]}', '{message_info["timestamp"]}', '{message_info["type"]}', {text}, {image}, {audio}, {document}', 'inbound', FALSE, '{contact_info["wa_id"]}')
        RETURNING message_id;
    """
    message_id = async_postgres.execute(logger, 'heroku', sql, commit=True)
    logger.info(message_id)
    return message_id
