# Draaiboek en voortgang — Zoeten Inval telsysteem

Dit document is het geheugen van het project. Nieuwste informatie onderaan (overdrachtsblok). Geen persoonlijke gegevens hier: de repo is openbaar.

## Verloop in het kort (oktober 2026)

| Datum | Wat |
|---|---|
| ~11 okt | Eerste versie als tegelpagina in Claude (artefact): kaart van het café, tellen, afrekenen, wisselgeld. Gebruikt op iPhone/Android als tegel op het beginscherm. |
| 11 okt | Kaart uitgebreid (Het bord, Bier van de klant, Dagartikel met vrije prijs), beheerscherm voor prijzen en artikelen. |
| 11 okt | Beslissing: gedeelde klantrekeningen over alle gsm's → eigen hosting nodig. Gekozen: GitHub Pages (pagina) + Firebase Realtime Database (gegevens), beide gratis. Reden: een Claude-artefact kan niet met Firebase praten. |
| 11–12 okt | Firebase-project `zoeten-inval-telsysteem` en GitHub-repo `lnelen61/zoeten-inval` aangemaakt; regels gepubliceerd; personeel meldt zich anoniem aan; beheerder met gebruikersnaam + wachtwoord; beheerderslijst in de database. |
| 12 okt | Oude gmail-login als beheerder verwijderd, Auto clean-up van anonieme gebruikers aangezet, oude link omgezet naar een "verhuisd"-pagina. |
| 12 okt | Toogscherm gebouwd, standaard uit (zie hieronder). Tegels half zo hoog. Instructiezin weg. Dagtotaal en totaal-van-alle-rekeningen weg. |
| 18 okt | Spraakbediening onderzocht: Stembediening van iOS bestaat niet in het Nederlands; proefpagina gemaakt en daarna geschrapt. Schakelaar Toogscherm verplaatst naar onder in Beheer kaart. |
| 19 okt | Overdracht naar Claude Code, werkpakket v1.0. |

## Beslissingen (en waarom)

- **Eén bestand, geen build.** Leo is half-amateur en moet kunnen volgen wat er gebeurt; een nieuwe versie plaatsen = één bestand vervangen.
- **Gratis stack.** Spark-plan en GitHub Pages volstaan ruim voor ~6 gsm's.
- **Personeel anoniem, beheerders met login, rechten via een lijst in de database.** Eenvoud voor personeel; alleen beheerders mogen de kaart wijzigen. Beheerders typen een gebruikersnaam (geen echt e-mailadres).
- **Rekeningen zijn open voor wie de link heeft.** Bewuste keuze; verder dichtzetten kan later (App Check of personeelslogins).
- **Toogscherm optioneel en standaard uit.** Bij drukte/fuiven aan, op kalme momenten uit. Alleen de beheerder schakelt. Bestellingen die rechtstreeks aan de toog gevraagd en betaald worden, gaan er niet langs.
- **Elke bestelling heeft medewerker en klant.** Naam van de medewerker wordt één keer per gsm gevraagd (en onthouden).
- **Geen artikel-uitverkocht-functie, geen melding aan de medewerker bij "klaar".** Wie aan de toog werkt, past een bestelling met de hand aan (minteken bij de regel).
- **Tablet: één rij, oudste links.** Posities blijven vast als er bestellingen bijkomen; de oudste (dringendste) staat altijd vooraan; geleverd staat grijs rechts, recentst geleverd het dichtst bij de open kaarten, zodat een correctie snel gevonden wordt.
- **Open bestellingen verdwijnen nooit door tijd** (een open rekening kan dagen openstaan). Geleverde bestellingen ouder dan 3 dagen worden door de tablet uit de database gewist.
- **Geen dagtotaal en geen totaal-van-alle-open-rekeningen:** totalen enkel per open klant.
- **Spraak niet doorgevoerd:** Nederlands ontbreekt bij Stembediening; een eigen microfoonknop is mogelijk maar onzeker op iOS in een tegel op het beginscherm en foutgevoelig in een luid café. Niet verder uitgewerkt.
- **Wifi/4G:** alle toestellen hebben internet nodig, ook op het terras; dezelfde wifi hoeft niet.

## Nog niet gedaan (open)

