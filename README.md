# INF226
## Assignment 2+3

# 2A
Strukturen kunne fått en positiv forbedring ved å legge css i en egen fil. Dette ville gjort det enklere og utvikle applikasjonen til ett større produkt senere hvis det skulle være relevant. Da kunne du lagt inn standardisert css som alle filene skal ha og gjort mindre endringer i hvert enkelt ark/fil. Laget egne mapper for å rydde i strukturen. Laget Functions, Login, Register, Messages og templates mapper som inneholder ulik logikk om de forskjellige områdene. Dette er smart for videre utvikling når prosjektet og appen blir større.

Fant fort ut at koden hadde flere svakheter. Dette er noen av de:

*	Du kan skrive rett til databasen i url-en. Dette fikset jeg fort med å legge til @login_required ved alle metoder som sender eller mottar data fra databasen.
*	Appen viser nøyaktig sql-spørringer (Bare å fjerne koden som skriver ut sql-spørringen)
*	Programmet mangler Cookies med SAME-site attributes. Disse sjekker hvordan tredje og førsteparts cookies skal bli behandlet. Sørger for at cookies ikke blir sendt til tredjepart.
*	Meldingene som blir sendt er heller ikke krypterte. (f.eks fare for man-in-the-middle-attack)
*	Brukerne sine passord blir lagret i vanlig tekst i databasen. Dette har jeg fikset ved å hashe passordene og legge til salt.
*	Ubrukte python filer som kan brukes til backdoor angrep.
*	Login systemet sjekker heller ikke passordet til brukeren, men logger inn kun ved bruk av brukernavn.
*	SQL injections er mulig ved bruk av foreksempel:
-	$ ‘UPDATE messages SET message=’Du er blitt hacket’ WHERE sender=’Bob’;--
*	Videre kan sending av meldinger misbrukes i den forstand at du kan sende meldingen:
-	$ <span onclick=alert(1)> Hello World!<span>
hvor alert(1) kan byttes med skadelig kode
*	Du kan også sende melding fra hvem som helst til hvem som helst. Ingen accountability altså.
*	Programmet har en veldig dårlig secret key. Secret key blir brukt som signatur på cookies og meldinger. Denne bør ikke være tilgjengelig for en eventuell hacker. I programmet finner vi den som app.secret_key = ‘mY s3kritz’. Dette fikser man lett ved bruk av secret.token_hex(128).
*	Koden mangler Content security policy header, noes om kan oppdage mulige angrep som for eksempel xss-angrep.
*	CSRF angrep (Cross Site Request Forgery) er mulig på systemet siden vi ikke har noen CSRF token sjekk. Det kan implementeres enkelt ved bruk av for eksempel wtforms i login formen. Siden vi ikke har en token-sjekk kan en bruker av systemet bli lurt(social engineering) til å trykke på en form på en annen nettside slik at hackeren kan hente ut alle meldingene gjennom skadelig program i url-en.
*	Send metoden er både en POST og GET request som betyr at en bruker kan bli lurt til å trykke på en link som vil sende en melding til serveren. Dette kan gjøres ved å for eksempel klikke på en slik link:
-	Localhost:5000/send?sender=Bob&message=HACKED
Dette er fordi å klikke på en lenke er som oftest GET og ikke POST request.


At databasen ligger i samme fil som resten av logikken er også noe som gir en dårlig struktur. SOLID-prinsippene blir ikke brukt nevneverdig og heller ikke noen konkrete designpatters. For eksempel slik som MVVM eller flask sitt standard prosjekt struktur. 

# 2b

Jeg har prøvd å lage en app som kan registrere brukere og sende enkle meldinger til hverandre. Først begynte jeg med å fjerne unødvendig kode og refraktorer slik at strukturen ble mere lesbar. La funksjonalitet i ulike mapper. Opprettet Functions mappen som inneholder ulike funksjoner som gjerne kan brukes flere steder og av ulike filer. Ved bruk av mappene ga jeg meg selv og evt andre ett bedre bilde over prosjektet og dens funksjonaliteter. Valgte å gå utenfor flask sin standard med static filer(css,js-files), men valgte å beholde templates mappen. Dette fordi jeg er mest vant til logic, functions og templates fra andre prosjekter og føler meg tryggere på dette.

