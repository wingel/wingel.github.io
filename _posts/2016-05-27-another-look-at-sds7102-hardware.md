---
layout: post
title: Another look at the hardware in the SDS7102
tags:
- nerdy stuff
- sds7102
id: 936bd5a6-1c14-4bd5-9379-0f70e1ca7b36
---

This is a post in a series about me poking at the insides of my OWON
SDS7012 oscilloscope.  You might want to start reading at the
[beginning]({{site.baseurl}}/2016/05/01/sds7102-hacking.html).

Except for soldering some wires to the JTAG and serial port on the
scope, most of the things I have discoveries about the SDS7102 I have
made so far has been done with just software and a bit of thinking.
But I was getting closer and closer to the point where I would have to
crack the scope open again and take a closer look at the hardware to
be able to discover more things.

So I did.  I also desoldered the shield covering the analog frontend
(AFE).  Here are a few photos of the main circuit board (click on them
for lager pictures).

[![Front of main PCB]({{site.baseurl}}/images/2016-05-27-another-look-at-sds7102-hardware/main-front.jpg)]({{site.baseurl}}/images/2016-05-27-another-look-at-sds7102-hardware/main-front-large.jpg)

[![Back of main PCB]({{site.baseurl}}/images/2016-05-27-another-look-at-sds7102-hardware/main-back.jpg)]({{site.baseurl}}/images/2016-05-27-another-look-at-sds7102-hardware/main-back-large.jpg)

Here's rough block diagram of how I think the pieces fit together.

![Block diagram]() bild som visar komponenter ovanpå en blek bild av
kretskortet.  Både framsida och baksida.  Rita i inkscape tror jag.

System on Chip
==============

The first part of the scope is a rather generic embedded computer
based around a System on Chip (SoC).  The SoC contains a 400Mhz ARM9
processor with a lot of built in peripherals display controller, USB
host and device controllers, serial ports (UART), a JTAG inteface for
debugging and a few more peripherals that aren't used in this design.
This SoC together with a DDR2 memory and a NAND flash comprises a
complete little embedded computer.  The SDS7102 designers have also
tacked on a 10/100Mbit ethernet controller.

TODO namn och länk till datablad för alla komponenter

U? is the Samsung S3C2416 SoC.

U? is the main 12MHz crystal for the SoC

U? is a 128MBbyte K9F1G08U0D Samsung NAND flash.  It's connected to
the the external bus controller on the SoC.  It seems to work fine
with the S3C2412 NAND flash driver built into the Linux kernel.

U? is a 64MByte Hynix DDR2 memory.  It's connected to the SDRAM
controller of the SoC.  It's initialized by the bootloader and seems
to work fine.

U60? is a mysterious connector which has not been populated.  I'm a
bit curious about what it does.

U?? is the USB host connector.  It's connected to the USB host
controller on the SoC and works fine with the OHCI driver in Linux.

U? is a TI TPS2041 "Power distribution switch" which provides power to
the USB host port.  This switch has an enable input and an overcurrent
output that could have been connected to the SoC to allow both control
and monitoring of the USB host port voltage.  As far as I can tell the
enable input is hardwired to always on and there's nothing that
monitors the output.

U? is the USB device connector.  It's connected to the USB device
controller on the SoC and works fine with the S3C24???? USB device
driver in Linux.  GPF2 on the SoC is used to detect the presense of
VBUS on the connector.

Below the USB device connector are three plated holes which are
connected to a serial port (UART0) on the SoC.  It works with the
S3C24xx UART driver in Linux.

U? is the VGA connector.

U? is the a KSZ8851SNL "Single Port MAC/PHY" 10/100Mbit ethernet
controller.  It is connected to the high speed SPI (HSSPI) port on the
SoC.  It works fine with the ksz8851?? driver in Linux.

X? is a 25MHz crystal for the ethernet controller.

U? is the Ethernet connector.

There are a few more components on the other side of the PCB that are
not shown in the block diagram above.

