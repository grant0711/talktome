import json
import datetime
import random
import string

import requests

PRODUCTION_URL = 'https://talk2me-customer-interface-app.herokuapp.com'
LOCAL_URL = 'http://127.0.0.1:8000'


def test_incoming_text_message(url, body):
    letters = string.ascii_letters
    random_message_id = 'wamid.' + ''.join(random.choice(letters) for i in range(50))
    unix_timestamp = datetime.datetime.utcnow().strftime('%s')

    payload = {
        'object': 'whatsapp_business_account',
        'entry': [{
            'id': '111201064929199',
            'changes': [{
                'value': {
                    'messaging_product': 'whatsapp',
                    'metadata': {
                        'display_phone_number': '15550901162',
                        'phone_number_id': '109551705096305'
                    }, 
                    'contacts': [{
                        'profile': {
                            'name': 'Grant'
                        },
                        'wa_id': '221784269198'
                        }],
                    'messages': [{
                        'from': '221784269198',
                        'id': random_message_id,
                        'timestamp': unix_timestamp,
                        'text': {
                            'body': body
                        },
                        'type': 'text'
                    }]},
                'field': 'messages'
        }]}
    ]}
    response = requests.post(url + '/webhook', json.dumps(payload))
    print(response.text)


if __name__ == "__main__":
    test_incoming_text_message(LOCAL_URL, 'hello world')