Videre sørget jeg for at inloggingsystemet funket som det skulle. At vi faktisk sjekket brukerne opp mot brukernavn og passord og ikke bare på navn. Lagret også disse brukernavnene og passordene på en tryggere måte ved å hashe passord å legge til salt. Salt gjør at rainbowtables og lookuptables blir umulig å bruke. Alle brukernavnene må være unike og alle passord må ha en lengde på mere enn 8 tegn. Dette er ting man kunne videreutviklet slik at man måtte ha ulike symboler og annet for å unngå mulige angrep. Må inneholde store og spesial tegn er typiske eksempler man møter på når man oppretter passord og gjør det vanskeligere med brute-froce angrep. Dette er noe som ikke er alt for vanskelig å implementere, men valgte å bruke tiden andre steder istedenfor.

Deretter laget jeg muligheten til å sende meldinger fra kun den brukeren som var logget inn fordi man kunne hvem som helst som skulle sende og motta i skjellet-koden. Gjorde det også mulig å bare sende til brukere som finnes i databasen ved bruk av en dropdownlist. Dette er en løsning for å slippe mye andre problemer. Som f.eks sende til brukere som ikke finnes. Målet mitt var å ha en mulighet til og sende meldinger en til en. Tror ikke det ville vært noe større problem å gjøre det mulig og velge flere mottakere, men igjen så var tid en sårbar faktor. 

Når du kommer inn på meldingsiden kan du sjekke om du har mottatt meldinger ved å trykke på knappen. Denne sjekker databasen for meldinger for den innloggede brukeren. Det gjør at de som skal se meldingen er de eneste som får dette. Ved mere tid vil det være lurt å implementere slik at meldingene blir kryptert og dekryptert, slik at man unngår man-in-the-middle angrep. HTML som eventuelt eksisterer i meldingene, vil ikke bli kjørt slik at vi unngår mulige XSS angrep.

Personen som sender en melding, må sjekkes for CSRF-token slik at det ikke har blitt tuklet med POST requesten slik at den kommer fra noen andre. Dette gjør vi ved bruk av @login_required fra wtforms i både login og register. Men vi gjør det manuelt når vi sender meldingene. Meldingene som blir sendt blir notert med både avsender og mottaker også timestamp og en id. Dette gjør at vi får en god tracability på meldingene og blir vanskeligere å tukle det til (i motsetning til i 2A :D). 

For å sikre meg mot sql-injection har jeg sørget for at det ikke går an å tukle med spørringene som man kunne gjøre enkelt ved bruk av search-funksjonen i 2A. Nå er det man skriver i feltene en del av spørringen slik at det ikke blir mulig. Prøvd å gjennomføre en søkefunksjonalitet i dine egne meldinger som du har sendt og mottatt. Mulighet for å se sine meldinger ved bruk av knappen Show messages som viser kun dine egne meldinger hvor du står som receiver. Vet ikke helt om en funksjonalitet som å søke opp har noe å gjøre i ett meldingssystem, men men.

## Features of this application

Simpel applikasjon hvor det er mulig å sende meldinger en til en.

## Creating user

Mulig å opprette egen bruker med eget valgt brukernavn og passord. Brukernavn må være unikt og mere enn 2 tegn. Passordet må ha en lengde på minimum 9 tegn.

## Logging in

Login siden kan du logge inn eller velge å opprette en ny bruker. Hvis du logger inn med en bruker som finnes i databasen blir du ført videre til meldingsystemet.

## Message application

Her kan du sende meldinger til deg selv eller andre brukere på systemet. Også mulighet for å søke opp ord eller tegn i mottatte meldinger. Mulige brukere blir vist i en dropdown list, mens vi har knapper som send som sender meldinger, search som søker etter ord i meldinger og show messages som viser alle meldingene du har lov til å se.

