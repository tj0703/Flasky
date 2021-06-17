import requests
import unittest
import json

class UserEndpointsTest(unittest.TestCase):

    def get_api_headers(self, token):
        return {
            'Token': token, 'Content-Type': 'application/json'
        }

    def get_api_headers_not_json(self, token):
        return {
            'Token': token, 'Content-Type': 'application/text'
        }

    def generate_auth_token(self, username, password):
        auth = (username, password)
        r = requests.get('http://0.0.0.0:8080/api/auth/token', auth=auth)
        response = json.loads(r.content)
        if response.get('status') == 'FAILURE':
            return None, r.json()
        res = r.json()
        token = res.get('token')
        return token, r.json()

    def test_existing_user_record(self):
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)
        r = requests.get(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers(auth_token))
        response = json.loads(r.content)
        self.assertIn('retrieval succesful', response.get('message'))

    def check_user_data_after_update(self, username, password, attr, data):
        auth_token = self.generate_auth_token(username, password)
        r = requests.get(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers(auth_token))
        response = json.loads(r.content)
        self.assertIn(data, response.get('payload').get(attr))
        return r.status_code

    def test_non_existing_user_record(self):
        with open('./user2.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)
        r = requests.get(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers(auth_token))
        response = r.json().get('message')
        self.assertIn('Token authentication required', response)

    def test_user_records_exists(self):
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)
        r = requests.get('http://0.0.0.0:8080/api/users', headers=self.get_api_headers(auth_token))
        payload = r.json().get('payload')
        self.assertIn(username, payload)

    def test_update_user_using_json_header(self):
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)
        with open('./updatedata.json') as f:
            params = json.load(f)
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers(auth_token),
                         data=json.dumps(params))
        response = r.json().get('message')
        self.assertIn('Updated', response)

    def test_update_user_incorrect_field(self):
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)
        attr = "password"
        update_data = "abcd1234"
        params = {attr: update_data}
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers(auth_token),
                         data=json.dumps(params))
        response = r.json().get('message')
        self.assertIn('Field update not allowed', response)

    def test_update_user_using_text_header(self):
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)
        with open('./updatedata.json') as f:
            params = json.load(f)
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers_not_json(auth_token),
                         data=json.dumps(params))
        response = r.json().get('message')
        self.assertIn('Bad Request', response)

    def test_update_user_firstname(self):
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)

        attr = "firstname"
        with open('./updatedata.json') as f:
            data = json.load(f)
        update_data = data["firstname"]
        params = {attr: update_data}
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers(auth_token),
                             data=json.dumps(params))
        if r.status_code == 200:
            self.asserEqual(200, self.check_user_data_after_update(username, password, attr, update_data))


    def test_update_user_phone(self):
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token, status_message = self.generate_auth_token(username, password)
        attr = "phone"
        with open('./updatedata.json') as f:
            data = json.load(f)
        update_data = data["phone"]
        params = {attr: update_data}
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers(auth_token),
                             data=json.dumps(params))
        if r.status_code == 200:
            self.asserEqual(200, self.check_user_data_after_update(username, password, attr, update_data))


if __name__ == '__main__':
    unittest.main(verbosity=2)
