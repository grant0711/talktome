from fastapi.testclient import TestClient

from app.src.main import app


client = TestClient(app)

def test_app_up():
    response = client.get("/")
    assert response.status_code == 200



# Example payload coming from whatsapp
"""
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
"""
