---
layout: post
title: STM32F405 pinout spreadsheet
date: '2015-11-14T17:37:00.000+01:00'
author: Christer Weinigel
tags: stm32f405 stm32f407
---

I've been using the STM32F405 for some of my projects.  To make it
easier to figure out which I/O pins I wanted to use for a certain
project I created a spreadsheet with the possible alternate functions
from the data sheet.  The first sheet lists pins grouped by which port
(PA, PB, etc) it is connected to.  The next sheets lists pins ordered
by pin numbers for all packages.  Two more sheets only list the the
pins present on the LQFP64 and LQFP100 packages.

The spreadsheet is a [LibreOffice/OpenOffice .ods
file]({{site.url}}/documents/stm32f405-pinout.ods) and have been
converted to [Excel .xls
file]({{site.url}}/documents/stm32f405-pinout.xls) if you can't read
LibreOffice documents.

I created spreadsheet by hand, so there will most probably be some
errors in it.  If you find any errors, please send me a mail and tell
me so that I can fix them.
