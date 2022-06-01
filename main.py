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
        - It doesn't appear that there is a built-in security method on the whatsapp api, no token
          is included on incoming requests, so we don't currently have a way to ensure that the incoming
          requests are actually coming from Whatsapp
        - When using the Starlette Request object directly in FastAPI, the automatic swagger documentation
          does not function as intended, considering the security risks of an unprotected endpoint
          this is actually the desirable behavior for the moment
    """
    headers = request.headers
    logger.debug(headers)

    body = await request.json()

    # Check if we have received from this contact before
    # Add to contacts if we haven't received from this contact
    contact_info = get_or_create_contact(logger, '221784269198')

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
    