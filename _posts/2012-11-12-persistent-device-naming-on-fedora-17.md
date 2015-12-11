---
layout: post
title: Persistent device naming on Fedora 17
date: '2012-11-12T23:57:00.000+01:00'
tags:
modified_time: '2012-11-12T23:57:25.190+01:00'
blogger_id: tag:blogger.com,1999:blog-4618495377058807667.post-5954802645584172628
permalink: /2012/11/persistent-device-naming-on-fedora-17.html
---

In their infinite wisdom the people behind Fedora 17 decided to remove
the udev scripts that provided persistent network names.  I kind of
liked those scripts so I just created a small RPM package which just
contains the files from a Fedora 16 installation.

So head over to [http://code.google.com/p/wingel-udev-persistent-
net](http://code.google.com/p/wingel-udev-persistent-net/) and try it out.

