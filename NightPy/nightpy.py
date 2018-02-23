import requests
import json


class NightPy:

    def __init__(self, client_id, client_secret, code):
        self.token_uri = 'https://api.nightbot.tv/oauth2/token'
        self.api_uri = 'https://api.nightbot.tv/1/'
        self.api_token = self.create_token(client_id, client_secret, code)
        self.client_data = [client_id, client_secret, code]

    '''
    Create token from client_id, client_secret, code
    '''
    def create_token(self, identification, secret, code):
        payload = {
            'client_id': identification,
            'client_secret': secret,
            'grant_type': 'authorization_code',
            'redirect_uri': '',
            'code': code
        }
        try:
            response = requests.post(self.token_uri, payload=payload)
            if response.status_code == 200:
                token_data = json.loads(response.text)
                return [token_data['access_token'], token_data['refresh_token']]
            else:
                return None
        except requests.HTTPError:
            print('HTTP Error occurred while trying to generate access token.')
            return None

    '''
    Returns API user's access token
    '''
    def get_access_token(self):
        return self.api_token[0]

    '''
    Returns API user's refresh token
    '''
    def get_refresh_token(self):
        return self.api_token[1]

    '''
    Generates a new token from old token
    '''
    def refresh_token(self, redirect_uri):
        payload = {
            'client_id': self.client_data[0],
            'client_secret': self.client_data[1],
            'grant_type': 'refresh_token',
            'redirect_uri': redirect_uri,
            'refresh_token': self.api_token[1]
        }

        try:
            response = requests.post(self.token_uri, payload=payload)
            if response.status_code == 200:
                token_data = json.loads(response.text)
                self.api_token = [token_data['access_token'], token_data['refresh_token']]
                return [token_data['access_token']]
            else:
                return None
        except requests.HTTPError:
            print('HTTP Error occurred while trying to refresh access token.')
            return None

    '''
    Request Nightbot API
    '''
    def api_request(self, endpoint, method='get', payload=None):
        method = method.lower()
        
        if payload is None:
            payload = ''

        header = 'Authorization: Bearer {0}'.format(self.api_token[0])
        try:
            if method is 'head':
                response = requests.head('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method is 'delete':
                response = requests.delete('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method is 'get':
                response = requests.get('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            elif method is 'options':
                response = requests.options('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method is 'post':
                response = requests.post('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            elif method is 'put':
                response = requests.put('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            else:
                response = None

            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return None

        except requests.HTTPError:
            print('HTTP Error occurred while trying to make request to Nightbot API.')
            return None

    # -------------------------------------------------------------------------
    # SCOPE: SONG REQUESTS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's song request settings
    '''
    def get_song_request_settings(self):
        return self.api_request('song_requests', method='get')

    '''
    Edits the song request settings
    '''
    def edit_song_request_settings(self, enabled=True, queue_limit=100, user_limits=100, playlist_only=True,
                                   exempt_user_level='everyone', playlist=None, providers=None, search_provider=None,
                                   request_user_level='everyone', volume=100, youtube_limit_to_music=True,
                                   youtube_limit_to_liked=True):

        if playlist is None:
            playlist = 'channel'
        if providers is None:
            providers = {}
        if search_provider is None:
            search_provider = ''

        payload = {
            'enabled': str(enabled).lower(),
            'limits': {
                'queue': queue_limit,
                'user': user_limits,
                'playlistOnly': str(playlist_only).lower(),
                'exemptUserLevel': exempt_user_level.lower(),
            },
            'playlist': playlist,
            'providers': json.dumps(providers),
            'searchProvider': search_provider,
            'userLevel': request_user_level,
            'volume': volume,
            'youtube': {
                'limitToMusic': str(youtube_limit_to_music).lower(),
                'limitToLikedVideos': str(youtube_limit_to_liked).lower()
            }

        }
        return self.api_request('song_requests', method='put', payload=payload)

    '''
    Gets the current API user's song request playlist
    '''
    def get_playlist(self, direction='desc', limit=100, offset=0, query='', sort_by='date'):

        payload = {
            'direction': direction.lower(),
            'limit': limit,
            'offset': offset,
            'q': query,
            'sort_by': sort_by
        }

        return self.api_request('song_requests/playlist', method='get', payload=payload)

    '''
    Adds a new playlist item to the current user’s channel.
    '''
    def add_playlist_item(self, query):
        payload = {'q': query}

        return self.api_request('song_requests/playlist', method='post', payload=payload)

    '''
    Deletes all playlist items
    '''
    def clear_playlist(self):
        return self.api_request('song_requests/playlist', method='delete')

    '''
    Imports a remote playlist to the current user’s channel.
    '''
    def import_remote_playlist(self, url):
        payload = {'url': url}

        return self.api_request('song_requests/playlist/import', method='post', payload=payload)

    '''
    Looks up a song request playlist item by id
    '''
    def get_playlist_item_by_id(self, identification):
        return self.api_request('song_requests/playlist/:{0}'.format(identification), method='get')

    '''
    Deletes a song requests playlist item by id
    '''
    def delete_playlist_item_by_id(self, identification):
        return self.api_request('song_requests/playlist/:{0}'.format(identification), method='delete')

    '''
    Gets the current API user’s song request queue
    '''
    def get_queue(self):
        return self.api_request('song_requests/queue', method='get')

    '''
    Adds a new queue item to the current user’s channel.
    '''
    def add_new_queue_item(self, query):
        payload = {'q': query}

        return self.api_request('song_requests/queue', method='post', payload=payload)

    '''
    Deletes all queue items
    '''
    def clear_queue(self):
        return self.api_request('song_requests/queue', method='delete')

    '''
    Skips the current playing queue item in the current user’s channel.
    '''
    def skip_current_queue_item(self):
        return self.api_request('song_requests/queue/skip', method='post')

    '''
    Looks up a song request queue item by id
    '''
    def get_queue_item_by_id(self, identification):
        return self.api_request('song_requests/queue/:{0}'.format(identification), method='get')

    '''
    Deletes a song requests queue item by id
    '''
    def delete_queue_item_by_id(self, identification):
        return self.api_request('song_requests/queue/:{0}'.format(identification), method='delete')

    '''
    Promotes a queue item to the front of the queue
    '''
    def promote_queue_item(self, identification):
        return self.api_request('song_requests/queue/:{0}/promote'.format(identification), method='post')
