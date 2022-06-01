import os

from hashlib import sha1


def authenticate_webhook_request(logger, x_hub_signature, payload):
    """

    
    """
    sha1_string = sha1((payload + os.environ['WEBHOOK_SECRET']).encode()).hexdigest()
    print(sha1_string)
    print(x_hub_signature)

    if sha1_string != x_hub_signature:
        logger.debug(f'UNAUTHORIZED incoming request: {payload}')
        return False

    return True