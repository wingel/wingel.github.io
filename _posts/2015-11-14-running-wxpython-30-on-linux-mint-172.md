---
layout: post
title: Running wxPython 3.0 on Linux Mint 17.2
date: '2015-11-14T17:37:00.000+01:00'
author: Christer Weinigel
tags:
modified_time: '2015-11-14T17:37:10.213+01:00'
blogger_id: tag:blogger.com,1999:blog-4618495377058807667.post-6059973465350912087
permalink: /2015/11/running-wxpython-30-on-linux-mint-172.html
---

I wanted to try out wxPython 3.0 on my machine running Linux Mint
17.2. Unfortunately, Ubuntu 14.04 LTS, that Mint is based on, only has
wxPython 2.8 in its repository.

It turned out to be fairly easy to build my own packages for wxPython
3.0 though.  Here's a short summary on how to do it.

Download the debian sources for a newer version of Ubuntu:

    http://packages.ubuntu.com/source/xenial/wxpython3.0

The files I downloaded were:

    wxpython3.0_3.0.2.0+dfsg-1build1.debian.tar.xz
    wxpython3.0_3.0.2.0+dfsg-1build1.dsc
    wxpython3.0_3.0.2.0+dfsg.orig.tar.xz

But they might be updated when you read this, in that case, modify the
commands below to match the current version.

Unpack the sources the same way that "apt source" usually does it:

    xzcat wxpython3.0_3.0.2.0+dfsg.orig.tar.xz | tar xvf -
    cd wxpython3.0-3.0.2.0.orig
    xzcat ../wxpython3.0_3.0.2.0+dfsg-1build1.debian.tar.xz | tar xvf -

Install some tools to build Debian packages:

    sudo apt-get install build-essential devscripts

Install some dependencies needed by wxPython itself:

    sudo apt-get install python-all python-all-dev libgtk2.0-dev libwxgtk3.0-dev libwxgtk-media3.0-dev

Build the Debian packages.  "-us -uc" tells debuild to skip signing
the packages, "-b" tells debuild to only build the binary packages:

    debuild -us -uc -b

You should now have a bunch of debian packages in the parent
directory.  On my computer I got the following:

    cd ..
    ls python-wx*.deb

    python-wxgtk-media3.0_3.0.2.0+dfsg-1build1_amd64.deb
    python-wxgtk3.0-dev_3.0.2.0+dfsg-1build1_all.deb
    python-wxgtk3.0_3.0.2.0+dfsg-1build1_amd64.deb
    python-wxtools_3.0.2.0+dfsg-1build1_all.deb
    python-wxversion_3.0.2.0+dfsg-1build1_all.deb

All that's left to do is to install them:

    sudo dpkg -i python-wx*.deb

One more thing though.  This will change the default version of
wxPython on your system to 3.0.  So any python application that does
just does "import wx" will use version 3.0 instead of 2.8:

    python
    >>> import wx
    >>> wx.VERSION_STRING
    '3.0.2.0'

This might break some other which did not expect that.  I have not
noticed any breakage so far, but if you want to be really safe, you
can lower the priority of wxPython 3.0 so that 2.8 will be the default
instead:

    update-alternatives --install /usr/lib/wx/python/wx.pth wx.pth /usr/lib/wx/python/wx3.0.pth 0

    python
    >>> import wx
    >>> wx.VERSION_STRING
    '2.8.12.1'

You can then explicitly select wxPython 3.0 in your application using
the wxversion module:

    python
    >>> import wxversion
    >>> wxversion.select('3')
    >>> import wx
    >>> wx.VERSION_STRING
    '3.0.2.0'

Now I just have to remember why I wanted wxPython 3.0 on my machine.  It'll come back to me soon I hope.

