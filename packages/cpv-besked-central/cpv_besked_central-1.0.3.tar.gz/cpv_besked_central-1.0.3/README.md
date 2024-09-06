# Coding Pirates Kuglebane Central

En simpel Web server der kan agere som den "globale kuglebane kommando central" :-)

## Opstart af server

Kan startes med `start.sh` scriptet, der starter flask op med:

`flask --app besked_central run --host=0.0.0.0`

`--host=0.0.0.0` gør den tilgænglig på alle interfaces, så man kan ramme den fra en anden maskine på netværket (så man kan teste det lokalt).

På URL'en `http://localhost:5000/` kan man tilgå administrations interfacet. Afhængigt af om man er _admin_ eller _controller_ kan man administrere brugere, kuglebaner og events for hhv. alle afdelinger eler kun sin egen afdeling.

## API

Serverens udstiller et API som man kan kalde fra [_kuglebane controlleren_](https://github.com/Coding-Pirates-Viborg/kuglebane-controller) kan modtage requests.

### `/token`

For at tilgå API'et skal man bruge en JWT token, der kan hentes med en registreret bruger via Basic Auth

JWT'en skal sendes med til de efterfølgende requests.

Se `*_api.py` filerne for hvilke endpoints der udstilles.

Eller få et hurtigt overblik i administartionsmodulets _API_ fane (http://localhost:5000/apidoc)

## Flask i virtuelt environment

Der er lagt op til at flask er installeret i et Python virtuelt environemnt (venv), som beskrevet i flask dokumentationen:

https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments

Start en terminal og gå til roden af repositoriet: `/cpv-besked-central/` og kør kommandoen:

`python3 -m venv venv`

For at oprette et virtuelt miljø på din egen maskine.
