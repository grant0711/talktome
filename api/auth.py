import os

import hmac
import base64


def authenticate_webhook_request(logger, x_hub_signature, payload):
    """

    
    """

    test_signature = hmac.digest(os.environ['WEBHOOK_SECRET'].encode(), payload, 'sha1')
    test_signature = base64.b64encode(test_signature).decode('utf-8')

    print(test_signature)
    print(x_hub_signature)

    if test_signature != x_hub_signature:
        logger.debug(f'UNAUTHORIZED incoming request: {payload}')
        return False

    return True