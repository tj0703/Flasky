import requests
import unittest
import json
import xmlrunner


class UserEndpointsTest(unittest.TestCase):

    def get_api_headers(self, token):
        return {'Token': token, 'Content-Type': 'application/json'}

    def get_api_headers_not_json(self, token):
        return {'Token': token, 'Content-Type': 'application/text'}


    def generate_auth_token(self, username, password):
        """returns authentication token and response from the endpoint"""
        auth = (username, password)
        r = requests.get('http://0.0.0.0:8080/api/auth/token', auth=auth)
        response = json.loads(r.content)
        if response.get('status') == 'FAILURE':
            return None, r.json()
        res = r.json()
        token = res.get('token')
        return token

    def test_existing_user_record(self):
        # tests if the existing user record is retrievable
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token = str(self.generate_auth_token(username, password))
        r = requests.get(f'http://0.0.0.0:8080/api/users/{username}', headers={'Token': auth_token, 'Content-Type': 'application/json'})
        response = json.loads(r.content)
        self.assertIn('retrieval succesful', response.get('message'))

    def check_user_data_after_update(self, username, password, attr, data):
        """Checks if the user record is updated with new data"""
        auth_token = str(self.generate_auth_token(username, password))
        r = requests.get(f'http://0.0.0.0:8080/api/users/{username}', headers={'Token': auth_token, 'Content-Type': 'application/json'})
        response = json.loads(r.content)
        self.assertIn(data, response.get('payload').get(attr))
        return r.status_code

    def test_non_existing_user_record(self):
        # tests if the non existing user record is unavailable
        with open('./user2.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token = str(self.generate_auth_token(username, password))
        r = requests.get(f'http://0.0.0.0:8080/api/users/{username}', headers={'Token': auth_token, 'Content-Type': 'application/json'})
        response = r.json().get('message')
        self.assertIn('Invalid Token', response)

    def test_user_records_exists(self):
        # tests if all the user records are stored in the database
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token = str(self.generate_auth_token(username, password))
        r = requests.get('http://0.0.0.0:8080/api/users', headers={'Token': auth_token, 'Content-Type': 'application/json'})
        payload = r.json().get('payload')
        self.assertIn(username, payload)

    def test_update_user_using_json_header(self):
        # tests the update functionality of each allowed field
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token = str(self.generate_auth_token(username, password))
        with open('./updatedata.json') as f:
            params = json.load(f)
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers={'Token': auth_token, 'Content-Type': 'application/json'},
                         data=json.dumps(params))
        response = r.json().get('message')
        self.assertIn('Updated', response)

    def test_update_user_incorrect_field(self):
        # tests the update functionality throws error when unavailable field is updated
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token= str(self.generate_auth_token(username, password))
        attr = "password"
        update_data = "abcd1234"
        params = {attr: update_data}
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers={'Token': auth_token, 'Content-Type': 'application/json'},
                         data=json.dumps(params))
        response = r.json().get('message')
        self.assertIn('Field update not allowed', response)

    def test_update_user_using_text_header(self):
        # tests the update functionality when data is sent in non json format
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token= str(self.generate_auth_token(username, password))
        with open('./updatedata.json') as f:
            params = json.load(f)
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers=self.get_api_headers_not_json(auth_token),
                         data=json.dumps(params))
        response = r.json().get('message')
        self.assertIn('Bad Request', response)

    def test_update_user_firstname(self):
        # tests the first name update functionality
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token = str(self.generate_auth_token(username, password))

        attr = "firstname"
        with open('./updatedata.json') as f:
            data = json.load(f)
        update_data = data["firstname"]
        params = {attr: update_data}
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers={'Token': auth_token, 'Content-Type': 'application/json'},
                             data=json.dumps(params))
        self.assertEqual(201, r.status_code)
        self.assertEqual(200, self.check_user_data_after_update(username, password, attr, update_data))


    def test_update_user_phone(self):
        # tests the phone update functionality
        with open('./user1.json') as f:
            data = json.load(f)
        username = data["username"]
        password = data["password"]
        auth_token = str(self.generate_auth_token(username, password))
        attr = "phone"
        with open('./updatedata.json') as f:
            data = json.load(f)
        update_data = data["phone"]
        params = {attr: update_data}
        r = requests.put(f'http://0.0.0.0:8080/api/users/{username}', headers={'Token': auth_token, 'Content-Type': 'application/json'},
                             data=json.dumps(params))
        self.assertEqual(201, r.status_code)
        self.assertEqual(200, self.check_user_data_after_update(username, password, attr, update_data))


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='demo_app/test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
    # unittest.main()
