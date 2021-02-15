---
title: "macOS Command Line Tools"
date: 2020-12-16
draft: false
slug: xcode-select
city: Cascavel
toc: true
tags: [macos]
---

Today, again, I forgot the command to install Command Line Tools and had to search for it.

This is post if for future me.

---

You always forget how to install XCode Command Line Tools when a new macOS release comes out... specially because this always happens when you're in a hurry, and obviously you forgot to run this earlier.

{{< figure caption="Installing..." src="/public/images/xcode-select/63cdce04-0861-416e-9ed9-aeb0f409df17.png" >}}

As you know, its a simple command that you just can't remember when you need:

```sh
$ xcode-select --install
```

You know sometimes it fails and you might also need to reset if first:

```sh
$ sudo xcode-select --reset
```

Last but not least, on betas, sometimes, you might need to download it directly from [Apple developers downloads](https://developer.apple.com/download/more/) page, which is a page you always take a couple of minutes to find on Google, for whatever reason. So, saved you a Google search.
