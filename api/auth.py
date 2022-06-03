import os

import hmac
from hashlib import sha1


def authenticate_webhook_request(logger, x_hub_signature, payload):
    """
    Authenticates the incoming request to ensure that it is arriving from Whatsapp API

    Inputs:
        - logger: logger object
        - x_hub_signature: str x-hub-signature header value on the incoming request
        - payload: bytes body of request

    Reference: https://developers.facebook.com/docs/graph-api/webhooks/getting-started/#:~:text=int-,Validating%20Payloads,-We%20sign%20all

    FIXME:
        - This doesn't work, I don't know why
        - The docs mention something about the encoding being 'unicode-escape' but I can't figure this out
    """
    test_signature = hmac.new(os.environ['WEBHOOK_SECRET'].encode(), payload.decode().encode('unicode-escape'), sha1).hexdigest()

    logger.debug(f'x_hub_signature: {x_hub_signature}')
    logger.debug(f'test_signature: {test_signature}')


    if test_signature != x_hub_signature[3:]:
        logger.debug(f'UNAUTHORIZED incoming request: {payload}')
        return False

    return True