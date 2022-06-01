"""


"""
import logging
from logging.config import dictConfig

from fastapi import FastAPI, Request
from dotenv import load_dotenv

from config.log_config import log_config
from api.contact_handler import (
    get_or_create_contact
)
from api.auth import authenticate_webhook_request

dictConfig(log_config)
logger = logging.getLogger('development')


load_dotenv()


app = FastAPI()


@app.get("/ping")
async def ping():
    logger.debug(f'Ping request: Logs are operational; log level {logger.level}')
    return {"message": "Server is up and running"}


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
    #payload = await request.body()
    #if not authenticate_webhook_request(logger, headers.get('x-hub-signature', ''), payload):
    #    return {"message": "Webhook request not authorized"}

    body = await request.json()

    # Check if we have received from this contact before
    # Add to contacts if we haven't received from this contact
    changes = body['entry'][0]['changes'][0]

    contact_profile = changes['value']['contacts'][0]['profile']
    message = changes['value']['messages'][0]

    logger.debug(contact_profile)
    logger.debug(message)

    contact_info = get_or_create_contact(logger, contact_profile['wa_id'])

    logger.debug(contact_info)

    # Write this event to the events table

    # Handle the event

    logger.debug(f'Incoming message: {body}')
    return "Incoming message"


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
            }, 'wa_id': '221784269198'
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