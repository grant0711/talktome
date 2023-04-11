#import os
#import logging
#from logging.config import dictConfig

from fastapi import (
    FastAPI,
    Request,
    HTTPException
)

#from app.config.log_config import log_config

#dictConfig(log_config)
#logger = logging.getLogger('development')

app = FastAPI()


@app.get("/")
async def index(request: Request):
    return "App is up"

#@app.post("/webhook")
#async def incoming_message(request: Request):
#    """
#    Endpoint to receive all inbound messages from whatsapp api
#    """
#    if not authenticate_webhook_request(logger, request.headers.get('x-hub-signature', ''), await request.body()):
#        return HTTPException(400, detail='NOT AUTHORIZED')
#    
#    body = await request.json()
#    logger.debug(f'INBOUND MESSAGE: {body}')
#    message = InboundMessage(logger, body)
#    return "OK"


#@app.get("/webhook")
#async def verify_webhook(request: Request):
#    """
#    Used by whatsapp api to validate webhook endpoint for the app
#    Documentation: https://developers.facebook.com/docs/graph-api/webhooks/getting-started
#    """
#    try:
#        if request.query_params['hub.verify_token'] == os.environ['WEBHOOK_CONFIG_TOKEN']:
#            return int(request.query_params['hub.challenge'])
#    except IndexError:
#        return HTTPException(400, detail='NOT AUTHORIZED')


#@app.get("/privacy_policy")
#async def privacy_policy():
#    """
#    This is required on setup of the whatsapp api
#    It isn't clear what specifically is required to display as a privacy policy, but simply
#    establishing this endpoint and returning simple text seemed to satisfy the requirement
#    """
#    logger.debug('Privacy policy page accessed')
#    return "FIXME This is a privacy policy. We won't sell your data to 3rd parties."
    