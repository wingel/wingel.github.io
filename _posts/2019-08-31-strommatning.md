---
layout: post
title: Strömmätning
tags:
- nerdy stuff
- current measurements
excerpt: Jag har byggt en ampere-meter.
id: b742352f-d288-47e5-9a12-adcef1e4d0e4
---

Ja, tja, jag har till och från jobbat med små batteridrivna prylar.
En fråga jag alltid fått från chefen är "hur ofta behöver man byta
batterier?"  Det är rätt viktigt att veta en sån sak.  Om en pryl kan
klara sig på ett knappcellsbatteri i ett par år så är det jättebra, om
man måste ha 4 AA-batterier som behöver bytas varannan månad så
sabbar det lätt kundens upplevelse av produkten.  Och det är en
jättesvår fråga att svara på.

För en ficklampa är det inte så svårt, den drar ingenting när den är
avstängd och om lysdioderna sen behöver 100mA när lampan är tänd så
kan man rätt lätt räkna ut att man får ungefär 8 timmars batteritid
med ett batteri på 800mAh.  Eller så har man i varje fall en
någorlunda enkel och jämn urladdningskurva som man kan räkna på.

En IoT-pryl brukar ha ett mycket mer dynamiskt beteende.  Prylen är
för det mesta i sleep mode och drar några microampere.  Sen vaknar den
till liv och då drar CPUn ett par milliampere.  Sen drar igång radion
för mottagning och då drar den ytterligare 10mA under 50
milllisekunder medans den sitter där och lyssnar.  Om den behöver
svara så måste den även sända och då går strömförbrukningen upp till
20mA under 3 millisekunder.  Har prylen en lysdiod som blinkar till så
kanske det drar 1mA under 100ms.  Osv.

En pryl som uCurrent är nästan oanvändbar för sånt här, om man ställer
in skalan på den så man kan mäta strömförbrukningen i sleep mode så
kommer spänningsfallet över shuntresistorn (burden voltage) vara så
högt vid 10mA att prylen dör på grund av för låg matningsspänning.
Man kan försöka komma runt det här genom att sätta dioder över
shuntresistorn.  Då begränsar man spänningsfallet till ett par hundra
millivolt, men om man t.ex. har en pryl som strömförsörjs direkt från
ett 3V knappcellsbatteri så är ett par hundra millivolt rätt mycket.
En fin dyr bänkmultimeter som kan mäta ner till microampere har ofta
samma problem.  Sen är en multimeter rätt dålig på att visa dynamiska
förlopp, man kan bara mäta på strömmar som inte varierar för mycket.

Man kan komma med en rätt bra gissning ändå, om prylen har en testmode
där man t.ex. kan säga åt den att slå på radion i mottagningsläge och
sen hänga där.  Då kan man mäta strömförbrukningen med en noggrann
multimeter och sen titta på hur länge prylen är i respektive läge med
ett oscilloskop.  Sen är det bara att ta mätningarna för varje läge
och räkna ut amperetimmar=ampere*sekunder/3600 och summera ihop dem.
Det är jobbigt och tråkigt men det fungerar någorlunda bra.  Fast med
moderna IoT-prylar med bluetooth low energy som växlar mellan flera
olika strömsparlägen och där man inte kommer åt testmoderna så blir
det jobbigare och jobbigare att göra sånt här för hand.

I rätt många år har jag haft i bakhuvudet att det borde gå att göra
något bättre.  Hur svårt ska det vara att bygga något som både klarar
av mäta höga strömmar på säg 100mA men som också kan mäta små strömmar
ner till några mikroampere?  Och som kan göra det utan för stort
spänningsfall över mätaren?  Och som kan logga strömförbrukningen med
någon millisekunds upplösning så att man kan se strömförbrukningen
över tid?

En modern multimeter som en Keithley DMM6500 för 10000 kronor kan
logga mätningar över tid så den kanske skulle kunna göra allt det där,
men det är rätt mycket pengar för ett mätinstrument.  Jag vet inte
heller om den klarar av att växla mellan mätområden snabbt nog.

Jag har i varje fall skissat och funderat på en sån här mätpryl till
och från i flera år.  Jag har läst på om hur en transimpedance
amplifier (TIA) fungerar: de är väldigt bra på att mäta väldigt låga
strömmar utan att burden voltage blir för stor.  Jag har funderat på
hur man kan utöka området som en sån förstärkare klarar av att driva
hålla nere burden voltage, och på sätt att hålla nere burden voltage
när förstärkaren ändå inte orkar längre.  Jag har simulerat och byggt
en massa testkretsar.  Men sen har det kommit jobb eller andra saker
emellan och så har projektet hamnat på hyllan igen.

För ett par veckor sen bestämde jag mig för att faktiskt få ändan ur
och göra det här på riktigt.  Jag tog de kretsar som fungerat bäst i
simulering och ritade ett kretskort där jag stoppade in alltihop.  Jag
fick mönsterkorten förra fredagen och har suttit i verkstan och lött
och mätt och provat saker på kvällarna efter jobbet.

