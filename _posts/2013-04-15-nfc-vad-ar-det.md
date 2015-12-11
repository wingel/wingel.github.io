---
layout: post
title: NFC, vad är det?
date: '2013-04-15T20:09:00.001+02:00'
tags: 
modified_time: '2013-04-17T19:49:53.882+02:00'
id: tag:blogger.com,1999:blog-4618495377058807667.post-551203389437497090
redirect_from: /2013/04/nfc-vad-ar-det.html
---

Jag har just skaffat en ny Android-telefon med stöd för "NFC".  NFC
betyder "Near Field Communication" eller på ren svenska trådlös
överföring av information mellan två prylar som är nära varandra.  På
svenska brukar man annars prata om beröringsfria kort.  Ett exempel är
kortet som används för att åka med Stockholms Lokaltrafik.

Fast NFC är rätt luddigt, det handlar mer om marknadsföring och jag är
mer intresserad av tekniken under.  Eftersom jag sitter fast på
Arlanda just nu och väntar på ett försenat flyg så har jag passat på
att läsa på lite.

Tydligen så stödjer Androids NFC fyra olika olika tekniker för
kommunikation med beröringsfria kort:

NfcA - ISO 14443 Type A.  En radiokodningsstandard för hur man skickar
data på 13.56MHz och som brukar användas för beröringsfria kort.
Längsta avstånd mellan läsare och kort brukar vara kring 5-10c och man
kan få en överföringshastighet på några hundra kilobit/sekund.  Mifare
är baserat på 14443 Type A.  Jag jobbat en hel del med Mifare som
används i passersystem.  Mifare används också i en en massa
betallösningar, bland annat Access-korten som används i Stockholms
lokaltrafik, Oyster Card i Londons lokaltrafik och (upptäckte jag
idag) tio- kortet på Arlanda Express.

NfcB - ISO 14443 Type B.  En annan radiokodningsstandard som är
väldigt lik Type A men lite annorlunda.  "Det som är så bra med
standarder, alla har en."  Den stora fördelen med Type B är att man
tydligen kan överföra mer energi till kortet än vad Type A kan, så man
kan göra mer intressanta saker i korten med Type B.  Det finns en
standard som heter iClass som för det mesta använder Type B.

NfcV - ISO 15693.  Ytterligare en radiokodningstandard för 13.56MHz.
Till skillnad från ISO 14443-varianterna så kan den användas på längre
avstånd, ända upp till någon meter.  Men man får betydligt lägre
överföringshastighet, mellan 5-25kilobit/sekund.  Så för passersystem
där man vill kunna öppna en dörr genom att komma nära den så vill man
använda ISO 15693 istället för 14443.  Men man har inte tillräckligt
med överföringshastighet för att kunna göra speciellt avancerade
saker.  I iClass så ingår även ISO 15693.

NfcF - FeliCa.  En standard från Sony i Japan för olika beröringsfria
betalkort som också jobbar på 13.56MHz.  Ganska lik ISO 14443 Type A/B
men lite annorlunda.  FeliCa var nästan på väg att bli standardiserad
som ISO 14443 Type C men det blev inget.  "Det som är så bra med
standarder..."  Används för kollektivtrafik på en massa ställen i
Asien som Bankok och Hong Kong.  Singapore EZ-Link använde tydligen
Felica förut men har bytt till Mifare nuförtiden.

Bara för att vara någorlunda komplett så ska jag väl också nämna att
det finns en äldre standard för beröringsfria kort som kallas för "EM
Marin" som jobbar på 125kHz.  Överföringshastigheten är väldigt låg
och det finns nästan ingen säkerhet, men det är robust och kan fungera
på flera meters avstånd.  Om man har beröringsfria kort i huset där
man bor så är det förmodligen EM Marin även om det börjar dyka upp
Mifare även där.  Vad jag kan se så stödjs inte EM Marin av Android.

