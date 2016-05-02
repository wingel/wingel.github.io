---
layout: post
title: Playing around with Jupyter
tags:
- nerdy stuff
id: d9b8234c-3f86-4e4a-b10b-3483dbed91b1
---

I've written some python scripts that talk to a [BG7TBL signal
generator](http://sigrok.org/wiki/BG7TBL) and to my Tektronix 11801B
oscilloscope.  I can set the output frequency for the BG7TBL and then
dump the measured waveform from the scope over a serial port or GPIB.
With a bit of signal processing (FFT and some calculations) it's
possible to calculate the frequency and amplitude of the signal.
Combine the signal generator with the amplitude measurements and you
have a poor man's network analyzer.  It's very slow, it takes a couple
of minutes to do a sweep of 400 pointer, and it's probably not very
accurate, but it's good enough to be useful.

I've been thinking of ways to create some kind fo GUI for these
scripts, and finally found something called [Project
Jupyter](http://jupyter.org/).  Jupyter allows you to basically have a
virtual notebook where you can enter text and calculations.  The
killer though, is that you can enter code and do things such as plot
the output from a function.  I abused this interface a bit to run my
Python code and now I can do things like this:

[![Interactive measurements]({{site.baseurl}}/images/2016-04-07-playing-around-with-jupyter/interactive.gif)]({{site.baseurl}}/images/2016-04-07-playing-around-with-jupyter/interactive.gif)

This could be really, really powerful.  Imagine jotting down notes and
making measurements and then postprocessing data on the fly.  All the
raw measurements can be be saved so if I want to reprocess the
measurements later on I can do that.  It should also be fairly easy to
take a notebook and convert it into a blog post.

I could really like this.

