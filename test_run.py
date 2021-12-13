# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import requests

data = {'description': 'random description'}

for x in range(1000):
    r = requests.post('http://127.0.0.1:8000/test/', json=data)
