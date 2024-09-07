# Coding Pirates Kommando Central

En simpel Web server der kan agere som en "global kommando central", hvor man kan sende en kommando fra en gruppe til en
anden - på tværs af afdelinger.

## Formål

Fungerer som et simpelt generisk API, der kan bruges til at sende kommadoer mellem forskellige systemer, så denne
kompleksitet kan abstraheres væk fra workshoppen.

F.eks. er _kommando centralen_  brugt til at sende "digitale kugler" fra en kuglebane til en anden, eller til at sende
simple tekstbeskeder fra en web-side til en anden.

# Struktur

Kommandoer sendes fra én enhed til en anden. En enhed kan være en enkelt pirat eller en gruppe - det afhænger af
workshoppen.

Hvad den enkelte kommando gør, er op til hvad man har defineret i workshoppen. For en kuglebane kan det f.eks. være at
man sender en START kommando, mens man for en simpel besked service kunne sende en BESKED kommando med en tilhørende
tekst.

Når en kommando afsendes lander den derfor hos den modtagende enhed, hvorefter den kan behandles af den pågældende
enhed.

En enhed er altid tilknyttet en afdeling og hver afdeling kan have et vilkårligt antal enheder.

Til hver afdeling er der oprettet én særskilt API-bruger, der bruges til at sende og modtage kommandoer på vegne af den pågældende
afdeling. API-brugeren oprettes på forhånd af en udvikler.

Derudover oprettes (minimum) én administrator per afdeling, der eftefølgende kan oprette og administrere grupper via
dashboardet.

## Opstart af server

Kan startes med `start.sh` scriptet, der starter flask op med:

`flask --app kommando_central run --host=0.0.0.0`

`--host=0.0.0.0` gør den tilgænglig på alle interfaces, så man kan ramme den fra en anden maskine på netværket (så man
kan teste det lokalt).

På URL'en `http://localhost:5000/` kan man tilgå administrations interfacet. Afhængigt af om man er _admin_ eller
_controller_ kan man administrere brugere, enheder og kommandoer for hhv. alle afdelinger eler kun sin egen afdeling.

## API

Serverens udstiller er REST API til at sende og modtage kommandoer, eller info om kommandoer.

### `/token`

For at tilgå API'et skal man bruge en JWT token, der kan hentes med en registreret bruger via Basic Auth

JWT'en skal sendes med til de efterfølgende requests.

Se `*_api.py` filerne for hvilke endpoints der udstilles.

Eller få et hurtigt overblik i administartionsmodulets _API_ fane (http://localhost:5000/apidoc)

## Flask i virtuelt environment

Der er lagt op til at flask er installeret i et Python virtuelt environemnt (venv), som beskrevet i flask
dokumentationen:

https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments

Start en terminal og gå til roden af repositoriet: `/cpv-besked-central/` og kør kommandoen:

`python3 -m venv venv`

For at oprette et virtuelt miljø på din egen maskine.
