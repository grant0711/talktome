import os

from hashlib import sha1
import hmac


def authenticate_webhook_request(logger, x_hub_signature, payload):
    """

    
    """

    test_signature = hmac.digest(os.environ['WEBHOOK_SECRET'].encode(), payload, 'sha1')
    print(test_signature)
    print(x_hub_signature)

    if test_signature != x_hub_signature:
        logger.debug(f'UNAUTHORIZED incoming request: {payload}')
        return False

    return True