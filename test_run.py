# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import random

import requests

for x in range(1000):
    data = {"val1": random.randint(0, 100000),
            "val2": random.randint(0, 100000)}
    r = requests.post('http://127.0.0.1:8000/test/', json=data)
    print(r.json())