## Logging out

Kanskje den featuren jeg brukte lengst tid på å lage. Slet lenge med at du kunne «logge ut», men ved bruk av tilbake knappen så var du fortsatt logget inn. Fikk fikset dette med javascript til slutt og sørget for at cookies og sessions blir nullstilt ved utlogging. Typisk at mange bare sender deg til innloggingsiden med en href.

## Hvordan kjøre applikasjonen

Applikasjonen kjører ved bruk av kommandoen «flask run» selv om jeg hadde problemer med denne kommandoen så måtte jeg kjøre prosjektet med «python3 -m flask run» dette kan høre sammen med at jeg har en eldgammel mac (2013-modell :P). Jeg har kun generert en bruker: bob med passord: bananas

Hvis du vil sende melding til noen andre enn deg selv blir du derfor nødt til å benytte deg av registreringsskjemaet før du logger deg inn. Bare sørg for at brukernavn har mere enn 2 tegn og passord har 9 eller flere. Det dukker dessverre ikke opp hvilke feilmeldinger som skulle oppstå på hvorfor du ikke får opprettet bruker. Dette gjelder også ved innlogging. Skulle gjerne vist en rød tekst med passord er feil eller passord er for svakt eller brukernavn er allerede tatt. Anbefaler å teste meldingsfunksjonaliteten og spesielt search knappen hvor jeg ikke er 100% sikker på om det er bombesikkert for sql-injection. Selv om jeg har gjort det umulig for både sql og xss angrep etter boka.

## Tekniske detaljer til prosjektet

Denne applikasjonen benytter seg av teknologien gitt i boilerplate prosjektet, login-server. Uansett for hashing har jeg benyttet meg av bcrypt biblioteket. For tilfeldig secret_key brukte jeg secrets-biblioteket. For å håndetere login og logout, brukte jeg flask_login og for CSRF verifisering benyttet meg av flask_wtf.CSRFProtect.

## Spørsmål

### *Threat model - who might attack the application? What can an attacker do? What damage could be done (in terms of confidentiality, integrity, availability)? Are there limits to what an attacker can do? Are there limits to what we can sensibly protect against?*

Det finnes mange feil ved prosjektets orginale tilstand som nevnt over i 2A. Så hvis vi antar at dette er ett meldingsystem som faktisk brukes enten om det er privat bruk eller en bedrift så kan vi anta at det er flere mulige angripere. En uvenn kan ha lyst til å se hva du og din bestevenn skriver til hverandre eller hente ut brukernavn og passord fra databasen hvor mange har samme brukernavn og passord flere steder. Noen angripere kan ha som mål å endre informasjonen som allerede er i applikasjonen mens andre bare vil at applikasjonen ikke skal fungere (etc. Konkurrenter). 

Først og fremst er det muligheter for XSS-angrep slik at du kan lure brukeren til å trykke på meldingsinnhold som er ondsinnet. Det er heller ikke noen CSRF beskyttelse i meldingskoden som følger med slik at dette er enda en svakhet.

SQL-injection er mulig gjennom search funksjonaliteten. Dette kan føre til at angriperen henter ut alt fra databasen. Bolierplaten har gjort dette mulig i messages og announcements. De vil også kunne endre og slette informasjon hvis de vil det også.

Alt dette utgjør en gigantisk trussel mot applikasjonen og brukerne. SQL-injeksjonen er alene ett brudd på alle tre elementene i CIA triad (Confidentiality, integrity, availability). Konfidensialiteten er brutt ved at angriperen henter ut sensitiv informasjon fra databasen. Integriteten er brutt ved at angriperen har mulighet til å endre informasjonen i databasen og tilgjengeligheten er brutt ved at angriperen har mulighet til å slette data eller hele databasen. Fra CSRF og XSS bryter du også med troverdigheten(authenticity) og ansvarligheten(accountability) fordi en melding kan for alt du vet være fra en angriper eller hacker og ikke den du måtte tro.

