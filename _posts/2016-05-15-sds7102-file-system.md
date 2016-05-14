---
layout: post
title: The SDS7102 File System
tags:
- nerdy stuff
- sds7102
id: 5e6de831-75cb-4369-9ac9-3af4ee066320
---

This is a post in a series about me poking at the insides of my OWON
SDS7012 oscilloscope.  You might want to start reading at the
[beginning]({{site.baseurl}}/2016/05/01/sds7102-hacking.html).

It was time to dig into the file system of SDS7012 scope to see if I
could understand how it worked.

Yaffs
=====

[Yet Another Flash File System (Yaffs)](http://www.yaffs.net/) is a
file system specifically built for working with NAND flash.  It
handles all the tricky parts of a NAND flash such as error correction,
remapping bad flash pages, wear leveling (trying to write to each
flash page an equal number of times so that single pages won't wear
out).  It's open source available under the GPL license and can be
found in both Linux and uBoot and there are also commercial licenses
if one wants to use it an a proprietary system.

I'd found some strings in the dump of the NAND flash that hinted that
the SDS7102 used Yaffs, and there were some comments on the EEVblog
forums that also said that the file system was Yaffs.  I searched the
internets for some tools that were supposed to be able to unpack a
Yaffs file system.

I spent quite some time on this, and failed miserably, none of the
tools wanted to have anything to do with the data from the dump.  I'm
almost ashamed to say that it took me a long time to actually start
thinking and actually look at the file system data myself.  When I did
i quickly realised that no, is wasn't Yaffs at all.

The first file
==============

It looked like the file system started at 640kBytes (0xa0000) into the
dump and here's the contents of the first page:

    000a0000  01 ff ff ff 01 00 00 00  ff ff 66 70 00 00 00 00  |..........fp....|
    000a0010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000a0100  00 00 00 00 00 00 00 00  00 00 ff ff 80 f1 00 00  |................|
    000a0110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    000a0120  00 00 00 00 00 00 00 00  ff ff ff ff ff ff ff ff  |................|
    000a0130  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    000a01c0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    000a01d0  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    000a01e0  ff ff ff ff ff ff ff ff  00 00 00 00 ff ff ff ff  |................|
    000a01f0  ff ff ff ff ff ff ff ff  00 00 00 00 00 00 00 00  |................|
    000a0200  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    000a07e0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    000a07f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

Each flash page is 2kBytes and after actually turning on my brain it's
fairly obvious that
<code>01&nbsp;ff&nbsp;ff&nbsp;ff&nbsp;01&nbsp;00&nbsp;00&nbsp;00</code>
is some kind of magic identifier, and that "fp" is the file name.

    000a0800  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    000a0810  55 99 aa 66 0c 85 00 e0  04 00 8c 85 c0 01 8c 82  |U..f............|
    000a0820  bc 00 8c 86 90 77 8c 43  20 00 08 c9 0c 87 00 f3  |.....w.C .......|
    000a0830  0c 83 00 81 04 00 04 00  04 00 04 00 04 00 04 00  |................|
    000a0840  04 00 04 00 04 00 04 00  04 00 04 00 04 00 04 00  |................|
    000a0850  04 00 04 00 04 00 cc 81  3c 13 8c 81 10 81 2c 84  |........<.....,.|
    000a0860  00 00 4c 80 00 f8 8c 87  ff ff cc 84 00 a0 cc 82  |..L.............|
    000a0870  00 20 cc 80 80 00 4c 86  00 00 4c 81 00 00 4c 85  |. ....L...L...L.|
    000a0880  00 00 4c 83 00 00 4c 87  00 00 cc 85 d8 47 cc 43  |..L...L......G.C|
    000a0890  00 00 00 00 04 00 04 00  0c 44 00 00 00 00 0c 85  |.........D......|
    000a08a0  00 80 0a 06 00 40 19 b5  00 00 00 00 00 00 00 00  |.....@..........|
    000a08b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

The data at 0xa0800 looks familiar.  Where have I seen that before?

Of course, it's the beginning of a Xilinx Spartan 6 bitstream file
that I had seen on [a blog post about bitstream
analysis](https://vjordan.info/log/fpga/bitstream-analysis-code.html).
Calling a FPGA bitstream file "fp" also makes sense.

![Analysis of a FPGA bitstream]({{site.baseurl}}/images/2016-05-15-sds7102-file-system/bitstream_analyzed.png)

That the data seems to be bitswapped, but that's actually rather
common.  Xilinx's own configuration memories uses bitswapped data, so
that's what their tools default to when outputting a bitstream file.

A bit later an almost identical flash page as the header appeared,
probably a trailer that indicates the end of the file.

    000f4800  01 ff ff ff 01 00 00 00  ff ff 66 70 00 00 00 00  |..........fp....|
    000f4810  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000f4900  00 00 00 00 00 00 00 00  00 00 ff ff 80 f1 00 00  |................|
    000f4910  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    000f4920  00 00 00 00 7c 32 05 00  ff ff ff ff ff ff ff ff  |....|2..........|
    000f4930  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    000f49c0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    000f49d0  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    000f49e0  ff ff ff ff ff ff ff ff  00 00 00 00 ff ff ff ff  |................|
    000f49f0  ff ff ff ff ff ff ff ff  00 00 00 00 00 00 00 00  |................|
    000f4a00  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    000f4fe0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    000f4ff0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

There are some differences though, in the header the word at 0x224 was
<code>00&nbsp;00&nbsp;00&nbsp;00</code>, in the trailer it is
<code>7c&nbsp;32&nbsp;05&nbsp;00</code>.  Hmm..  What's the size of
all the pages between the header and the trailer?
0xf4800&nbsp;-&nbsp;0xa0800&nbsp;=&nbsp;0x54000.  Take the number from
the trailer 0x5327c and round that up and it matches fairly well.
That field might be the file size.

A copy of the first file
========================

The next page seems to be the header for a file called "fpcp".  

    000f5000  01 ff ff ff 01 00 00 00  ff ff 66 70 63 70 00 00  |..........fpcp..|
    000f5010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000f5100  00 00 00 00 00 00 00 00  00 00 ff ff 80 f1 00 00  |................|
    000f5100  00 00 00 00 00 00 00 00  00 00 ff ff 80 f1 00 00  |................|
    000f5110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    000f5120  00 00 00 00 00 00 00 00  ff ff ff ff ff ff ff ff  |................|
    000f5130  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|

The contents seem to be the the same as for "fp".  Seems like they keep
a backup copy of FPGA bitstream in a second file.

    000f5800  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    000f5810  55 99 aa 66 0c 85 00 e0  04 00 8c 85 c0 01 8c 82  |U..f............|
    000f5820  bc 00 8c 86 90 77 8c 43  20 00 08 c9 0c 87 00 f3  |.....w.C .......|
    000f5830  0c 83 00 81 04 00 04 00  04 00 04 00 04 00 04 00  |................|
    000f5840  04 00 04 00 04 00 04 00  04 00 04 00 04 00 04 00  |................|

The "fpcp" trailer looks the same as for "fp", with the file size at
offset 0x124:

    00149800  01 ff ff ff 01 00 00 00  ff ff 66 70 63 70 00 00  |..........fpcp..|
    00149810  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    00149900  00 00 00 00 00 00 00 00  00 00 ff ff 80 f1 00 00  |................|
    00149910  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    00149920  00 00 00 00 7c 32 05 00  ff ff ff ff ff ff ff ff  |....|2..........|
    00149930  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|

Param file
==========

The "fp" and "fpcp" files are followed by a "param" file header:

    0014a000  01 ff ff ff 01 00 00 00  ff ff 70 61 72 61 6d 00  |..........param.|
    0014a010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    0014a100  00 00 00 00 00 00 00 00  00 00 ff ff 80 f1 00 00  |................|
    0014a110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    0014a120  00 00 00 00 00 00 00 00  ff ff ff ff ff ff ff ff  |................|
    0014a130  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    0014a1c0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    0014a1d0  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    0014a1e0  ff ff ff ff ff ff ff ff  00 00 00 00 ff ff ff ff  |................|
    0014a1f0  ff ff ff ff ff ff ff ff  00 00 00 00 00 00 00 00  |................|
    0014a200  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    0014a7e0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    0014a7f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

"param" file data:

    0014a800  00 00 00 00 00 00 00 00  30 30 30 30 30 30 30 30  |........00000000|
    0014a810  30 30 30 30 30 30 30 30  00 00 00 00 00 00 00 00  |00000000........|
    0014a820  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    0014a990  00 00 00 00 00 00 00 00  cd ab cd ab 00 00 39 30  |..............90|
    0014a9a0  7c 32 05 00 22 6c 62 40  00 00 00 00 00 00 00 00  ||2.."lb@........|
    0014a9b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    0014a9c0  00 00 00 00 00 00 00 00  e9 5b c9 92 00 00 00 00  |.........[......|
    0014a9d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    0014afff  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

and "param file" trailer:

    0014b000  01 ff ff ff 01 00 00 00  ff ff 70 61 72 61 6d 00  |..........param.|
    0014b010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    0014b100  00 00 00 00 00 00 00 00  00 00 ff ff 80 f1 00 00  |................|
    0014b110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    0014b120  00 00 00 00 cc 01 00 00  ff ff ff ff ff ff ff ff  |................|
    0014b130  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    0014b1c0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    0014b1d0  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    0014b1e0  ff ff ff ff ff ff ff ff  00 00 00 00 ff ff ff ff  |................|
    0014b1f0  ff ff ff ff ff ff ff ff  00 00 00 00 00 00 00 00  |................|
    0014b200  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    0014b7e0  ff ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
    0014b7f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

The file size at 0x124 is 0x1cc so it seems to be a very small file.

The "param" file is followed by an identical "paramcp" file, just as
for "fp".

More files
==========

The next file after that is "tx" which contained a lot of text, it
seems to be some kind of calibration data:

    0014df90  38 3d 39 33 32 30 3b 09  0d 0a 24 61 75 74 6f 5f  |8=9320;...$auto_|
    0014dfa0  73 65 6c 66 5f 63 61 6c  20 63 68 32 5f 74 69 61  |self_cal ch2_tia|
    0014dfb0  6f 5f 62 6a 61 30 5f 39  3d 32 30 36 39 3b 09 0d  |o_bja0_9=2069;..|
    0014dfc0  0a 24 61 75 74 6f 5f 73  65 6c 66 5f 63 61 6c 20  |.$auto_self_cal |
    0014dfd0  63 68 32 5f 74 69 61 6f  5f 62 6a 61 30 5f 31 30  |ch2_tiao_bja0_10|
    0014dfe0  3d 35 32 31 31 3b 09 0d  0a 24 61 75 00 00 00 00  |=5211;...$au....|
    0014dff0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    0014e000  74 6f 5f 73 65 6c 66 5f  63 61 6c 20 63 68 32 5f  |to_self_cal ch2_|
    0014e010  74 69 61 6f 5f 62 6a 61  30 5f 31 31 3d 31 30 34  |tiao_bja0_11=104|
    0014e020  30 30 3b 09 0d 0a 0d 0a  24 74 72 69 67 6d 6f 64  |00;.....$trigmod|
    0014e030  65 20 63 68 31 5f 41 43  5f 76 61 6c 75 65 5f 52  |e ch1_AC_value_R|
    0014e040  3d 32 33 33 3b 09 09 2f  2f 43 48 31 20 cb cd 41  |=233;..//CH1 ..A|

One interesting thing to note is that the last 20 bytes of the flash
pages in the file are zeroes.  At this point I checked the "fp" file
and noticed that it also had zeroes at the end of each page.  For some
strange reason they are only using 2028 bytes of the 2048 bytes in a
page.  Weird...  But oh well, if that's how it is, that's how it is.

This file is also followed by a "param" and "paramcp" file.

File Extractor
==============

At this point I had recognized a pattern.  A file consists of a header
page, a data page and a trailer page.  Only the first 2028 bytes of
each page actually contain data.  Each file is followed by an
identical "cp" file then by and a "param" and "paramcp" file.

As a programmer, if anything has to be done more than once it's time
to write a tool to automate it.

I wrote some Python code to read the dump file and extract all the
files it could find.  The tool parses the header page and copies out
data from each flash page until it finds the trailer page.  It
verifies that the file size in the trailer rounds up to the size of
the copied data and that all the extra data beyond the file size is
zeroes.  It then chops of the extra zeroes and writes the data to a
file.  If there file with the name from the header already exists the
tool adds a number to the end to make the file name unique.

After this I had a directory with a bunch of files.  There is a Unix
command called "file" that knows about a lot of different file
formats.  Here's what it has to say about the files:

    fp:        AIX core file fulldump 32-bit 64-bit
    fpcp:      AIX core file fulldump 32-bit 64-bit
    param:     data
    paramcp:   data

    tx:        ISO-8859 text, with CRLF line terminators
    txcp:      ISO-8859 text, with CRLF line terminators
    param.0:   data
    paramcp.0: data

    bmp:       PC bitmap, Windows 3.x format, 800 x 600 x 8
    bmpcp:     PC bitmap, Windows 3.x format, 800 x 600 x 8
    param.1:   data
    paramcp.1: data

    hz:        data
    hzcp:      data
    param.2:   data
    paramcp.2: data

    os:        data
    oscp:      data
    param.3:   data
    paramcp.3: data

    me:        Little-endian UTF-16 Unicode text, with CRLF line terminators
    mecp:      Little-endian UTF-16 Unicode text, with CRLF line terminators
    param.4:   data
    paramcp.4: data

    hlp:       Little-endian UTF-16 Unicode text, with CRLF line terminators
    hlpcp:     Little-endian UTF-16 Unicode text, with CRLF line terminators
    param.5:   data
    paramcp.5: data

I had already identified the "fs" as a FPGA bitstream, so the "AIX
core" stuff is file being confused about the file format.

"tx" looks like text file with calibration data.

"bmp" looks like a Windows bitmap.  Let's look at it:

![OWON Boot Image]({{site.baseurl}}/images/2016-05-15-sds7102-file-system/bmp.png)

The boot logo.  Neat!  And since I can load the image and there's no
visible corruption it seem that my file system extractor actually
works.

"hz" contains a lot of binary data.  It's about 3MBytes in size so it
probably does something important, but I have no idea what.

"os" is another 3MByte file which seems to contain ARM machine code.
Considering the name this is probably the main operating system for
the scope.

The "me" file and the "hlp" files both contain unicode text and seems
to be translations for the menu entries and help texts respectively.

At this point my file extractor broke.  There was a lot more data in
the flash but the next file was a "param" file without a trailer.
Huh?  After comparing the file header to the previous I noticed that
the header had a value at offset 0x124 and not zero as the earlier
ones.  Ahh, I see, if the header has a file size, there's no need for
a trailer any more.  I modified my extractor and continued.

It got worse.  The next few pages was just garbage.  But it was
followed by more file headers for files like "savewave" and multiple
copies of "table1", "tale" and "table3".  I modified my extractor to
ignore "bad" pages and look for the next header.

I'm not sure if that "garbage" is actually something important or not,
but I hope I won't have to care.  We'll see later.

Contents of the param file
==========================

When I disassembled the second stage bootloader I could see that it
was verifying a checksum of the file contents.  But where did the
checksum it was comparing with come from?

After some time I realized that the data was coming from the "param"
file.  For the "os" file there are five 32 bit words at offset 0x124.
The first word is a flag word, if it contains 0xabcdabcd it means that
the "os" file has been written to flash and the words following that
is the load address, another address of some kind, the file size and
the file checksum.

This is then followed by similar flag, load address, size and checksum
fields for the "hz", "tx", "me", "hlp", "fp" and "bmp" files.

For each file (and copy) written to flash a new "param" (and
"paramcp") file is written with the fields for that file filled in.
That explains why there are so many copies of the param files in the
file system.

I even disassembled the checksumming function.  It turned out to be a
crc32 variant which I then rewrote in python:

    def checksum(data):
        s = 0
        for c in data:
            s ^= ord(c) << 8
            for i in range(8):
                s <<= 1
                if s & 0x10000:
                    s ^= 0x1021
            s &= 0xffffffff

        return s

When I tested the checksum function with the values from the "param"
file they actually matched the contents of the files.  Great!  More
confirmation that my file extractor actually works the way it should.

The Ugly
========

From some strings found in the NAND dump it looks as if OWON were
planning to use Yaffs as the file system, but for some reason they
decided to build their own file system instead.  I'm not even sure if
it's worthy of being called a file system, it's extremely simple with
no wear leveling and doesn't even seem to have a way of overwriting
files if the file system becomes full.

That's OK with me, if they only need a set of static files they don't
need more.  But what is more worrying is that I don't consider this
file systems as especially secure.  As I wrote in my previous post,
NAND is unreliable.  NAND flash _will_ develop spontaneous bit errors
over time, even if it just sits there without being written.  One
needs error correction to be able to compensate for this.

This file system has no error correction at all.  Since they have left
20 bytes as zeroes out of every page in a file, I guess they were
planning to stick some kind of error correcting codes (ECC) in there
but never got around to it.  And sticking the error correction codes
in the data itself is kind of dumb since the NAND flash they are using
has 64 bytes of "OOB" data associated with every page which is
specifically intended for error correcting codes.  I have later dumped
the OOB data from Linux and it's also unused and all zeroes.

I can't see a good way in the file system of handling bad pages
either, unless they just scan for the next header in the file system
if something goes wrong.  That might have been what happened with the
"garbage" I saw in my flash dump.  I'm also not sure how the file
system would handle if the magic identifier from the header would be
found as data in one of the files in the file system.

The bootloader does do error _detection_.  It verifies that important
files such as the operating system file match a checksum, and there is
a copy of the file that will be used in that case.  Yes, in a way this
is error correction since it means that they can recover from a bit
error in either the original or the copy, but not both.

There is a pretty high risk that both will develop bit errors.  With
"high risk" I don't mean that it will happen to every scope, it might
be one scope out a hundred, but the risk is higher than what I
personally would be happy with if I was a manufacturer delivering
thousands of units.  Especially since it's so easy to do proper error
correction, it's not hard to search for "ECC algorithm source" and
implement it.  The Samsung S3C2416 even has error correction in
hardware using that OOB data, all one has to do is to switch it on
when writing and reading flash pages.

There is also no error correction used for the second stage
bootloader.  It is small, less than 75kBytes, so the risk of a bit
error on those specific pages isn't that high, but it would still have
been so easy to do it properly.

My general feeling is that OWON builds quite nice hardware, but the
software isn't up to par and it is a bit disappointing.

It might all have changed
=========================

After I did this analysis I upgraded my scope to the latest version of
the software.  The first and second stage bootloaders are unchanged,
but the rest of the file system looks completely different.  I haven't
bothered figuring out what has happened and tried to understand the
new layout but it might be better in some ways.  Or maybe I'm just
confused and need to make a new flash dump and start looking at it.

But I probably won't.  I have a set of files from the old firmware
that I can analyze and that's good enough for now.

Results
=======

What is the result from this session?  I have managed to extract a
bunch of files, most importantly the FPGA bitstream and the operating
system.  I should be able to load the operating system file in Medusa
and start disassembling it to figure out how it works.

If I were only interested in hacking the scope to have higher
bandwidth I could start looking for the functions that set up the
bandwidth limiting filters in the variable gain amplifier.  They
shouldn't be too hard to find and to modify.  I could then write to
"os" file and update the checksum in the "param" file.

That's not really what I'm interested in though.  I'm more interested
in figuring out how the all the hardware in the scope works and write
my own FPGA code and firmware from scratch.  So I'll mostly use the
disassembly to figure out how the hardware works and ignore the rest
of what the current operating system is doing.

But I'll save that for another post.
