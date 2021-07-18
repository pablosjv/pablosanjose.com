---
title: "A sensible way to organize your repositories locally"
date: 2021-02-23
draft: false
slug: organize-local-repositories
city: Madrid
toc: true
tags:
- github
- gitlab
- dev
- git
---


If you interact with any typo of code in your life, you probably are using git. Git is an open source version control system. It allow us to track the changes in a project, also known as repository. And then we have platforms like [Github.com](http://github.com) and [Gitlab.com](http://gitlab.com) which host this repositories remotely so multiple people can collaborate and contribute. You can __clone__ this repositories locally to work on them, __commit__ your changes and __push__ them to the remote repository so they are incorporated in the last version.


So far so good.


## What is the problem?


Depending on how many repositories you interact in a day to day basis, you can easily lost track to where exactly your repositories are in your local machine. You maybe just want to use a `~/projects/` folder and put everything there. It is straight forward, but it other problems arise:

* Sooner or later that folder will become a huge mess with tons of projects, which makes it harder to look for a particular proyect
* You try to clone a project twice, because you don't remember that you have downloaded it before.
* You lost track of the _origin_ of the repository, meaning both where the remote is located (github, gitlab, bitbucket) and where that repository belongs (personal, organization, open source project...).
* Maybe you want to separate your work and personal projects and use different users and keys

This is just and organization problem, so we just need to come up with a simple system that allow us to put order and keep the order of the repos.


## Solution


> Replicate the remote repositories structure inside your local machine


This is the very simple rule I follow to organize my repositories. The algorith is as follows:

1. Create a folder for your projects. E.g. `~/projects/`
1. For each git platform you use (github, gitlab, etc...) create a single folder. E.g `~/projects/github.com/` or `~/projects/gitlab.com/`. I like to use the full domain name so I can distinguish between enterprise github/gitlab and the public ones.
1. For a repository of a platform, use the path in the url as the directory structure to place that repository. E.g. let's say I want to work on [https://github.com/apache/spark](https://github.com/apache/spark), then I will clone the repository into `~/projects/github.com/apache/spark`

That is the basic idea. This way you will have a 1:1 relationship between the remote repositories and your local. This is great to locate your projects quickly. You can also distinguish very quickly a fork, and the original one. It is specially useful with gitlab, where you can have a undefined number of subprojects too.


## Advance usage


Let's say that you want to keep your accounts separate. For example, your company has github enterprise at `github.company.com` and you also have your personal account with `github.com`. We don't want to make commits with our personal email or username into our company repositories neither the other way around! How can we avoid this?


The username and email are managed in your `~/.gitconfig` file. It can also be managed by `git config --global --set user.email` , for example. However you are not restricted to a single `.gitconfig` file. You can have as many as you want and include them in your global `~/.gitconfig` file. Moreover, this include can be conditional, like this:


```scheme
[user]
email = hi@pablosanjose.com
name = pablo

[includeIf "gitdir:~/projects/github.com/"]
path = ~/projects/github.com/.gitconfig

[includeIf "gitdir:~/projects/github.company.com/"]
path = ~/projects/github.company.com/.gitconfig
```


This way you can have a different configuration for any of the sites you use to host your repos. Then is a matter of including the `[user]` section in those `.gitconfig` files.


Note that the order is important. If a section is repeated, it will take the lat one. This is why we put the `[user]` at the top of the file in the example.

