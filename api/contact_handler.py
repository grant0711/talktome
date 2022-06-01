"""


"""
from lib import async_postgres


def get_contact_detailed_info(logger, wa_id):
    """
    
    """
    sql = f"SELECT * FROM whatsapp.contacts WHERE wa_id='{wa_id}';"
    contact_info = async_postgres.execute(logger, 'heroku', sql)

    try:
        return contact_info[0]
    except IndexError:
        logger.debug(f'Contact not found: {wa_id}')
        return {}


def create_contact(logger, wa_id):
    """
    
    """
    sql = f"INSERT INTO whatsapp.contacts (wa_id) VALUES ('{wa_id}') RETURNING *;"
    contact_info = async_postgres.execute(logger, 'heroku', sql, commit=True)
    return contact_info[0]


def get_or_create_contact(logger, wa_id):
    """
    """
    # FIXME redis cache check key and return value if found

    contact_info = get_contact_detailed_info(logger, wa_id)

    if len(contact_info) == 0:
        contact_info = create_contact(logger, wa_id)

        # FIXME redis cache set key/value here
    
    return contact_info


def update_contact_info(logger, wa_id, vars):
    """
    
    """
    # Update the vars column on the contact with something new
    # Clear the redis cache for this specific contact key
    pass