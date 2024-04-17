import requests

class Server:
    '''
    ### Example usage:
        ```python
            base_url = 'http://your-nestjs-server-url'
            bearer_token = 'your-bearer-token'

            api = Server(base_url, bearer_token)
        ```
    '''
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}

    def set_token(self, token):
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}

    def _match_route(self):
        return f'{self.base_url}/match'
    
    def _user_route(self):
        return f'{self.base_url}/user'

    def _handle_response(self, response: requests.Response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"Error: {response.status_code}. {err}")
            return None
        
# 
# 
# 

    def set_username(self, name):
        url = f'{self._user_route()}/rename/'
        data = {
            'name': name
        }
        response = requests.post(url, json=data, headers=self.headers)
        return self._handle_response(response)


    def get_user_matches(self):
        url = f'{self._match_route()}/user'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)
    
    def get_match_info(self, id):
        url = f'{self._match_route()}/info/{id}'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_match(self, id):
        """
        Get a match by its ID.

        :param id: The ID of the match to retrieve.
        :return: The match data.
        """
        url = f'{self._match_route()}/{id}'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_match_inst(self, id, order):
        url = f'{self._match_route()}/inst/{id}'
        data = {
            'order': order
        }
        response = requests.get(url, json=data, headers=self.headers)
        return self._handle_response(response)

    def send_message(self, match_id: str, message: str):
        url = f'{self._match_route()}/sendmsg'
        data = {
            'matchId': match_id,
            'message': message
        }
        response = requests.post(url, json=data, headers=self.headers)
        return self._handle_response(response)