Det at login kun sjekker brukernavnet og ikke noe passord kalles for broken authentication og er ett stort sikkerhetsproblem.

Allikevel er angriperen temmelig begrenset i skade omfang fordi applikasjonen er såpass simpel og bare lagrer meldinger og kunngjøringer slik at angriperen kun kan manipulere rundt disse to.

Det er også begrenset hvor sikkert man kan gjøre en applikasjon. Vi kan selvfølgelig opprette tiltak mot de angrepene som allerede er kjente, men det er derfor data sikkerhet er såpass i vinden om dagen siden det hele tiden utvikler seg og mere og mere data samles og kan misbrukes hvis det skulle ende opp i feil hender. Når du prøver å forsvare deg mot noen type angrep kan det hende du åpner opp for andre. Som igjen fører til at du må forsvare og beskytte deg mot dette også. Dette krever mye tid og evt penger for bedrifter. Derfor er det mange som ender opp med applikasjoner og nettsider med udugelig sikkerhet.

### *What are the main attack vectors for the (boilerplate) application?*

Søke- og sende-funksjonaliteten på prosjektet er hovedområdene for angrep.

### *What should we do (or what have you done) to protect against attacks?*

Vi bør beskytte oss mot de tre sårbarhetene jeg har snakket om; SQL, XSS og CSRF. SQL-injection forhindres ved bruk av forberedte setninger når du legger inn brukerdata i SQL-spørringer. Dette har jeg forhindret med å fjerne mulighetene og legge det i knapper. Slik at alt blir knyttet til innlogget bruker og begrenser sjansen for å skrive inn i spørringen. Også gjort det umulig å endre avsender og kun sende til registrerte brukere. Søke og kunngjørings funksjonaliteten er også endret slik at den ikke kan tukles med. XXS-angrep er tatt kontroll over ved å ikke lese brukerinput som html men heller sette det inn som html gjennom innerText. CSRF angrep har jeg allerede skrevet om tidligere i oppgavene (Token, POST). Lagre passord i vanlig form er ganske dumt så det å hashe dem var noe av det første jeg tenkte på og var fort gjort. Viktig å huske salt slik at det ikke kan knekkes med lookup tables.
Ett nøkkelord for å ha noe sikkert i nåtiden hvor mange angrep kommer gjennom social-engineering er å bruke «sunn fornuft». Ikke trykk på lenker i mails du ikke vet hvor kommer fra...

### *What is the access control model?*

Applikasjonen som ble utgitt skulle ha Mandatory Access Control, der brukere skal ha tillatelse til å gjøre alt i applikasjonen, mens personer uten bruker sannsynligvis ikke skulle ha det. Siden autentiseringen er svært ødelagt, og nettsiden ikke krever at du er logget inn for å gjøre noen av disse, har den dermed i praksis ingen access control.
I applikasjonen min eksisterer denne Mandatory Access Control på en måte siden det er forskjell på å være logget inn og logget ut. Hver bruker kan kun lese meldinger sendt eller mottatt. Dette hindrer alle brukere unntatt to fra å ha tilgang til og lese innholdet. Denne tilgangskontrollmodellen kalles Discretionary Access Control, hvor kun eieren og en gitt subjekt/bruker har tilgang.

### *How can you know that your security is good enough?*

Det finnes aldri god nok sikkerhet. "God nok" sikkerhet er vanskelig å definere, men jeg vil definere det som å minimere angrepsoverflaten slik at de fleste/alle de vanligste sårbarhetene dekkes, forhindre slike angrep som SQL-injeksjon, XSS osv. Men siden det alltid kan eksistere sikkerhetsfeil i hver applikasjon, er sporbarhet en viktig funksjon. Dette betyr at hvis det til slutt var et sikkerhetsbrudd, kan du spore opprinnelsen og prøve å forhindre at flere slike angrep skjer. Denne sporbarhetsegenskapen kan vi få fra logging av ulike aktiviteter i applikasjonen.

Takk for meg!

**Daniel Nyvoll**