U? is a Chrontel CH7206 "TV/VGA Encoder" which translates the LCD
display signals into a VGA signal.  I've already discovered that the
I2C bus used to control this chip is connected to GPB4 and GPB9 on the
SoC and I can talk to it using the i2c-gpio driver in Linux.  I
haven't tried configuring the VGA controller yet it shouldn't be that
hard to make it work.

U9, a 74AC08 "Quad AND Gate" seems to be used as a driver for some of
the signals in the VGA connector.  Everything is hardwired so there's
nothing to configure here.

U? is an AT88SC CryptoMemory, basically an I2C memory with encryption.
It probably stores the serial number in an encrypted formats which is
then used for copy protection.  I have not figured found out how to
talk to this chip yet, and even if I do the contents are encrypted
which means I won't be able to do anything with the information
anyway.

U? is a TI TPS65051 "Automotive 6-channel Power Management IC (PMIC)"
which provides some of the voltages used by the system.  As with the
USB power switch it has a couple of enable inputs which could have
been controlled by some GPIO pins on the SoC but I don't think they
are, it looks like they are hardwired to be always on.

In the upper left corner there is a connector for a cable to the front
panel with all the buttons and knobs on the front of the scope.  I
haven't figured out how this works yet.

In the upper right corner there is a connector to the display board.
Most of the pins from GPC and GPD are used for the LCD panel itself.
GPB3 is used to control the display brightness.  The LCD also works in
Linux.

The buzzer.  I have never heard this one making noise, despite
changing most of the GPIO ports configured as outputs on the SoC.
I wonder how it is connected?  It's GPB0.

All these components, except for the VGA controller, the front panel
and the buzzer, are working in Linux.

Signal Processing
=================

The next part is consists of an Analog to Digital Converter (ADC), a
Field Programmable Gate Array (FPGA) and yet another DDR2 memory.  The
ADC samples the two scope channels and feeds the samples to the FPGA.
The FPGA does some signal processing and then stores the processed
samples in the DDR2 memory.

The FPGA is connected to the SoC via some bus, probably same expansion
bus as the NAND flash is connected to, and some extra I/O pins on the
SoC that are used to configure the FPGA with the FPGA bitstream.  This
allows the SoC to access the samples via the FPGA and present them on
the display.

U? is the FPGA, a Xilinx Spartan 6 SC6SLX9.  I have figured out how to
configure the FPGA.  GPK3, GPK5, GPK7, GPK11 and GPK13 on the Soc are
connected to CCLK, DONE, PROG_B, DIN and INIT_B on the FPGA.  The FPGA
is programmed using slave serial mode driven by the SoC. I'm hoping
that the high bandwidth bus between the FPGA and SoC will be using the
same bus as the NAND flash, but I have a sneaking suspicion that it
isn't.

U? is the DDR2 memory, the same Hynix 64MByte memory as used for the
SoC.  I need to figure out how it is connected to the FPGA.  The FPGA
has a built in hard SDRAM controller which supports DDR2 memory, so
hopefully they have used one of the default Xilinx Memory Interface
Generator (MIG) pinout.

U? is the ADC, a Texas Instruments ADC08D500 (produktnamn) which can
sample two channels with 8 bits of resolution at 500Msamples/s.  It
can also combine the two channels and sample one channel at
1Gsamples/s.  This chip has a SPI bus for control.  I need to figure
out where the CS/CLK/DIN pins are connected.  I need to figure out how
the digital sample outputs are connected to the FPGA, but that ought
to be fairly easy after I have started talking to the ADC over SPI.
There might be other pins that are interesting such as the RST or CAL
inputs or the overrange output.

U? is a a 10MHz crystal oscillator (XO) which provides the a very
stable reference frequency for the signal processing block.  Nothing
to control here.

U? is a ADF4360-7 ??? PLL & VCO.  It outputs a frequency between ??
and ?? MHz which is phase locked to the 10MHz reference clock.  This
frequency is used by the ADC as the sampling clock.  This chip has a
SPI bus for control.  I need to figure out where the CS/CLK/DIN pins
are connected.  And maybe a few more pins.

R?? to R?? are resistors packs that are probably connected in series
with all signals on the bus between the FPGA and the SoC.