- Zoon als tweede beheerder (twee stappen, zie `ARCHITECTUUR.md`).
- Eigenaarschap Firebase (Google-account) en GitHub-account overdragen of een gedeeld café-account kiezen (stappen staan in het overdrachtsdocument van Leo; nooit de repo naar een ander account verhuizen).
- Back-ups buiten GitHub: kopie van `index.html` en JSON-export van de database.
- `spraaktest.html` uit de repo halen als ze er nog in staat.

## Testlog

| Datum | Wat | Resultaat |
|---|---|---|
| 12 okt | Echte test op gsm + tablet: bestelling doorsturen, bijbestellen op dezelfde klant, geluid | Geslaagd (door Leo) |
| 12 okt | Nieuwe versie met kaarten in één rij en lagere tegels | Geslaagd (door Leo, op tablet en gsm) |
| 19 okt | Rooktest in het uitgepakte werkpakket (Linux, nagebootste Firebase): 19 controles | Geslaagd; niet op Windows zelf getest (zie overdrachtsblok) |

---

## OVERDRACHTSBLOK — 19 oktober 2026 (naar Claude Code)

**Wat er gebeurt:** vanaf nu wordt het project hoofdzakelijk bewerkt in Claude Code op Leo's Windows-laptop, in `C:\Projecten\ZoetenInval-werk` (git clone van `https://github.com/lnelen61/zoeten-inval`, niet in OneDrive). Het eerdere werk gebeurde in een Claude-chat (Claude Docs voor het overdrachtsdocument).

**Stand:** versie v1.0. Alles hierboven staat live, behalve mogelijk de laatste kleine wijziging (schakelaar onderaan in Beheer kaart): controleer dat met `git diff --stat` na het kopiëren van het pakket in de clone.

**Wat te doen als eerste (volgorde):**
1. `STARTGIDS_Claude_Code.md` volgen tot en met de controle-opdracht (stap 6).
2. `CLAUDE.md` lezen (werkafspraken en conventies).
3. `git diff --stat` bekijken; verschilt `index.html`, dan Leo vragen of de nieuwste versie gepubliceerd mag worden (`v1.0` taggen en pushen).
4. Open punten afwerken op vraag van Leo (zie "Nog niet gedaan").

**Waar niet-publieke gegevens staan:** `lokaal\BEHEERGEGEVENS.md` (gitignored): beheerdersgebruikersnaam, UID, links naar de consoles en het overdrachtsdocument. Het beheerderswachtwoord staat nergens in bestanden; Leo kent het.

**Bekende zwakke punten:** (a) rekeningen zijn voor iedereen met de link leesbaar en wijzigbaar; (b) de tests dekken de echte Firebase, het aanmelden als beheerder en de regels niet; (c) iOS/Safari-gedrag en geluid zijn enkel handmatig te testen; (d) Firebase-regels worden niet via git gepubliceerd.

**Werkafspraken kort:** Nederlands; één stap per bericht met de volledige opdracht; "ok" volstaat; eerst documenteren dan verder; vóór elke wijziging aan de laptop eerst de rollback noteren; Leo beslist wanneer we stoppen; variabelen in code uitleggen met commentaar.

**Resultaat van de test van de uitgepakte zip (19 oktober 2026), eerlijk:**

- Getest (in een Linux-omgeving, zip uitgepakt in een lege map): `node tests/check_syntax.mjs` → OK; nieuwe Python-omgeving (venv) met `pip install -r tests/requirements.txt` → playwright 1.56.0; `tests/smoke_test.py` → `ALLES OK (19 controles)`; `git init` + `git add -A` in de uitgepakte map → `lokaal/` werd niet gevolgd; zoekopdracht naar vaste Linux-paden (`/home/claude`, `/mnt`, `/opt`, `/tmp`), sleutels/tokens en e-mailadressen buiten `lokaal/` → niets gevonden.
- NIET getest: uitvoering op Windows zelf (de opdrachten met `.\.venv\Scripts\python.exe` en `Expand-Archive`/`robocopy`), `playwright install chromium` op Windows (in de testomgeving stond de browser al klaar), `git clone`/`git push` naar het echte GitHub, de echte Firebase (aanmelden, regels, meerdere toestellen), iOS/Safari, geluid.
- Gevolg: de eerste keer op de laptop kan een opdracht anders reageren dan hier. Meld dan de exacte foutmelding; niets in het pakket schrijft naar Firebase of GitHub zonder dat jij een opdracht geeft.
