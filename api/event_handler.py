from psycopg2.extensions import JSON
from . import async_postgres

def insert_incoming_event(logger, message_info, contact_info):
    """
    
    """
    logger.debug(f"MESSAGE INFO : {message_info}")
    logger.debug(f"CONTACT INFO : {contact_info}")

    sql = f"""
        INSERT INTO whatsapp.events (
            message_id,
            timestamp,
            type,
            text,
            image,
            audio,
            document,
            direction,
            automated,
            contact_id) VALUES (
                '{message_info["id"]}',
                '{message_info["timestamp"]}',
                '{message_info["type"]}',
                {JSON(message_info.get("text", {}))},
                {JSON(message_info.get("image", {}))},
                {JSON(message_info.get("audio", {}))},
                {JSON(message_info.get("document", {}))},
                'inbound',
                FALSE,
                '{contact_info["wa_id"]}'
            ) RETURNING message_id;
    """
    message_id = async_postgres.execute(logger, 'heroku', sql, commit=True)

    #sample_contact_info = {
    #    'wa_id': '221784269198',
    #    'time_created': datetime.datetime(2022, 6, 1, 13, 45, 37, 248582),
    #    'vars': None
    #}
    
    #sample_message_info = {
    #    'from': '221784269198',
    #    'id': 'wamid.HBgMMjIxNzg0MjY5MTk4FQIAEhggNkY3Q0MwREU2REQ2RkM5NzlCMzU2QjcyQjYxODgyMkEA',
    #    'timestamp': '1654091136',
    #    'text': {
    #        'body': 'Test21'
    #    },
    #    'type': 'text'
    #}