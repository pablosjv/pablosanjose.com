---
title: "Generating deterministic UUIDs in Python"
date: 2021-05-08
draft: true
slug: 
city: Madrid, S
toc: true
tags:
---


# Approach 1


Time and namespace based


```python
import random
import uuid
from datetime import datetime


class IDGenerator:
    """Wraper that creates deterministic UUID4"""

    def __init__(self, execution_date: datetime, namespace: str) -> None:
        self.seed: int = self._create_seed(execution_date, namespace)
        self.random: random.Random = random.Random()
				self.random.seed(self.seed)

    def _create_seed(self, execution_date: datetime, namespace: str) -> int:
        namespace_part: str = ''.join([str(n) for n in list(namespace.encode('utf8'))])
        timestamp_part: str = str(int(execution_date.timestamp()))
        seed: int = int(namespace_part + timestamp_part)
        return seed

    def get(self, text: str = "None") -> str:
        return str(uuid.UUID(version=4, int=self.random.getrandbits(128)))
```


## Approach 2


```python
import hashlib
import random
import uuid


class IDGenerator:
    """Wraper that creates deterministic UUID4"""

    def __init__(self) -> None:
        self.random: random.Random = random.Random()

    def get(self, text: str) -> str:
        h = hashlib.sha224(text.encode('utf-8'))
        self.random.seed(int(h.hexdigest(), 16))
        return str(uuid.UUID(version=4, int=self.random.getrandbits(128)))
```

