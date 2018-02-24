# API Scope Resource Objects


class Channel:
    def __init__(self, unique_id, display_name, joined, name, plan):
        self.id = unique_id
        self.display_name = display_name
        if joined.lower() == 'true':
            self.joined = True
        else:
            self.joined = False
        self.name = name
        self.plan = plan


class CustomCommand:
    def __init__(self, unique_id, cool_down, count, created_at, message, command_name, updated_at, user_level):
        self.id = unique_id
        self.cool_down = cool_down
        self.count = count
        self.created_at = created_at
        self.message = message
        self.command_name = command_name
        self.updated_at = updated_at
        self.user_level = user_level


class DefaultCommand:
    def __init__(self, unique_name, cool_down, enabled, command_name, user_level):
        self.name = unique_name
        self.cool_down = cool_down
        if enabled.lower() == 'true':
            self.enabled = True
        else:
            self.enabled = False
        self.command_name = command_name
        self.user_level = user_level


class Authorization:
    def __init__(self, user_level, auth_type, credentials, scopes):
        self.user_level = user_level
        self.auth_type = auth_type
        self.credentials = credentials
        self.scopes = scopes


class User:
    def __init__(self, user_id, admin, avatar, display_name, name, provider, provider_id):
        self.id = user_id
        self.admin = admin
        self.avatar = avatar
        self.display_name = display_name
        self.name = name
        self.provider = provider
        self.provider_id = provider_id


class Regular:
    def __init__(self, regular_id, created_at, display_name, name, provider, provider_id, updated_at):
        self.id = regular_id
        self.created_at = created_at
        self.display_name = display_name
        self.name = name
        self.provider = provider
        self.provider_id = provider_id
        self.updated_at = updated_at


class Limits:
    def __init__(self, user, playlist_only, exempt_user_level):
        self.user = user

        if playlist_only.lower() == 'true':
            self.playlist_only = True
        else:
            self.playlist_only = False
        if exempt_user_level.lower() == 'true':
            self.exempt_user_level = True
        else:
            self.exempt_user_level = False


class Youtube:
    def __init__(self, limit_to_music, limit_to_liked_videos):
        if limit_to_music.lower() == 'true':
            self.limit_to_music = True
        else:
            self.limit_to_music = False
        if limit_to_liked_videos.lower() == 'true':
            self.limit_to_liked_videos = True
        else:
            self.limit_to_liked_videos = False


class SongRequest:
    def __init__(self, enabled, limits,  playlist, providers, search_provider, user_level, volume, youtube):
        if enabled.lower() == 'true':
            self.enabled = True
        else:
            self.enabled = False
        self.limits = limits
        self.playlist = playlist
        self.providers = providers
        self.search_provider = search_provider
        self.user_level = user_level
        self.volume = volume
        self.youtube = youtube


class Track:
    def __init__(self, artist, duration, provider, provider_id, title, url):
        self.artist = artist
        self.duration = duration
        self.provider = provider
        self.provider_id = provider_id
        self.title = title
        self.url = url


class PlaylistItem:
    def __init__(self, item_id, created_at, track, updated_at):
        self.id = item_id
        self.created_at = created_at
        self.track = track
        self.updated_at = updated_at


class QueueItem:
    def __init__(self, queue_id, created_at, track, user, updated_at):
        self.id = queue_id
        self.created_at = created_at
        self.track = track
        self.user = user
        self.updated_at = updated_at


class Filter:
    def __init__(self, name, filter_type, enabled, exempt_user_level, length, message, silent,
                 limit=None, limit_min=None, limit_max=None, blacklist=None, whitelist=None):
        self.name = name
        self.type = filter_type
        if enabled.lower() == 'true':
            self.enabled = True
        else:
            self.enabled = False
        self.exempt_user_level = exempt_user_level
        self.length = length
        self.message = message
        if silent.lower() == 'true':
            self.silent = True
        else:
            self.silent = False
        # Optional
        self.limit = limit
        self.limit_min = limit_min
        self.limit_max = limit_max
        self.blacklist = blacklist
        self.whitelist = whitelist


class Subscribers:
    def __init__(self, subscriber_id, created_at, display_name, name, provider, provider_id, updated_at):
        self.id = subscriber_id
        self.created_at = created_at
        self.display_name = display_name
        self.name = name
        self.provider = provider
        self.provider_id = provider_id
        self.updated_at = updated_at


class Timers:
    def __init__(self, timer_id, created_at, enabled, interval, lines, message, name, next_run_at, updated_at):
        self.id = timer_id
        self.created_at = created_at
        if enabled.lower() == 'true':
            self.enabled = True
        else:
            self.enabled = False
        self.interval = interval
        self.lines = lines
        self.message = message
        self.name = name
        self.next_run_at = next_run_at
        self.updated_at = updated_at
