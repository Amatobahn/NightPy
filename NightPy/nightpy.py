import requests
import json


class NightPy:

    def __init__(self, client_id, client_secret, code):
        self.auth_uri = 'https://api.nightbot.tv/oauth2/authorize'
        self.token_uri = 'https://api.nightbot.tv/oauth2/token'
        self.api_uri = 'https://api.nightbot.tv/1/'
        self.api_token = self.create_token(client_id, client_secret, code)
        self.client_data = [client_id, client_secret, code]

    # -------------------------------------------------------------------------
    # NIGHTBOT API
    # -------------------------------------------------------------------------
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
    # OAUTH2
    # -------------------------------------------------------------------------
    '''
    Create token from client_id, client_secret, code
    '''
    def create_token(self, client_id, client_secret, redirect_uri, code):
        payload = {
            'client_id': '{0}'.format(client_id),
            'client_secret': '{0}'.format(client_secret),
            'grant_type': 'authorization_code',
            'redirect_uri': '{0}'.format(redirect_uri),
            'code': '{0}'.format(code)
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
    Revokes token
    '''
    def revoke_token(self):
        payload = {'token': self.api_token[0]}

        try:
            response = requests.post('{0}/revoke'.format(self.token_uri), payload=payload)
            if response.status_code == 200:
                print('Token has been revoked')
        except requests.HTTPError:
            print('HTTP Error occurred while trying to revoke access token.')

    # -------------------------------------------------------------------------
    # SCOPE: CHANNEL
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's channel information
    '''
    def get_channel(self):
        return self.api_request('channel', method='get')

    '''
    Makes Nightbot join (enter) the current user's channel
    '''
    def join_channel(self):
        return self.api_request('channel/join', method='post')

    '''
    Makes Nightbot part (leave) the current user's channel
    '''
    def part_channel(self):
        return self.api_request('channel/part', method='post')

    # -------------------------------------------------------------------------
    # SCOPE: CHANNEL SEND
    # -------------------------------------------------------------------------
    '''
    Makes Nightbot send a message to the channel
    '''
    def send_channel_message(self, message):
        payload = {'message': '{0}'.format(message)}
        return self.api_request('channel/send', method='post', payload=payload)

    # -------------------------------------------------------------------------
    # SCOPE: COMMANDS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's custom commands list
    '''
    def get_custom_commands(self):
        return self.api_request('commands', method='get')

    '''
    Adds a new custom command to the current user's channel
    '''
    def add_new_custom_command(self, cool_down, message, command_name, user_level='everyone'):
        payload = {
            'coolDown': cool_down,
            'message': '{0}'.format(message),
            'name': '(0}'.format(command_name),
            'userLevel': '(0}'.format(user_level.lower())
        }
        return self.api_request('commands', method='post', payload=payload)

    '''
    Looks up a custom command by id
    '''
    def get_custom_command_by_id(self, identification):
        return self.api_request('commands/{0}'.format(identification), method='get')

    '''
    Edits a custom command by its id
    Defaults: cool_down=30, count=0, message='', name='', user_level='everyone'
    '''
    def edit_custom_command_by_id(self, identification,
                                  cool_down=None, count=None, message=None, name=None, user_level=None):
        payload = {}

        if cool_down is not None:
            payload['coolDown'] = cool_down
        if count is not None:
            payload['count'] = count
        if message is not None:
            payload['message'] = '{0}'.format(message)
        if name is not None:
            payload['name'] = '{0}'.format(name)
        if user_level is not None:
            payload['userLevel'] = '{0}'.format(user_level)

        if len(payload) > 0:
            return self.api_request('commands/{0}'.format(identification), method='put', payload=payload)
        else:
            return None

    '''
    Deletes a custom command by id
    '''
    def delete_custom_command_by_id(self):
        return self.api_request('commands/id', method='delete')

    # -------------------------------------------------------------------------
    # SCOPE: COMMANDS DEFAULT
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's default commands list
    '''
    def get_default_commands(self):
        return self.api_request('commands/default', method='get')

    '''
    Looks up a default command by name
    '''
    def get_default_command_by_name(self, name):
        return self.api_request('commands/default/{0}'.format(name), method='get')

    '''
    Edits a default command by its name
    '''
    def edit_default_command_by_name(self, name, cool_down=None, enabled=None, user_level=None):
        payload = {}

        if cool_down is not None:
            payload['coolDown'] = cool_down
        if enabled is not None:
            payload['enabled'] = str(enabled).lower()
        if user_level is not None:
            payload['userLevel'] = '{0}'.format(user_level)

        if len(payload) > 0:
            return self.api_request('commands/default/{0}'.format(name), method='put', payload=payload)

    # -------------------------------------------------------------------------
    # SCOPE: ME
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's information
    '''
    def get_current_user(self):
        return self.api_request('me', method='get')

    # -------------------------------------------------------------------------
    # SCOPE: REGULARS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's regulars list
    '''
    def get_regulars(self, limit=None, offset=None, query=None):
        query_parameters = ''

        if limit is not None:
            if limit > 100:
                limit = 100
            if limit < 1:
                limit = 1
            query_parameters += '&limit={0}'.format(limit)
        if offset is not None:
            query_parameters += '&offset={0}'.format(offset)
        if query is not None:
            query_parameters += '&query={0}'.format(query)
        if len(query_parameters) > 0:
            query_parameters = '?{0}'.format(query_parameters[1:])

        return self.api_request('regulars{0}'.format(query_parameters), method='get')

    '''
    Adds a new regular to the current user's channel
    '''
    def add_new_regular(self, name):
        payload = {'name': '{0}'.format(name)}

        return self.api_request('regulars', method='post', payload=payload)

    '''
    Looks up a regular by id
    '''
    def get_regular_by_id(self, identification):
        return self.api_request('regulars/{0}'.format(identification), method='get')

    '''
    Deletes a regular by id
    '''
    def delete_regular_by_id(self, identification):
        return self.api_request('regulars/{0}'.format(identification), method='delete')

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

    # -------------------------------------------------------------------------
    # SCOPE: SONG REQUESTS PLAYLIST
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's song request playlist
    '''
    def get_playlist(self, direction=None, limit=None, offset=None, query=None, sort_by=None):
        query_parameters = ''

        if direction is not None:
            query_parameters += '&direction={0}'.format(direction)
        if limit is not None:
            query_parameters += '&limit={0}'.format(limit)
        if offset is not None:
            query_parameters += '&offset={0}'.format(offset)
        if query is not None:
            query_parameters += '&q={0}'.format(query)
        if sort_by is not None:
            query_parameters += '&sort_by={0}'.format(sort_by)

        if len(query_parameters) > 0:
            query_parameters = '?{0}'.format(query_parameters[1:])

        return self.api_request('song_requests/playlist{0}'.format(query_parameters), method='get')

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
        return self.api_request('song_requests/playlist/{0}'.format(identification), method='get')

    '''
    Deletes a song requests playlist item by id
    '''
    def delete_playlist_item_by_id(self, identification):
        return self.api_request('song_requests/playlist/{0}'.format(identification), method='delete')

    # -------------------------------------------------------------------------
    # SCOPE: SONG REQUESTS QUEUE
    # -------------------------------------------------------------------------
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
        return self.api_request('song_requests/queue/{0}'.format(identification), method='get')

    '''
    Deletes a song requests queue item by id
    '''
    def delete_queue_item_by_id(self, identification):
        return self.api_request('song_requests/queue/{0}'.format(identification), method='delete')

    '''
    Promotes a queue item to the front of the queue
    '''
    def promote_queue_item(self, identification):
        return self.api_request('song_requests/queue/{0}/promote'.format(identification), method='post')

    # -------------------------------------------------------------------------
    # SCOPE: SPAM PROTECTION
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's spam protection filters list
    '''
    def get_filters(self):
        return self.api_request('spam_protection', method='get')

    '''
    Looks up a spam protection filter by type
    '''
    def get_filter_by_type(self, filter_type):
        return self.api_request('spam_protection/{0}'.format(filter_type), method='get')

    '''
    Edits a spam protection filter by its type
    '''
    def edit_filter_by_type(self, filter_type, blacklist=None, enabled=None, exempt_user_level=None, length=None,
                            limit=None, message=None, silent=None, whitelist=None):
        payload = {}
        if blacklist is not None:
            payload['blacklist'] = '{0}'.format(blacklist)
        if enabled is not None:
            payload['enabled'] = str(enabled).lower()
        if exempt_user_level is not None:
            payload['exemptUserLevel'] = '{0}'.format(exempt_user_level)
        if length is not None:
            payload['length'] = length
        if limit is not None:
            payload['limit'] = limit
        if message is not None:
            payload['message'] = '{0}'.format(message)
        if silent is not None:
            payload['silent'] = str(silent).lower()
        if whitelist is not None:
            payload['whitelist'] = '{0}'.format(whitelist)

        if len(payload) > 0:
            return self.api_request('spam_protection/{0}'.format(filter_type), method='put', payload=payload)
        else:
            return None

    # -------------------------------------------------------------------------
    # SCOPE: SUBSCRIBERS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's subscribers list
    '''
    def get_subscribers(self, limit=None, offset=None, display_name=None):
        query_parameters = ''

        if limit is not None:
            query_parameters += '&limit={0}'.format(limit)
        if offset is not None:
            query_parameters += '&offset={0}'.format(offset)
        if display_name is not None:
            query_parameters += '&q={0}'.format(display_name)
        if len(query_parameters) > 0:
            query_parameters = '?{0}'.format(query_parameters[1:])

        return self.api_request('subscribers{0}'.format(query_parameters), method='get')

    '''
    Adds a new subscriber to the current user's channel
    '''
    def add_new_subscriber(self, name):
        payload = {'name': '{0}'.format(name)}
        return self.api_request('subscribers', method='post', payload=payload)

    '''
    Looks up a subscriber by id
    '''
    def get_subscriber_by_id(self, identification):
        return self.api_request('subscribers/{0}'.format(identification), method='get')

    '''
    Deletes a subscriber by id
    '''
    def delete_subscriber_by_id(self, identification):
        return self.api_request('subscribers/{0}'.format(identification), method='delete')

    # -------------------------------------------------------------------------
    # SCOPE: TIMERS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's timers list
    '''
    def get_timers(self):
        return self.api_request('timers', method='get')

    '''
    Adds a new timer to the current user's channel
    '''
    def add_new_timer(self, interval, lines, message, name, enabled=True):
        payload = {
            'enabled': str(enabled).lower(),
            'interval': '{0}'.format(interval),
            'lines': '{0}'.format(lines),
            'message': '{0}'.format(message),
            'name': '{0}'.format(name)
        }

        return self.api_request('timers', method='post', payload=payload)

    '''
    Looks up a timer by id
    '''
    def get_timer_by_id(self, identification):
        return self.api_request('timers/{0}'.format(identification), method='get')

    '''
    Edits a timer by its id
    '''
    def edit_timer_by_id(self, identification, interval=None, lines=None, message=None, name=None, enabled=None):
        payload = {}

        if interval is not None:
            payload['interval'] = '{0}'.format(interval)
        if lines is not None:
            payload['lines'] = '{0}'.format(lines)
        if message is not None:
            payload['message'] = '{0}'.format(message)
        if name is not None:
            payload['name'] = '{0}'.format(name)
        if enabled is not None:
            payload['enabled'] = '{0}'.format(enabled).lower()

        if len(payload) > 0:
            return self.api_request('timers/{0}'.format(identification), method='put', payload=payload)
        else:
            return None

    '''
    Deletes a timer by id
    '''
    def delete_timer_by_id(self, identification):
        return self.api_request('timers/{0}'.format(identification), method='delete')
