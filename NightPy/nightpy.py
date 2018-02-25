import requests
import json
from .models import *


class NightPy:

    def __init__(self, token):
        self.auth_uri = 'https://api.nightbot.tv/oauth2/authorize'
        self.token_uri = 'https://api.nightbot.tv/oauth2/token'
        self.api_uri = 'https://api.nightbot.tv/1/'
        self.api_token = token
        # self.client_data = [client_id, client_secret, code]

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

        header = {'Authorization': 'Bearer {0}'.format(self.api_token)}
        try:
            if method == 'head':
                response = requests.head('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method == 'delete':
                response = requests.delete('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method == 'get':
                response = requests.get('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            elif method == 'options':
                response = requests.options('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method == 'post':
                response = requests.post('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            elif method == 'put':
                response = requests.put('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            else:
                response = None
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(json.loads(response.text)['message'])
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
            response = requests.post(self.token_uri, data=payload)
            print(response.text)
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
        return self.api_token

    '''
    Revokes token
    '''
    def revoke_token(self):
        payload = {'token': self.api_token[0]}

        try:
            response = requests.post('{0}/revoke'.format(self.token_uri), data=payload)
            if response.status_code == 200:
                print('Token has been revoked')
        except requests.HTTPError:
            print('HTTP Error occurred while trying to revoke access token.')

    # -------------------------------------------------------------------------
    # SCOPE: CHANNEL
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's channel information
    Return: Channel Resource Object
    '''
    def get_channel(self):
        data = self.api_request('channel', method='get')
        channel = data['channel']
        return Channel(channel['_id'], channel['displayName'], channel['joined'], channel['name'], channel['plan'])

    '''
    Makes Nightbot join (enter) the current user's channel
    '''
    def join_channel(self):
        self.api_request('channel/join', method='post')

    '''
    Makes Nightbot part (leave) the current user's channel
    '''
    def part_channel(self):
        self.api_request('channel/part', method='post')

    # -------------------------------------------------------------------------
    # SCOPE: CHANNEL SEND
    # -------------------------------------------------------------------------
    '''
    Makes Nightbot send a message to the channel
    '''
    def send_channel_message(self, message):
        payload = {'message': '{0}'.format(message)}
        self.api_request('channel/send', method='post', payload=payload)

    # -------------------------------------------------------------------------
    # SCOPE: COMMANDS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's custom commands list
    Return: List of Commands
    '''
    def get_custom_commands(self):
        data = self.api_request('commands', method='get')
        commands = []
        for command in data['commands']:
            item = CustomCommand(command['_id'], command['coolDown'], command['count'], command['createdAt'],
                                 command['message'], command['name'], command['updatedAt'], command['userLevel'])
            commands.append(item)
        return commands

    '''
    Adds a new custom command to the current user's channel
    Return: Command
    '''
    def add_new_custom_command(self, cool_down, message, command_name, user_level='everyone'):
        payload = {
            'coolDown': cool_down,
            'message': '{0}'.format(message),
            'name': '(0}'.format(command_name),
            'userLevel': '(0}'.format(user_level.lower())
        }
        data = self.api_request('commands', method='post', payload=payload)
        command = data['command']
        return CustomCommand(command['_id'], command['coolDown'], command['count'], command['createdAt'],
                             command['message'], command['name'], command['updatedAt'], command['userLevel'])

    '''
    Looks up a custom command by id
    Returns: Command
    '''
    def get_custom_command_by_id(self, identification):
        data = self.api_request('commands/{0}'.format(identification), method='get')
        command = data['command']
        return CustomCommand(command['_id'], command['coolDown'], command['count'], command['createdAt'],
                             command['message'], command['name'], command['updatedAt'], command['userLevel'])

    '''
    Edits a custom command by its id
    Defaults: cool_down=30, count=0, message='', name='', user_level='everyone'
    Returns: Command
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
            data = self.api_request('commands/{0}'.format(identification), method='put', payload=payload)
            command = data['command']
            return CustomCommand(command['_id'], command['coolDown'], command['count'], command['createdAt'],
                                 command['message'], command['name'], command['updatedAt'], command['userLevel'])
        else:
            return None

    '''
    Deletes a custom command by id
    '''
    def delete_custom_command_by_id(self):
        self.api_request('commands/id', method='delete')

    # -------------------------------------------------------------------------
    # SCOPE: COMMANDS DEFAULT
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's default commands list
    Returns: List of Commands
    '''
    def get_default_commands(self):
        data =  self.api_request('commands/default', method='get')
        commands = []
        for command in data['commands']:
            item = DefaultCommand(command['_name'], command['coolDown'], command['enabled'],
                                  command['name'], command['userLevel'])
            commands.append(item)
        return commands

    '''
    Looks up a default command by name
    Returns: Command
    '''
    def get_default_command_by_name(self, name):
        data = self.api_request('commands/default/{0}'.format(name), method='get')
        command = data['command']
        return DefaultCommand(command['_name'], command['coolDown'], command['enabled'],
                              command['name'], command['userLevel'])

    '''
    Edits a default command by its name
    Returns: Command
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
            data = self.api_request('commands/default/{0}'.format(name), method='put', payload=payload)
            command = data['command']
            return DefaultCommand(command['_name'], command['coolDown'], command['enabled'],
                                  command['name'], command['userLevel'])

    # -------------------------------------------------------------------------
    # SCOPE: ME
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's information
    Returns: Authorization, User
    '''
    def get_current_user(self):
        data = self.api_request('me', method='get')
        a_data = data['authorization']
        u_data = data['user']
        auth = Authorization(a_data['userLevel'], a_data['authType'], a_data['credentials'], a_data['scopes'])
        user = User(u_data['_id'], u_data['admin'], u_data['avatar'], u_data['displayName'], u_data['name'],
                    u_data['provider'], u_data['providerId'])
        return auth, user

    # -------------------------------------------------------------------------
    # SCOPE: REGULARS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's regulars list
    Return: List of Regulars
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

        data = self.api_request('regulars{0}'.format(query_parameters), method='get')
        regulars = []
        for regular in data['regulars']:
            item = Regular(regular['_id'], regular['createdAt'], regular['displayName'], regular['name'],
                           regular['provider'], regular['providerId'], regular['updatedAt'])
            regulars.append(item)
        return regulars

    '''
    Adds a new regular to the current user's channel
    Return: Regular
    '''
    def add_new_regular(self, name):
        payload = {'name': '{0}'.format(name)}

        data = self.api_request('regulars', method='post', payload=payload)
        regular = data['regular']
        return Regular(regular['_id'], regular['createdAt'], regular['displayName'], regular['name'],
                       regular['provider'], regular['providerId'], regular['updatedAt'])

    '''
    Looks up a regular by id
    Return: Regular
    '''
    def get_regular_by_id(self, identification):
        data = self.api_request('regulars/{0}'.format(identification), method='get')
        regular = data['regular']
        return Regular(regular['_id'], regular['createdAt'], regular['displayName'], regular['name'],
                       regular['provider'], regular['providerId'], regular['updatedAt'])

    '''
    Deletes a regular by id
    '''
    def delete_regular_by_id(self, identification):
        self.api_request('regulars/{0}'.format(identification), method='delete')

    # -------------------------------------------------------------------------
    # SCOPE: SONG REQUESTS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's song request settings
    Return: Song Request Settings
    '''
    def get_song_request_settings(self):
        data = self.api_request('song_requests', method='get')
        settings = data['settings']
        limits = settings['limits']
        youtube = settings['youtube']
        l_data = Limits(limits['user'], limits['playlistOnly'], limits['exemptUserLevel'])
        y_data = Youtube(youtube['limitToMusic'], youtube['limitToLikedVideos'])

        return SongRequest(settings['enabled'], l_data, settings['playlist'], settings['providers'],
                           settings['searchProvider'], settings['userLevel'], settings['volume'], y_data)

    '''
    Edits the song request settings
    Return: Song Request Setting
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
        data = self.api_request('song_requests', method='put', payload=payload)
        settings = data['settings']
        limits = settings['limits']
        youtube = settings['youtube']
        l_data = Limits(limits['user'], limits['playlistOnly'], limits['exemptUserLevel'])
        y_data = Youtube(youtube['limitToMusic'], youtube['limitToLikedVideos'])

        return SongRequest(settings['enabled'], l_data, settings['playlist'], settings['providers'],
                           settings['searchProvider'], settings['userLevel'], settings['volume'], y_data)

    # -------------------------------------------------------------------------
    # SCOPE: SONG REQUESTS PLAYLIST
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's song request playlist
    Return: List of PlaylistItems
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

        data = self.api_request('song_requests/playlist{0}'.format(query_parameters), method='get')
        playlists = []
        for playlist in data['playlist']:
            track = playlist['track']
            t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                           track['title'], track['url'])
            item = PlaylistItem(playlist['_id'], playlist['createdAt'], t_data, playlist['updatedAt'])
            playlists.append(item)
        return playlists

    '''
    Adds a new playlist item to the current user’s channel.
    Return: PlaylistItem
    '''
    def add_playlist_item(self, query):
        payload = {'q': query}

        data = self.api_request('song_requests/playlist', method='post', payload=payload)
        playlist = data['item']
        track = playlist['track']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        return PlaylistItem(playlist['_id'], playlist['createdAt'], t_data, playlist['updatedAt'])

    '''
    Deletes all playlist items
    '''
    def clear_playlist(self):
        self.api_request('song_requests/playlist', method='delete')

    '''
    Imports a remote playlist to the current user’s channel.
    '''
    def import_remote_playlist(self, url):
        payload = {'url': url}

        self.api_request('song_requests/playlist/import', method='post', payload=payload)

    '''
    Looks up a song request playlist item by id
    Return: PlaylistItem
    '''
    def get_playlist_item_by_id(self, identification):
        data = self.api_request('song_requests/playlist/{0}'.format(identification), method='get')
        playlist = data['item']
        track = playlist['track']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        return PlaylistItem(playlist['_id'], playlist['createdAt'], t_data, playlist['updatedAt'])

    '''
    Deletes a song requests playlist item by id
    '''
    def delete_playlist_item_by_id(self, identification):
        self.api_request('song_requests/playlist/{0}'.format(identification), method='delete')

    # -------------------------------------------------------------------------
    # SCOPE: SONG REQUESTS QUEUE
    # -------------------------------------------------------------------------
    '''
    Gets the current API user’s current song
    Return: QueueItem
    '''
    def get_current_song(self):
        data = self.api_request('song_requests/queue', method='get')
        song = data['_currentSong']
        track = song['track']
        user = song['user']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
        return QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])

    '''
    Gets the current API user’s song request queue
    Return: List of QueueItem
    '''
    def get_queue(self):
        data = self.api_request('song_requests/queue', method='get')
        queued = []
        for song in data['queue']:
            track = song['track']
            user = song['user']
            t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                           track['title'], track['url'])
            u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
            item = QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])
            queued.append(item)
        return queued

    '''
    Adds a new queue item to the current user’s channel.
    Return: QueueItem
    '''
    def add_new_queue_item(self, query):
        payload = {'q': query}

        data = self.api_request('song_requests/queue', method='post', payload=payload)
        song = data['item']
        track = song['track']
        user = song['user']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
        return QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])

    '''
    Deletes all queue items
    '''
    def clear_queue(self):
        self.api_request('song_requests/queue', method='delete')

    '''
    Plays the current playing queue item in the current user’s channel.
    Return: QueueItem
    '''
    def play_current_queue_item(self):
        data = self.api_request('song_requests/queue/play', method='post')
        song = data['item']
        track = song['track']
        user = song['user']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
        return QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])

    '''
    Pauses the current playing queue item in the current user’s channel.
    Return: QueueItem
    '''
    def pause_current_queue_item(self):
        data = self.api_request('song_requests/queue/pause', method='post')
        song = data['item']
        track = song['track']
        user = song['user']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
        return QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])

    '''
    Skips the current playing queue item in the current user’s channel.
    Return: QueueItem
    '''
    def skip_current_queue_item(self):
        data = self.api_request('song_requests/queue/skip', method='post')
        song = data['item']
        track = song['track']
        user = song['user']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
        return QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])

    '''
    Looks up a song request queue item by id
    Return: QueueItem
    '''
    def get_queue_item_by_id(self, identification):
        data = self.api_request('song_requests/queue/{0}'.format(identification), method='get')
        song = data['item']
        track = song['track']
        user = song['user']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
        return QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])

    '''
    Deletes a song requests queue item by id
    '''
    def delete_queue_item_by_id(self, identification):
        self.api_request('song_requests/queue/{0}'.format(identification), method='delete')

    '''
    Promotes a queue item to the front of the queue
    Return: QueueItem
    '''
    def promote_queue_item(self, identification):
        data = self.api_request('song_requests/queue/{0}/promote'.format(identification), method='post')
        song = data['item']
        track = song['track']
        user = song['user']
        t_data = Track(track['artist'], track['duration'], track['provider'], track['providerId'],
                       track['title'], track['url'])
        u_data = User(None, None, None, user['displayName'], user['name'], user['provider'], user['providerId'])
        return QueueItem(song['_id'], song['createdAt'], t_data, u_data, song['updatedAt'])

    # -------------------------------------------------------------------------
    # SCOPE: SPAM PROTECTION
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's spam protection filters list
    Return: List of Filters
    '''
    def get_filters(self):
        data = self.api_request('spam_protection', method='get')
        filters = []
        for filter_data in data['filters']:
            if 'limit' not in filter_data:
                filter_data['limit'] = None
            if '_limitMin' not in filter_data:
                filter_data['_limitMin'] = None
            if '_limitMax' not in filter_data:
                filter_data['_limitMax'] = None
            if 'blacklist' not in filter_data:
                filter_data['blacklist'] = None
            if 'whitelist' not in filter_data:
                filter_data['whitelist'] = None
            item = Filter(filter_data['_name'], filter_data['_type'], filter_data['enabled'],
                          filter_data['exemptUserLevel'], filter_data['length'], filter_data['message'],
                          filter_data['silent'], limit=filter_data['limit'], limit_min=filter_data['_limitMin'],
                          limit_max=filter_data['_limitMax'], blacklist=filter_data['blacklist'],
                          whitelist=filter_data['whitelist'])
            filters.append(item)
        return filters

    '''
    Looks up a spam protection filter by type
    Return: Filter
    '''
    def get_filter_by_type(self, filter_type):
        data = self.api_request('spam_protection/{0}'.format(filter_type), method='get')
        filter_data = data['filter']
        if 'limit' not in filter_data:
            filter_data['limit'] = None
        if '_limitMin' not in filter_data:
            filter_data['_limitMin'] = None
        if '_limitMax' not in filter_data:
            filter_data['_limitMax'] = None
        if 'blacklist' not in filter_data:
            filter_data['blacklist'] = None
        if 'whitelist' not in filter_data:
            filter_data['whitelist'] = None
        return Filter(filter_data['_name'], filter_data['_type'], filter_data['enabled'],
                      filter_data['exemptUserLevel'], filter_data['length'], filter_data['message'],
                      filter_data['silent'], limit=filter_data['limit'], limit_min=filter_data['_limitMin'],
                      limit_max=filter_data['_limitMax'], blacklist=filter_data['blacklist'],
                      whitelist=filter_data['whitelist'])

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
            data = self.api_request('spam_protection/{0}'.format(filter_type), method='put', payload=payload)
            filter_data = data['filter']
            if 'limit' not in filter_data:
                filter_data['limit'] = None
            if '_limitMin' not in filter_data:
                filter_data['_limitMin'] = None
            if '_limitMax' not in filter_data:
                filter_data['_limitMax'] = None
            if 'blacklist' not in filter_data:
                filter_data['blacklist'] = None
            if 'whitelist' not in filter_data:
                filter_data['whitelist'] = None
            return Filter(filter_data['_name'], filter_data['_type'], filter_data['enabled'],
                          filter_data['exemptUserLevel'], filter_data['length'], filter_data['message'],
                          filter_data['silent'], limit=filter_data['limit'], limit_min=filter_data['_limitMin'],
                          limit_max=filter_data['_limitMax'], blacklist=filter_data['blacklist'],
                          whitelist=filter_data['whitelist'])
        else:
            return None

    # -------------------------------------------------------------------------
    # SCOPE: SUBSCRIBERS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's subscribers list
    Return: List of Subscribers
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

        data = self.api_request('subscribers{0}'.format(query_parameters), method='get')
        subscribers = []
        for subscriber in data['subscribers']:
            item = Subscribers(subscriber['_id'], subscriber['createdAt'], subscriber['displayName'],
                               subscriber['name'], subscriber['provider'], subscriber['providerId'],
                               subscriber['uploadedAt'])
            subscribers.append(item)
        return subscribers

    '''
    Adds a new subscriber to the current user's channel
    Return: Subscriber
    '''
    def add_new_subscriber(self, name):
        payload = {'name': '{0}'.format(name)}
        data = self.api_request('subscribers', method='post', payload=payload)
        subscriber = data['subscriber']
        return Subscribers(subscriber['_id'], subscriber['createdAt'], subscriber['displayName'], subscriber['name'],
                           subscriber['provider'], subscriber['providerId'], subscriber['uploadedAt'])

    '''
    Looks up a subscriber by id
    Return: Subscriber
    '''
    def get_subscriber_by_id(self, identification):
        data = self.api_request('subscribers/{0}'.format(identification), method='get')
        subscriber = data['subscriber']
        return Subscribers(subscriber['_id'], subscriber['createdAt'], subscriber['displayName'], subscriber['name'],
                           subscriber['provider'], subscriber['providerId'], subscriber['uploadedAt'])

    '''
    Deletes a subscriber by id
    '''
    def delete_subscriber_by_id(self, identification):
        self.api_request('subscribers/{0}'.format(identification), method='delete')

    # -------------------------------------------------------------------------
    # SCOPE: TIMERS
    # -------------------------------------------------------------------------
    '''
    Gets the current API user's timers list
    Return: List of Timers
    '''
    def get_timers(self):
        data = self.api_request('timers', method='get')
        timers = []
        for timer in data['timers']:
            item = Timers(timer['_id'], timer['createdAt'], timer['enabled'], timer['interval'], timer['lines'],
                          timer['message'], timer['name'], timer['nextRunAt'], timer['uploadedAt'])
            timers.append(item)
        return timers

    '''
    Adds a new timer to the current user's channel
    Return: Timer
    '''
    def add_new_timer(self, interval, lines, message, name, enabled=True):
        payload = {
            'enabled': str(enabled).lower(),
            'interval': '{0}'.format(interval),
            'lines': '{0}'.format(lines),
            'message': '{0}'.format(message),
            'name': '{0}'.format(name)
        }

        data = self.api_request('timers', method='post', payload=payload)
        timer = data['command']
        return Timers(timer['_id'], timer['createdAt'], timer['enabled'], timer['interval'], timer['lines'],
                      timer['message'], timer['name'], timer['nextRunAt'], timer['uploadedAt'])

    '''
    Looks up a timer by id
    Return: Timer
    '''
    def get_timer_by_id(self, identification):
        data = self.api_request('timers/{0}'.format(identification), method='get')
        timer = data['timer']
        return Timers(timer['_id'], timer['createdAt'], timer['enabled'], timer['interval'], timer['lines'],
                      timer['message'], timer['name'], timer['nextRunAt'], timer['uploadedAt'])

    '''
    Edits a timer by its id
    Return: Timer
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
            data = self.api_request('timers/{0}'.format(identification), method='put', payload=payload)
            timer = data['timer']
            return Timers(timer['_id'], timer['createdAt'], timer['enabled'], timer['interval'], timer['lines'],
                          timer['message'], timer['name'], timer['nextRunAt'], timer['uploadedAt'])
        else:
            return None

    '''
    Deletes a timer by id
    '''
    def delete_timer_by_id(self, identification):
        self.api_request('timers/{0}'.format(identification), method='delete')
