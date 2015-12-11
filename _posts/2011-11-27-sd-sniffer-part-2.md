---
layout: post
title: SD Sniffer part 2
date: '2011-11-27T22:45:00.001+01:00'
tags:
- nerdy stuff
- hardware hacking
- SD bus
modified_time: '2011-11-27T22:50:19.729+01:00'
blogger_id: tag:blogger.com,1999:blog-4618495377058807667.post-2031177423977693249
permalink: /2011/11/sd-sniffer-part-2.html
---

I've finally had time to play around a bit more with the [SD
sniffer](http://blog.weinigel.se/2011/11/sd-sniffer.html) I designed a
few weeks ago.  I started placing all the active components on the
board and also got to curse myself for choosing the tiny, tiny, SC70
packages for the comparators.  The SC70 package is tiny and the
components were quite tricky to solder, mostly because I don't have
access to a stereo microscope any more.  But it all worked out in the
end.

Since I have used the OpalKelly FPGA board before and have a lot of
existing code for it, it didn't take long to hack together an FPGA
image that could control the D/A converter on the board to set the
reference voltage for the comparators.  With that done it was possible
to probe the outputs from the comparators with a scope and see that
the signals matched the signals on the SD bus.  One of the purposes
with this board was to not put too much load on the SD data lines, and
this actually seems to work.  I have a high speed SD card which runs
at 48MHz which gets a lot of errors if I probe the CLK line with a
normal 10x scope probe.  With the sniffer board it works fine at 48MHz
without any errors.

A little while later I could actually get the signals into the FPGA
and then stream them onto my PC.  The current FPGA image is rather
simple, on every SD CLK edge it samples the SD CMD and SD DATA lines
and stores them in a FIFO buffer inside the FPGA.  The Cypress FX2 USB
controller on the OpalKelly board then streams the data from the FIFO
to the PC.  This is basically what the USBee does, so this has the
same limitation of 30MHz clock speed on the bus.  So the only
advantage so far is that my SD sniffer doesn't affect the SD bus
signals as much as the USBee does.

But since I have access to the FPGA on the OpalKelly board there's a
lot more that can be done.  The USBee wastes a fair bit of the USB
bandwidth since it always transfers 8 bits to the host for each
sample.  The SD bus only uses 5 bits per sample, the CMD line and four
DATA lines, so 3 out of every 8 bits going over the USB bus are
unused.  With the FPGA it's quite simple to pack eight 5 bit samples
into five 8 bit words.  So to be able to handle a 50MHz bus it needs
50*5/8 = 31.25MBit/s throughput on the USB bus which is just about
what's possible.

But first I'll clean up the existing code a bit and then start working
on some way of processing and presenting the raw SD bus data.
