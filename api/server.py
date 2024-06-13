import requests
from requests.adapters import HTTPAdapter, Retry

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
        self.session = requests.Session()
        self.session.headers = {'Authorization': f'Bearer {token}'}
        self.retries = Retry(total=5,backoff_factor=2)
        self.session.mount('https://', HTTPAdapter(max_retries=self.retries))


    def set_token(self, token):
        self.token = token
        self.session.headers = {'Authorization': f'Bearer {token}'}

    def _match_route(self):
        return f'{self.base_url}/match'
    
    def _user_route(self):
        return f'{self.base_url}/user'

    def _handle_response(self, response: requests.Response):
        try:
            response.raise_for_status()
            if not response.content or response.content in [b'', b'null']:
                return None
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"Error: {response.status_code}. {err}")
            return None
        except ValueError as err:
            # Handle JSON decode error
            print(f"JSON decode error: {err}")
            return None
        
# 
# User
# 

    def get_user(self):
        url = f'{self._user_route()}'
        response = self.session.get(url)
        return self._handle_response(response)
    
    def set_username(self, name):
        url = f'{self._user_route()}/rename/'
        data = {
            'name': name
        }
        response = self.session.post(url, json=data)
        return self._handle_response(response)

#
# Matches
#

    def join_match(self):
        url = f'{self._match_route()}/join'
        response = self.session.post(url)
        return self._handle_response(response)
    
    def cancel_match(self):
        url = f'{self._match_route()}/cancel'
        response = self.session.delete(url)
        return self._handle_response(response)
    
    def get_user_matches(self):
        url = f'{self._match_route()}/user'
        response = self.session.get(url)
        return self._handle_response(response)
    
    def get_match_info(self, id):
        url = f'{self._match_route()}/info/{id}'
        response = self.session.get(url)
        return self._handle_response(response)

    def get_match(self, id):
        """
        Get a match by its ID.

        :param id: The ID of the match to retrieve.
        :return: The match data.
        """
        url = f'{self._match_route()}/{id}'
        response = self.session.get(url)
        return self._handle_response(response)

    def get_match_inst(self, id, order):
        url = f'{self._match_route()}/inst/{id}'
        data = {
            'order': order
        }
        response = self.session.get(url, json=data)
        return self._handle_response(response)

    def send_message(self, match_id: str, message: str):
        url = f'{self._match_route()}/sendmsg'
        data = {
            'matchId': match_id,
            'message': message
        }
        response = self.session.post(url, json=data)
        return self._handle_response(response)

    def end_match(self, match_id):
        url = f'{self._match_route()}/end'
        data = {
            'matchId': match_id,
        }
        response = self.session.post(url, json=data)
        return self._handle_response(response)