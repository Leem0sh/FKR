# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations
import requests
data = {'description': 'random description'}


for x in range(600):
    r = requests.post('http://127.0.0.1:8000/dimensions/measure/1/nabytek', json=data)
    print(r.text)
