---
title: "The Best Makefile Help"
date: 2021-03-02
draft: false
slug: best-makefile-help
city: Madrid
toc: true
tags:
- makefile
- dev
---


Having a `Makefile` in my projects is something like I love. It is a common entrypoint for all the usual workflow commands in a project. It also serves as reference for those commands you never remember. New team members can pick the makefile and start developing right away (if everything is configured properly)


Makefiles can also be big and do complex things. So it is a good thing to have some kind of help dialog as the default target.


During the years I see this [gist](https://gist.github.com/prwhite/8168133) evolve with smart `help` targets to allow the makefile be self documented (it is always the first in my google search!). The idea is to include `##` after a target and add there the documentation for the target. The last ones are particular smart.


### Clean makefile help


Just add the following target into your makefile


```makefile
help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
```


I like that this one has colors too and it is my current favourite.


### Docker based solution


This one is interesting. Use a lightweight docker image to generate the help message. Curtesy of [Xanders github user](https://github.com/Xanders).


```makefile
# Show this help
help:
  @cat $(MAKEFILE_LIST) | docker run --rm -i xanders/make-help
```


Although nowadays the most likely scenario is that you have docker installed and running, I prefer to not depend on that for the help command unless I am using docker for other targets 