Det jag byggt är en kombination av en vanlig ampere-meter med en
10mOhm shunt-resistor.  Den klarar av att mäta ström upp till +/-3A
och ner till +/-100µA innan signalen försvinner i bruset.  Sen har jag
en transimpedance amplifier i serie med den som kan mäta upp till
+/-300µA och ner till +/-10nA eller så innan bruset tar över.
Transimpedance amplifiern i sig har jag modifierat så att den klarar
av att kompensera för spänningsfallet över mätkretsen ända upp till
+/-200mA.  För att burden voltage inte ska bli för stor vid strömmar
över det så har jag en MOSFET som kortsluter ingången till
transimpedance amplifiern när strömmen genom shunt-resistorn är över
+/-100mA.  Överlappet mellan mätområdena borde göra att jag kan mäta
ström hela vägen från +/-10nA upp till +/-3A och MOSFETen borde göra
så att kretsen beter sig som om den bara hade 10mOhm shunt-resistans
(plus lite till för MOSFETen) hela vägen upp till 3A.

Och tamigtusan om det inte verkar fungera.  Eller ja, det verkar
fungera efter att ha fulpatchat en del misstag i min konstruktion, men
sånt får man väl räkna med.

Om man börjar nerifrån.  Så här ser det ut om jag sveper min
strömkälla från -10nA till +10nA i steg om 1nA.  Inte bra, man kan ju
se en trend, men i början så var ju mätvärdena helt fel.  Om jag
skulle göra samma mätning en gång till så lär jag få en helt annan
kurva för att det är så mycket brus och mätvärdena driver fram och
tillbaka.

![png]({{ "images/2019-08-31-strommatning/m1.png" | relative_url }})

Svep från -100nA till +100nA i steg om 10nA.  Mycket bättre.  Det
finns ett litet gain-fel, om man tittar på Y-axeln så rapporterar
kretsen ett lite högre värde än 100nA för en ström in på 100nA.
Gainen verkar vara några procent högre än vad den borde vara.  (Eller
så är det min strömkälla som levererar ett par procent högre ström än
vad den borde.)  Men utöver det så ser det ju jättebra ut.

I verkligheten så har utsignalen en DC-offset på ungefär 13uV som jag
räknat bort innan jag översatt utspänningen i volt till ampere.

![png]({{ "images/2019-08-31-strommatning/m2.png" | relative_url }})

Svep från -1µA till +1µA i steg om 100nA.  Rakt och fint och inget
märkbart gain-fel.  Den röda linjen är alltså från
transimpedance-amplifiern som mäter små strömmar.  Den gröna linjen är
mätvärdet från shunt-resistorn, men det är bara bruset som syns vid så
låga strömmar.

![png]({{ "images/2019-08-31-strommatning/m3.png" | relative_url }})

Svep från -10µA till +10µA i steg om 1µA. Inga konstigheter. Den röda
linjen från transimpedance amplifiern ser bra ut. Den gröna linjen
från shunt-resistorn börjar gå åt rätt håll, men den är fortfarande
skräp.

Fonten som används i skalan är trasig, fyrkanten borde vara "µ".

![png]({{ "images/2019-08-31-strommatning/m4.png" | relative_url }})

Svep från -100µA till +100µA. Nu kommer man till området där
mätningarna från shunt-resistorn börjar bli användbara. Mätvärdena är
fortfarande brusiga och det finns en offset men det är nästan
användbart. Mätningarna från transimpedance amplifiern ser fortfarande
bra ut.

![png]({{ "images/2019-08-31-strommatning/m5.png" | relative_url }})

Svep från -1mA till +1mA. Här tog transimpedance-amplifierns mätområde
slut. Den förstärker med 10000V/A och utspänningen kan variera mellan
ungefär +/-3.5V vilket gör att den bara är linjär upp till ungefär
+/-300µA. Men här börjar ju mätnignarna från shunt-resistorn vara bra
nog att ta över.

![png]({{ "images/2019-08-31-strommatning/m6.png" | relative_url }})

Svep från -10mA till +10mA. Inga konstigheter här heller. Mätvärdet
från transimpedance amplifiern är oanvändbart vid de här strömmarna
även om den fortfarande ser till att burden voltage är låg. Mätvärdet
från shunt-resistorn är snyggt och linjärt dock.

Tyvärr så lyckades jag inte få med burden voltage i mätningarna jag
gjorde innan jag smet från verkstan igår, men om jag minns rätt så
ligger den fortfarande på enstaka millivolt här.

![png]({{ "images/2019-08-31-strommatning/m7.png" | relative_url }})

Svep från -100mA till +100mA. Nånstans här så har MOSFETen slagt till
och kortslutit transimpedance amplifiern.

![png]({{ "images/2019-08-31-strommatning/m8.png" | relative_url }})

Svep från -1A till +1A. Inga konstigheter.

Det här är så långt jag kunde köra med min fin-strömkälla. Men jag har
även testat för hand med ett labbaggregat att kretsen klarar av att
leverera ett vettigt mätvärde upp till +/-3A och att burden voltage
ligger kring +/-30mV då. Vid +/-5A så får man inte ut några vettiga
mätvärden längre, men burden voltage höll sig kring +/-50mV.

![png]({{ "images/2019-08-31-strommatning/m9.png" | relative_url }})

Så, tja, själva biten som tar en ström in och levererar en spänning ut
på två områden verkar ju fungera. Nu är det bara resten kvar.

Jag har köpt en flerkanals 24-bitars 100ksps A/D-omvandlare som jag
tänkt använda för att få in spänningarna i en microcontroller. Men
först behövs det lite signalnivåanpassning och lågpassfilter mellan
mätkretsen och A/D-omvandlaren. Sen måste jag skriva nån slags
firmware för microncontroller också som kan strömma samples över USB
till en PC eller spara ner det på ett SD-kort.

Jag återkommer väl och berättar hur det gick om ytterligare ett par år.
