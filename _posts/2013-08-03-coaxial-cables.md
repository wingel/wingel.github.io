---
layout: post
title: Coaxial Cables
date: '2013-08-03T12:04:00.002+02:00'
tags:
- nerdy stuff
modified_time: '2013-08-03T12:04:39.629+02:00'
thumbnail: http://2.bp.blogspot.com/-NGjdbbp-NOg/UfzDgiiwVLI/AAAAAAAAAGI/nvgAcXVHQxY/s72-c/square.png
id: tag:blogger.com,1999:blog-4618495377058807667.post-5994926949903660941
redirect_from: /2013/08/coaxial-cables.html
---

It's been a long time since I wrote anything here so I guess it's time
to write something.  A warning though, this post will talk about
coaxial cables, so those with a low tolerance for boredom can stop
reading now.

A few years ago I bought a [TDR
oscilloscope](http://blog.weinigel.se/2011/12/tdr-scope.html) and
wrote a bit about how you can use it to measure the performance of
different kinds of cable.  So I went out and bought a bunch of
different coaxial cables and tried to measure the RF performance of
them.  The idea was to see how much difference the cables make before
buying half a dozen cables to use in my lab.

My oscilloscope also has a function for Time-domain transmissiometry
(TDT).  This functions uses the same pulse generator as the TDR
function, but the cable is connected between two ports on the scope
and instead of looking at the reflections, the scope will measure the
signal that comes out the other end.  The pulse has a 250mV amplitude
and a 25ps rise time and for a perfect cable what would be what the
scope would show at the other end, but with real cables there will be
distortion of the signal.

A square wave is composed of all the odd harmonics of the fundamental
frequency for the square wave.  A first approximation of a square wave
is just a sine wave, and by adding higher frequency harmonics the
shape will get closer and closer to a perfect square wave with
vertical edges that are infinitely short.

[![]({{ site.baseurl }}/images/s400/square.png)]({{ site.baseurl }}/images/s1600/square.png)

In the physical world is not possible to have harmonics with
infinitely high frequencies, so all actual electrical signals will
only approximate as square wave and will have a bit of ringing and
non-zero rise and fall times.  The higher the bandwidth of the system
the faster rise and fall times it will have and the closer it can get
to the ideal square wave.

As a rule of thumb for analog oscilloscopes, the bandwidth neccesary
to show a certain rise time is:

> bandwidth * risetime = 0.45

So a 25ps risetime requires about 0.45 / 25ps = 18GHz of bandwith.

This also shows up with cables, cables attenuate signals send through
them, and the attenuation is frequency dependent.  Most cables
attenuate high frequency signals more than low frequency signals and
when measuring TDT this will slow down the rise time of the TDR pulse.
So a cable with higher bandwidth will generally show faster rise
times.  A cable with with high bandwidth could have high total losses
though, and vice versa.  A mains extension cord has horrible bandwidth
but not that much losses, while a thin coax cable can have pretty good
bandwidth but high resistance and losses.  Another thing to think
about is the impedance of the cable, a thin and flexible cable might
get bent or pinched so that the impedance varies and this can cause
reflections and losses.

Without further ado, here are the contestants:

[![]({{ site.baseurl }}/images/s400/cables.jpg)]({{ site.baseurl }}/images/s1600/cables.jpg)

Starting from the left, here are the results.

  1. 75 cm of RG405, a 2.2 mm diameter semi-flexible cable bought from
  [rfsupplier.com](http://rfsupplier.com/).  Semi-flexible means that
  the cable is fairly stiff and not that easy to work with - you're
  really meant to connect the permanently and not move it around that
  much.  The received signal is down at 230mV at the other end, so the
  total losses are fairly high and the rise time is just below 30ps so
  the bandwidth is decent.

  2. 75 cm of RG402, a 3.6 mm semi-flexible cable also from
  rfsupplier.  Not as much losses as with the RG405, the received
  signal is 240mV and the rise time is also just below 30ps.  I guess
  this is to be expected, a thicker cable has slightly less resistance
  and less losses.

  3. 28 cm of semi-rigid cable bought from
  [sdr-kits.net](http://sdr-kits.net/).  This was some surplus cable
  so I have no idea what the brand of the cable is.  I is short and
  semi-rigid means that it's stiff and hard to work with and can
  probably not be bent more than a dozen times without going bad.  It
  is the best cable I have though, very low losses, the received
  signal is at 245mV and the rise time is at 25ps, almost identical to
  the source.  I'm curious to how much of this performance is due to
  the cable being so short and how much is due to the quality of the
  cable.  It would be interesting to get a 25cm RG400 or RG402 cable
  and compare.

  4. 75 cm of RG400, a 5mm flexible cable from rfsupplier.  RG400 is
  specified to have a "max operating frequency" of 12.4GHz.  It's
  quite nice to work with since it is fairly flexible.  It did have
  fairly high losses with 235mV received signal and the rise time was
  30ps.

  5. 75 cm of KSR195, a 5mm "low loss" cable from rfsupplier.  The
  cable is supposed to be a replacement for a standard cable called
  LMR195.  It's fairly stiff and hard to work with.  Low losses at
  240mV received signal and the same 30ps rise time as most other
  cables.

  6. 65 cm of flexible cable from sdr-kits, also surplus with a Huber
  Suhner sticker on it. The loss was decent at 240mV but the rise time
  was 33ps, slightly slower than most other cables.  Nice to work with
  though and the angled connectors make it preferable for some tasks.
  I'm also curious to how the angled connectors affect the rise time,
  does it make any difference or not?

  7. 75 cm of KSR420, a 6 mm "low loss" cable from rfsupplier.
  Replacement for standard cable LMR240.  Fairly stiff and cumbersome.
  Low losses at 245mV received signal and a rise time of 30ps.  There
  were noticeable impedance discontinuities at the SMA connector
  though which showed up in TDR measurements.

  8. 75 cm of KSR400, a 10 mm "low loss" cable from rfsupplier.
  Replacement for standard cable LMR400.  Low losses at 245mV received
  signal and a rise time of 33ps.  Even stiffer and harder to bend
  than KSR420 and had even more impedance discontinuities in the
  connector.

  9. 50 cm piece of unspecified 2mm flexible cable which is not in the
  picture.  This is just some cable I had lying around.  Very thin and
  flexible and nice to work with.  Decent losses at 240mV but slow
  rise time at 35ps.

What's the result of all this?  Well, the differences were smaller
than I expected, all cables are probably good up to 10GHz or so and
have reasonable losses.  This informal testing was probably unfair to
the low loss cables, they are meant to be used for long distances
where loss is very important, testing on a 75cm piece of cable does
not show off what they are good at.  I did find a data sheet for
LMR400 which says that it is only specified for signals up to 2.4GHz.;
according to the rule of thumb above, the 33ps for KSR400 means that
for such a short length it had a bandwidth of more than 10GHz.  If I
really wanted to test this cable properly I ought to buy 100m of cable
and see how it performs. It's probably also kind of dumb to put SMA
connectors on such cables since a SMA connector is so small compared
to the diameter of the cable, using a N connector would probably work
much better.

So, if you need the best performance, buy a good (and probably
expensive) and short semi-rigid cable.  Or call [Huber
Suhner](http://www.hubersuhner.com/) and buy their Sucotest cable,
I've used it before and yes it's expensive but it's also flexible and
nice to work with; it's high performance and they will even calibrate
it for you so that you know the attenuation for all frequencies up to
the specified bandwidth of the cable.  I wish I could afford stuff
like that nowdays.

Me, I'll probably buy a couple more cables with RG400, it's flexible
nice to work with on a lab bench and has decent performanc.  I must
also say that I'm quite happy with rfsupplier, I found them on eBay
and they built exactly the cables I asked for at a good price and with
fast delivery.  I was a bit worried about buying cables from China,
but after measuring the cables rfsupplier delivered and comparing them
to other variants I have nothing at all to complain about.  And I'll
see if they have some cable similar to the last one in the list, since
it's so thin and flexible it's even nicer to work with and for signals
up to 1GHz or so it's probably quite good enough.