External trigger output.  There's probably some kind of drive circuit
which is then controlled by the FPGA.

Probe compensation output.  Probably also driven by the FPGA.

Lots of things to discover.  The DDR memory bus and the bus to the SoC
are the two big worries here.

Analog Frontend
===============

The Analog Frontend (AFE) takes the signals from the scope probes,
feeds them through some relays that select AC or DC coupling and the
input attenuation.  There are a few amplifiers, some with fixed gain
and also a variable gain attenuator which can also be used to low pass
filter the signal.  An analog mux, one per channel, is used to select
one of the signals inside frontend which is then fed to a PECL
comparator which provides triggering.  An 8 channel digital to analog
converter (DAC) is used to provide various reference voltages used in
the AFE, most probably one output per channel which is used to to
shift the level of the input signals and two more channels to to set
the triger voltages for the comparator.

Analog electronics aren't my strongest point so I can't really explain
all that's happing here.  The nick "tinhead" drew a schematic for the
AFE on the [EEVblog forums](länk).  Anyway, I'm mostly interested in
the components that have digital connections which can be controlled
by the SoC or the FPGA.

The main components of the AFE are the following:

J?, J?, back of the scope probe inputs.

J?, external trigger input.

U? and U? are solid state relays (part no?).  It the relay is inactive
the signal from the probe input will pass through the capacitor next
to it and the signal will be AC coupled.  If the relay is acitve it
shorts the capacitor the input will be DC coupled.  This relay
probably needs some kind of drive circuit which is the connected to
I/O pins on the SoC or the FPGA.

U?, U?, U? and U? are NEC ?? mechanical relays which switch between
different attenuator banks on the respective channels.  They
definitely need a drive circuit.  When I was writing data to random
GPIO pins on the SoC earlier I could hear relays switching so they are
probably controlled by the SoC.

U?, U? are two more mechanical relays.  One relay is next to the
external trigger input so it probably has something to do with
triggering.  The other one is in the middle between the two channels,
but since there's only one relay between two channels it I'm a bit
confused about what it does.  But first I want to figure out how it is
controlled.

U?, U? and U? are OP Amps, one for each channel and one for the
external trigger input.  As far as I can tell there are no digital
signals to control here.  This is probably where the DC level of each
channel is shifted by voltages from the DAC.

U? and U? are LMH6518 variable gain amplifiers, one per channel.  They
have a bunch of registers which can be written using a SPI bus.  I
need to figure out where these pins, (chip select/latch enable, clock
and data in, reset?), are connected.

U? in the channel 1 box, votlage regulator I think.  No digital. controls.

U?, big component outside the afe box, voltage regulator I think.  No
digital. controls.

U58, with big inductor next to it.  Probably a DC/DC converter.
Hopefully no digital controls.

On the other side there are some more components.  Ny bild på blek
bild av kretskortet.

J?, J?, front of the scope probe inputs.

J?, front of external trigger input.

U? and U?, video MUX.  Each one takes some signal from the respective
channel, buffer it and feeds it to the PECL comparator.  There are
three digital inputs on each MUX, A0, A1 to select and input and ???
to enable/disable the output.

U?, dual PECL comparator.  There's probably one channel per
comparator, the reference voltage for each channel probably comes from
the DAC.  There are some "latch enable" pins that might be controlled
by the FPGA.

U? is a [Rhom BU2506FV "10bit 8ch D/A
converter"](http://www.rohm.com/web/global/products/-/product/BU2506FV)
- probaly used to provide the voltages to shift the levels of the
input channels and to set the comparison voltages for trigger.
SPI-like bus, LE, clk, data.

U? and U? are more amplifiers, seems to be one per channel.  I hope
there aren't any digital controls here.

U? is a ???? in the middle between the two channels.  I don't know
what it does.  Probably nothing to control.

U? is a ???.  Unidentified chip.  Two wires leading up.  Could be a
bus, or outputs.

Finishing up
============

This time I have a much better idea of how everything fits together
even though there are still some unesolved questions such as what the
myster chip ?? actually is.

Lots of components, lots of connections between the components to
discover.  But that's the subject for another post.

