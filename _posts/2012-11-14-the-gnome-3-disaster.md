---
layout: post
title: The Gnome 3 Disaster
date: '2012-11-14T20:14:00.003+01:00'
tags:
modified_time: '2012-11-14T20:21:29.118+01:00'
blogger_id: tag:blogger.com,1999:blog-4618495377058807667.post-3126794908565826676
permalink: /2012/11/the-gnome-3-disaster.html
---

Yes, this is yet another rant about Gnome 3.  Others have written
about it before, but I just read the announcement that [Gnome 3
Fallback mode will be dropped](http://mail.gnome.org/archives/release-team/2012-November/msg00009.html) and just need to vent my feelings
somewhere.

English is not my native language.  If it was I might have known
enough expletives to properly describe my feelings about Gnome 3.  But
in short it was a total disaster.

The single biggest mistake made was to break Gnome 2 and make it
impossible to have Gnome 2 and Gnome 3 installed on the same
machine. This made it impossible for people like me to keep running
Gnome 2 when distributions decided to push Gnome 3.  Someone at the
Gnome foundation really should have stopped to think for a moment and
said:

> _"Do we really have to break Gnome 2, can't we rename things and tack on a 3
at the end of all incompatible file names and APIs so that Gnome 3 can coexist
with Gnome 2?"_

But apparently nobody thought that far.  Then former Gnome bigwig
"Miguel de Icaza" tries to blame[the Linux developer culture for not
caring about backwards
compatibility](http://tirania.org/blog/archive/2012/Aug-29.html),
something that Linus Torvalds did not [quite agree
with](http://www.itwire.com/business-it-news/open-source/56418-torvalds-pours-scorn-on-de-icazas-desktop-claims).
What part of ["We don't break user
space"](http://www.spinics.net/lists/kernel/msg1435145.html) did the
Gnome people miss?

Instead they introduced Gnome 3 Fallback mode which really made nobody
happy, it was quite different from Gnome 2 with lots of things broken.
It was a [temporary
stopgap](https://live.gnome.org/ThreePointSeven/Features/DropOrFixFallbackMode)
that obviously would be dropped sooner rather than later when the
Gnome 3 people grew tired of it.  And then they act surprised that
nobody is willing to step up and maintain it.  And by the way, one of
the big reasons to why Gnome 2 and Gnome 3 can't coexist on the same
system is the Fallback mode, that's where most of the file name
conflicts come from.

What also surprised me a lot was that the Fedora Project seemed to
have drunk the cool-aid and pushed Gnome 3 into Fedora. Why didn't
anyone at Fedora push back and tell the Gnome people that it simply
wasn't acceptable to break Gnome 2 and that they'd have fix it before
being included in Fedora?  But no, when Fedora 15 arrived it came with
Gnome 3 and no way of running Gnome 2.

At that time I had just bought a new Sandy Bridge based computer which
wouldn't run Fedora 14, it required hardware support that was only
available in Fedora 15 so I was between a rock and a hard place, run
Fedora 14 and go through the pain of trying to add the hardware
support for Sandy Bridge by hand, or install Fedora 15 and get the
hardware support but be forced to use Gnome 3.  Actually, what I did
was to test Gnome 3 for a while and finally realize that I really
could not stand it; then [I built my own Gnome 2
packages](http://code.google.com/p/gnome-classic/) and used those
instead. That at least allowed me to get by for a while but it did
cost me a lot of time to make everything work and to resolve conflicts
later on.

Now we have the [MATE Desktop](http://mate-desktop.org/), a fork of
Gnome 2 which is available in Fedora 17.  Very good, finally some
sanity.  But it does have some problems, mate-applets is missing and I
really liked some of the applets that gnome had such as the system
monitor applet that shows me CPU/disk/network usage.  Also, since MATE
is a fork where everything has been renamed to avoid file name
conflicts and legal issues, which means that there is no binary
compatibility Gnome 2.  So I've had to redo all my customization of my
Gnome desktop by hand.  There are also some regressions where things
that used to work well on Gnome 2 no longer work on MATE or are
slightly broken.  MATE seems to be actively developed, so this will
undoubtedly be fixed sooner or later.

But I'm still quite pissed.  This is the year when Microsoft totally
messed up the desktop formerly known as Metro.  Gartner and other
organizations have been spewing FUD about ["Lost productivity stemming
from learning curves and compatibility can eat up direct-cost savings
when moving to Linux on the
desktop"](http://www.gartner.com/id=406459), Well, it would probably
have been easier to train a user on Gnome 2 than on Windows 8. The
last year has been a lost year for the Linux Desktop and the Gnome
Foundation have fumbled away one of their biggest opportunities ever.

What also bugs me is that they don't seem to realize how badly they
messed up.  Every time I read something from the Gnome Foundation they
keep saying what a success Gnome 3 is and that everyone loves it
(well, most users are not savvy enough to recompile Gnome 2 so they
have to make do with what the distribution makers hand them, so it's
not surprising that most people take the road of least resistance and
use Gnome 3 on Fedora or Unity on Ubuntu).  I have not seen one clear
message from the Gnome Foundation saying "we messed up, sorry" or
anyone from the Fedora Project saying "allowing Gnome 3 into Fedora
and breaking Gnome 2 was a mistake".  It probably won't ever happen.

But what I would like to see happening (since going back into time to
the beginning of 2011 and stopping them from breaking Gnome 2 is
rather tricky) is this:

  * Drop fallback mode from Gnome 3.  It's being done.  Good.  It should never have been introduced at all.

  * Fix the parts of Gnome 3 that stop it from coexisting with Gnome 2.  Rename executables, icons, files, APIs, D-Bus objects and whatnot in Gnome 3 that conflict with Gnome 2.

  * Allow MATE to continue using all the old Gnome names so that the MATE Desktop actually becomes the Gnome 2 desktop and is compatible with old applications.

  * Don't change Gnome 2/MATE a lot, decide that it is a mature product and only fix things that are obviously broken.  Sure, compatibility with Gnome 3 is nice and maybe newer versions could use some of the infrastructure in Gnome 3 that doesn't break Gnome 2.  Or improving the user experience when mixing Gnome 2 and Gnome 3 applications (for example, making themes apply to both Gnome 2 and Gnome 3 applications so that they look the same).  But don't make any major changes in how Gnome 2 works.

That would go a long way towards fixing things and making up for all
the trouble that has been caused.

And it would be very nice if someone from the Gnome Foundation would
publically admit that they have made mistakes in how the transition
from Gnome 2 to Gnome 3 was handled.  It won't make any difference to
how much pain they have caused over the last year, but it would be
quite nice anyway.  And it might even mean that we can all learn a bit
from this so the next time someone wants to introduce the next new big
thing we can avoid the making the same mistakes.  But as long as the
Gnome Foundation insists that everything is fine there is no chance of
doing that.

Note: even though I personally loathe the way the Gnome 3 desktop
works (it's just not made for me and my usage patterns), I have
nothing against people trying experimenting with new user interfaces.
Go ahead, "innovate" all you want, but **don't break old stuff**.  The
first releases of Gnome also sucked quite badly and at that time I
kept using fvwm2 instead.  But finally I grew tired of recompiling
fvwm2 and by that time Gnome had matured and turned into a quite
useful desktop.  That's how you make changes, build something new and
let Luddites like me use the old stuff, when the new stuff is good
enough and has matured we'll join you willingly.  Maybe.

