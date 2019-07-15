![alt text](http://www.iamgregamato.com/img/np_logo.svg)
<p align=center>
  <a href="https://badge.fury.io/py/NightPy">
    <img src="https://badge.fury.io/py/NightPy.svg" alt="PyPI version" height="18">
  </a>
</p>

A python wrapper for Nightbot API

API documentation : https://api-docs.nightbot.tv/


### Install 
From PyPI:
```bash
pip install NightPy
```
Using Distributed Wheel from GitHub:
```bash
pip install NightPy-2018.1.1-py3-none-any.whl
```
### Usage
```python
from NightPy.nightpy import NightPy


np = NightPy(api_token_here)

np.skip_current_queue_item()
```
