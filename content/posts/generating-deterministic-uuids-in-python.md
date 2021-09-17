---
title: "Generating Deterministic UUIDs in Python"
date: 2021-09-17
draft: false
slug: 
city: Madrid, Spain
toc: true
tags:
- dev
- python
- tutorial
---


UUID stands for [Universally Unique Identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier). It is a standard way to generate unique IDs for elements in software systems. Latests versions of the UUID, almost guarantees uniqueness. As a fellow colleague said:


> _"Is more probable that both our houses will be struck by lighting at the same time that to have repeated UUIDs"_


A typical way to generate UUIDs in python is to use the standard library package: `uuid`. The usage is very simple


```python
import uuid

my_id = str(uuid.uuid4())

print(my_id)
```


Quite straightforward.


However, there might be the case that you want to generate the same UUIDs multiple times. The reason can be:

1. Ease for creating test to functions that rely on UUID.
1. Reproducibility of data pipelines.
1. Create collisions "on purpose"  when you want to deduplicate entities based on specific fields.

Working in Data and ML, I have recently encounter more than one time the number 1 and 2. Number 3 I have just encountered it when doing a particular data extraction for news data in which I want to make sure I assign the same UUID to the same article (date + title + article body)


I have searched the web on how to do this, and although is also simple, is not as straightforward as just generating a UUID4. I found 2 approaches that worked quite well.


# 1. Time + Namespace


The first approach for me was to make the UUID dependent on two things.


First, the __execution date time__: this should be passed as a parameter to the generator. When orchestrating data pipelines with Airflow and other data orchestration tools, is very common to have the execution date as a parameter. With this you can ensure the reproducibility of past executions.


However, timestamp alone can lead to unintended collisions with other pipelines. So it is important to include other parameter to the equation. The parameter is a __namespace__, which can be virtually anything. For my use case, we assigned as namespace the name of the pipeline in which the code is run.


I created a class for this `IDGenerator`. We used the execution time and the namespace to generate a seed for the python's `random` module. Then, the `UUID` class accepts a 128 bits integer to generate the UUID deterministically.


The code will look something like this


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


This approach is simple enough to help you writing tests for your code, and to generate the same id in pipelines in which you know that the number of elements don't change between executions. However, it is naive to the actual contents of the data so it will assign different UUIDs to duplicates entries if there where any. If at some point in a data correction you add or remove elements, this approach will change the ids for those elements which is not ideal.


## 2. Content based


To overcome the drawbacks of the previous approach, I implemented a second version. This one works more general than the previous one, taking a free text as the seed for the the `random` module. As the text can be arbitrarily long, we first hash the text and then use the hash to form the seed .


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


## Bonus: `Random()` objects


You might have notice that in this implementation we crea a `random.Random()` object as a class attribute. This is a feature that I didn't know it exists until recently.


The `random` python module acts like a singleton instance. But we can separate `Random` objects. This is great if you have multiple `IDGenerator` objects in different places on your code and you don't want that the seed are overwritten. 

