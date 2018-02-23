# NightPy
A python wrapper for Nightbot API

API documentation : https://api-docs.nightbot.tv/


How to use:
```
'''
Copy NightPy folder to project root.
'''

from NightPy.nightpy import NightPy


np = NightPy(client_id, client_secret, code)

np.skip_current_queue_item()
```
