---
title: "Importing local Python modules in to Jupyter Notebooks"
date: 2021-02-20
draft: false
slug: import-python-local-modules-in-notebooks
city: Madrid
toc: true
tags:
- tutorial
- python
- jupyter
---


I find working in a Jupyter Notebook very useful when developing any type of python code. The instant feedback of new written code help me a lot to iterate quickly and debug certain snippets.

There is a small tweak that you can do to also import your python modules and functions while developing in notebooks. It is very simple but I always struggle to remember it and found it in google


```python
%load_ext autoreload
%autoreload 2

import os
import sys
module_path = os.path.abspath(os.path.join('../src')) # or the path to your source code
sys.path.insert(0, module_path)
```


### What does this do?

Basically we have two parts. 

The first one is the `autoreload` module. This is an extension that is installed by default with Jupyter. It allow us (as its name suggest) to autoreload the imported modules when there is any changes. Otherwise, you will need to restart the kernel.

The second part is to add the path to your source code to your `PYTHONPATH` so it can be imported. The easiest way of do this is to insert the math in with the `sys.path.insert` command. the `0` is the index to insert the path. We put it in the first place so it takes preference over anything else you might have installed.

### Bonus track - Add your environment variables

As a bouns track, I also like to add my environment variables in the notebooks itself when I am debuging something. It as easy as:


```python
%env AWS_PROFILE=development
```


Of course, be careful and don't put any secret in the code.

### That's it!

This is a ritual setup that I always do when creating a new notebook. Maybe the next step is to automatize it...
