import os

import hmac
from hashlib import sha1


def authenticate_webhook_request(logger, x_hub_signature, payload):
    """

    
    """

    test_signature = hmac.new(os.environ['WEBHOOK_SECRET'].encode(), payload.decode().encode('unicode-escape'), sha1).hexdigest()

    print(test_signature)
    print(x_hub_signature)

    if test_signature != x_hub_signature[3:]:
        logger.debug(f'UNAUTHORIZED incoming request: {payload}')
        return False

    return True