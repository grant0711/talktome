"""


"""
import logging
from logging.config import dictConfig

from fastapi import (
    FastAPI,
    Request,
    HTTPException
)
from dotenv import load_dotenv

from config.log_config import log_config
from api.auth import authenticate_webhook_request
from api.contact_handler import get_or_create_contact
from api.event_handler import insert_incoming_event

dictConfig(log_config)
logger = logging.getLogger('development')

load_dotenv()

app = FastAPI()



@app.post("/webhook")
async def incoming_message(request: Request):
    """
    Endpoint to receive all inbound events from whatsapp api

    Inputs:
        - Starlette Request class object: https://www.starlette.io/requests/

    NOTE:
        - Authentication is not currently deployed
        - When using the Starlette Request object directly in FastAPI, the automatic swagger documentation
          does not function as intended, considering the security risks of an unprotected endpoint
          this is actually the desirable behavior for the moment
    """
    # FIXME we authenticate the incoming webhook request to ensure it's coming from whatsapp
    payload = await request.json()

    headers = request.headers
    if not authenticate_webhook_request(logger, headers.get('x-hub-signature', ''), payload):
        #return HTTPException(400, detail="Webhook secret incorrect")
        pass

    body = await request.json()
    logger.debug(f'Incoming message: {body}')

    changes = body['entry'][0]['changes'][0]['value']

    contact = changes['contacts'][0]
    message_info = changes['messages'][0]

    # Check if we have received from this contact before
    # Add to contacts if we haven't received from this contact
    contact_info = get_or_create_contact(logger, contact['wa_id'])

    # Write this event to the events table
    message_id = insert_incoming_event(logger, message_info, contact_info)

    # If we didn't insert the event then return a failure
    if not message_id.get('message_id'):
        return HTTPException(400, detail="Event not inserted successfully")

    # Handle the event

    
    return {"message": f"message_id {message_id} received successfully"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Used by whatsapp api to validate webhook endpoint for the app

    Documentation: https://developers.facebook.com/docs/graph-api/webhooks/getting-started
    """
    logger.debug(f"Incoming webhook verification request")
    if request.query_params['hub.verify_token'] == "testtoken123":
        return int(request.query_params['hub.challenge'])



@app.get("/privacy_policy")
async def privacy_policy():
    """
    This is required on setup of the whatsapp api

    It isn't clear what specifically is required to display as a privacy policy, but simply
    establishing this endpoint and returning simple text seemed to satisfy the requirement
    """
    logger.debug('Privacy policy page accessed')
    return "FIXME This is a privacy policy. We won't sell your data to 3rd parties."
    




changes = {
    'value': {
        'messaging_product': 'whatsapp',
        'metadata': {
            'display_phone_number': '15550901162', 'phone_number_id': '109551705096305'
        },
        'contacts': [
            {'profile': {
                'name': 'Grant'
            },
            'wa_id': '221784269198'
        }],
        
        'messages': [
            {
                'from': '221784269198',
                'id': 'wamid.HBgMMjIxNzg0MjY5MTk4FQIAEhggMDE2OEU4REMyRjBBODNDQ0ZDNkFGRkYwRUMxMUM3NUUA',
                'timestamp': '1654089912',
                'text': {
                    'body': 'Test17'
                }, 'type': 'text'
            }]
    }, 'field': 'messages'}